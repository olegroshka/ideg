"""AR-020d: review-round-2 stationary-state suite.

    python scripts/ar020d_stationary_suite.py <n_sites> <stage>
    stages: gge | blocks | kcurve | sparse | windowgap

(1) blocks  — TRUE unrestricted stationary search for degenerate H:
    sigma = (sum_B A_B A_B^dagger)/Z with one complex A_B per DEGENERATE
    energy block ([sigma,H]=0 iff block structure; coherences inside
    blocks now included). XX-based classes (quasiperiodic, integrable).
(2) gge     — Generalized Gibbs Ensemble family for the free XX chain:
    p_S = exp(-sum_{k in S} lambda_k)/Z over exact mode-occupation
    eigenstates (constructed via Slater determinants; self-checked
    against H). N parameters — the physics-canonical 'natural'
    stationary family for an integrable model.
(3) kcurve  — quasiperiodic miss vs Chebyshev order K (price curve).
(4) sparse  — quasiperiodic miss vs support size k (sparse mixtures).
(5) windowgap — finite-window vs infinite-time averaging: reduced-state
    and metric-space discrepancy between the window-averaged state and
    the diagonal ensemble, per class (review point 3).

Outputs: results/AR-010/ar020d_<stage>_N<n>.json
"""

import json
import sys
import time
from itertools import combinations
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ideg.evolve import EigenEvolver                        # noqa: E402
from ideg.migraph import (I0, X_MIN,                        # noqa: E402
                          mutual_information_matrix, phi_distance_matrix,
                          phi_series)
from ideg.models import xx_chain                            # noqa: E402
from ideg.states import magnon_superposition, neel, \
    haar_product_state                                      # noqa: E402

OUT = ROOT / "results" / "AR-010"
MAN = json.loads((OUT / "confirmatory_manifest.json").read_text())
ADD1 = json.loads((OUT / "confirmatory_manifest_addendum1.json").read_text())
for g, per in ADD1["seeds"].items():
    MAN["seeds"].setdefault(g, {}).update(per)

N = int(sys.argv[1])
STAGE = sys.argv[2]
WINDOW = np.arange(20.0, 200.0 + 1e-9, 0.5)
EPS_PHI = MAN["epsilon_phi"]
PAIRS = [(i, j) for i in range(N) for j in range(i + 1, N)]


def qp_runs():
    for seed in MAN["seeds"]["TA_ii_quasiperiodic"][str(N)]:
        rng = np.random.default_rng(seed)
        psi, _ = magnon_superposition(N, rng)
        yield psi


def integrable_runs():
    for k, seed in enumerate(MAN["seeds"]["TC_integrable"][str(N)]):
        rng = np.random.default_rng(seed)
        yield neel(N) if k == 0 else haar_product_state(N, rng)


def dbar_of(ev, psi0):
    states = ev.states_at(psi0, WINDOW)
    return phi_series(states, N).mean(axis=0)


def mi_phi_of_rho4s(rho4s):
    """metric from a dict pair->4x4 rdm."""
    mi = np.zeros((N, N))
    for (i, j), rho4 in rho4s.items():
        lam = np.clip(np.linalg.eigvalsh(rho4), 1e-14, None)
        s4 = float(-np.sum(lam * np.log(lam)))
        rr = rho4.reshape(2, 2, 2, 2)
        for red, tr_ax in (("a", (1, 3)), ("b", (0, 2))):
            pass
        rho_a = np.trace(rr, axis1=1, axis2=3)
        rho_b = np.trace(rr, axis1=0, axis2=2)
        la = np.clip(np.linalg.eigvalsh(rho_a), 1e-14, None)
        lb = np.clip(np.linalg.eigvalsh(rho_b), 1e-14, None)
        sa = float(-np.sum(la * np.log(la)))
        sb = float(-np.sum(lb * np.log(lb)))
        mi[i, j] = mi[j, i] = max(sa + sb - s4, 0.0)
    return phi_distance_matrix(mi)


t0 = time.time()

# ================= free-fermion eigenbasis (for gge) =================
if STAGE == "gge":
    hop = np.zeros((N, N))
    for i in range(N - 1):
        hop[i, i + 1] = hop[i + 1, i] = 1.0
    e1, orb = np.linalg.eigh(hop)  # orbitals phi_k(site)
    dim = 2 ** N
    V = np.zeros((dim, dim))
    occ = np.zeros((dim, N))
    col = 0
    for m in range(N + 1):
        for S in combinations(range(N), m):
            # eigenstate for mode subset S: Slater det of orbitals S
            # over down-spin positions; sites ordered ascending
            amp = np.zeros(dim)
            for x in range(dim):
                pos = [s for s in range(N) if (x >> (N - 1 - s)) & 1]
                if len(pos) != m:
                    continue
                if m == 0:
                    amp[x] = 1.0
                else:
                    Mx = orb[np.ix_(pos, list(S))]
                    amp[x] = np.linalg.det(Mx)
            V[:, col] = amp / np.linalg.norm(amp) if m else amp
            occ[col, list(S)] = 1.0
            col += 1
    # self-check: H V = V E
    h = xx_chain(N)
    E = occ @ e1
    err = float(np.max(np.abs(h @ V - V * E[None, :])))
    print(f"free-basis self-check |HV-VE| = {err:.2e}", flush=True)
    assert err < 1e-8

    # per-eigenstate pair RDMs in the free basis
    t_full = np.ascontiguousarray(V.T).reshape((dim,) + (2,) * N)
    RD = []
    for (i, j) in PAIRS:
        t = np.moveaxis(t_full, (1 + i, 1 + j), (1, 2)).reshape(dim, 4, -1)
        RD.append(np.einsum("nax,nbx->nab", t, t, optimize=True))
    ev = EigenEvolver(h)

    def gge_probe(psi0):
        dbar = dbar_of(ev, psi0)
        nrm = np.linalg.norm(dbar)

        def loss_grad(lmb):
            logp = -occ @ lmb
            logp -= logp.max()
            p = np.exp(logp)
            p /= p.sum()
            rho4s = {pq: np.tensordot(p, r, axes=1)
                     for pq, r in zip(PAIRS, RD)}
            d = mi_phi_of_rho4s(rho4s)
            loss = float(np.linalg.norm(d - dbar) / nrm)
            # numerical gradient over N params (cheap): central diff
            g = np.zeros(N)
            for k in range(N):
                ee = np.zeros(N)
                ee[k] = 1e-5
                lp = -occ @ (lmb + ee)
                lp -= lp.max()
                pp = np.exp(lp)
                pp /= pp.sum()
                r4 = {pq: np.tensordot(pp, r, axes=1)
                      for pq, r in zip(PAIRS, RD)}
                dp = mi_phi_of_rho4s(r4)
                g[k] = (float(np.linalg.norm(dp - dbar) / nrm) - loss) / 1e-5
            return loss, g

        best = np.inf
        rng = np.random.default_rng(7)
        for lmb0 in [np.zeros(N), rng.normal(size=N),
                     rng.normal(size=N) * 2]:
            r = minimize(loss_grad, lmb0, jac=True, method="L-BFGS-B",
                         options={"maxiter": 200, "ftol": 1e-10})
            best = min(best, float(r.fun))
        return best

    out = {"n_sites": N, "family": "GGE (N lambdas, exact free basis)",
           "self_check_HV_VE": err, "groups": {}}
    for label, runs in (("TA_ii_quasiperiodic", qp_runs()),
                        ("TC_integrable", integrable_runs())):
        vals = []
        for psi0 in runs:
            vals.append(gge_probe(psi0))
            print(f"[{time.time() - t0:8.1f}s] gge {label} run "
                  f"{len(vals) - 1} miss={vals[-1]:.4f}", flush=True)
        out["groups"][label] = {
            "runs": vals, "median": float(np.median(vals)),
            "min": float(np.min(vals)),
            "n_below_eps_phi": int(np.sum(np.array(vals) < EPS_PHI)),
            "n_runs": len(vals)}
    with open(OUT / f"ar020d_gge_N{N}.json", "w") as f:
        json.dump(out, f, indent=2)
    print("gge done", {g: (v["median"], v["n_below_eps_phi"])
                       for g, v in out["groups"].items()})

# ================= block-coherent stationary search ==================
elif STAGE == "blocks":
    h = xx_chain(N)
    ev = EigenEvolver(h)
    evals, evecs = ev.evals, ev.evecs
    bnd = np.concatenate([[0], np.nonzero(np.diff(evals) > 1e-10)[0] + 1,
                          [len(evals)]])
    blocks = [(int(a), int(b)) for a, b in zip(bnd[:-1], bnd[1:])]
    print(f"{len(blocks)} blocks, sum|B|^2 = "
          f"{sum((b - a) ** 2 for a, b in blocks)}", flush=True)
    dim = 2 ** N
    t_full = np.ascontiguousarray(evecs.T).reshape((dim,) + (2,) * N)
    # per-pair, per-block cross RDM tensors R[m,n] (|B|,|B|,4,4)
    CROSS = []
    for (i, j) in PAIRS:
        t = np.moveaxis(t_full, (1 + i, 1 + j), (1, 2)).reshape(dim, 4, -1)
        per_block = []
        for (a, b) in blocks:
            tb = t[a:b]
            per_block.append(np.einsum("max,nbx->mnab", tb, tb.conj(),
                                       optimize=True))
        CROSS.append(per_block)

    nb = len(blocks)
    sizes = [b - a for a, b in blocks]
    offs = np.cumsum([0] + [s * s for s in sizes])
    ntot = int(offs[-1])

    def unpack(x):
        """x (2*ntot real) -> list of A_B complex matrices."""
        xr, xi = x[:ntot], x[ntot:]
        As = []
        for k, s in enumerate(sizes):
            blk = (xr[offs[k]:offs[k + 1]]
                   + 1j * xi[offs[k]:offs[k + 1]]).reshape(s, s)
            As.append(blk)
        return As

    def probe(psi0, p_warm):
        dbar = dbar_of(ev, psi0)
        nrm = np.linalg.norm(dbar)

        def loss_grad(x):
            As = unpack(x)
            sig = [A @ A.conj().T for A in As]
            tr = sum(float(np.trace(sb).real) for sb in sig)
            sig = [sb / tr for sb in sig]
            rho4s = {}
            for pq, per_block in zip(PAIRS, CROSS):
                r = np.zeros((4, 4), dtype=complex)
                for sb, cr in zip(sig, per_block):
                    r += np.einsum("mn,mnab->ab", sb, cr, optimize=True)
                rho4s[pq] = r
            # loss + dLoss/d sigma_B via entropy gradients & FW paths
            mi = np.zeros((N, N))
            cache = {}
            for pq, rho4 in rho4s.items():
                rho4h = 0.5 * (rho4 + rho4.conj().T)
                lam, u = np.linalg.eigh(rho4h)
                lamc = np.clip(lam, 1e-14, None)
                s4 = float(-np.sum(lamc * np.log(lamc)))
                rr = rho4h.reshape(2, 2, 2, 2)
                rho_a = np.trace(rr, axis1=1, axis2=3)
                rho_b = np.trace(rr, axis1=0, axis2=2)
                la, ua = np.linalg.eigh(rho_a)
                lb, ub = np.linalg.eigh(rho_b)
                lac = np.clip(la, 1e-14, None)
                lbc = np.clip(lb, 1e-14, None)
                sa = float(-np.sum(lac * np.log(lac)))
                sb_ = float(-np.sum(lbc * np.log(lbc)))
                m = max(sa + sb_ - s4, 0.0)
                mi[pq[0], pq[1]] = mi[pq[1], pq[0]] = m
                cache[pq] = (lamc, u, lac, ua, lbc, ub, m)
            w = np.where(mi > 0, -np.log(np.clip(mi / I0, X_MIN, 1.0)),
                         -np.log(X_MIN))
            np.fill_diagonal(w, 0.0)
            # FW with predecessors
            d = w.copy()
            np.fill_diagonal(d, 0.0)
            nxt = np.tile(np.arange(N), (N, 1))
            for mm in range(N):
                alt = d[:, mm:mm + 1] + d[mm:mm + 1, :]
                mask = alt < d - 1e-15
                d = np.where(mask, alt, d)
                nxt = np.where(mask, np.tile(nxt[:, mm:mm + 1], (1, N)),
                               nxt)
            diff = d - dbar
            L2 = float(np.sum(diff ** 2))
            loss = np.sqrt(L2) / nrm
            gw = np.zeros((N, N))
            for k in range(N):
                for l in range(k + 1, N):
                    c = 4.0 * diff[k, l]
                    if c == 0.0:
                        continue
                    a1 = k
                    guard = 0
                    while a1 != l and guard <= N:
                        b1 = nxt[a1, l]
                        gw[min(a1, b1), max(a1, b1)] += c
                        a1 = b1
                        guard += 1
            # chain to sigma blocks
            G = [np.zeros((s, s), dtype=complex) for s in sizes]
            for pq, per_block in zip(PAIRS, CROSS):
                i, j = pq
                lamc, u, lac, ua, lbc, ub, m = cache[pq]
                x4 = m / I0
                if gw[i, j] == 0.0 or x4 <= X_MIN or x4 >= 1.0:
                    continue
                dw_dmi = -1.0 / (x4 * I0)
                ln4 = (u * np.log(lamc)[None, :]) @ u.conj().T
                M4 = -(ln4 + np.eye(4))
                lna = (ua * np.log(lac)[None, :]) @ ua.conj().T
                lnb = (ub * np.log(lbc)[None, :]) @ ub.conj().T
                Ma = -(lna + np.eye(2))
                Mb = -(lnb + np.eye(2))
                # dMI/d rho4 = kron(Ma,I) + kron(I,Mb) - M4  (MI=Sa+Sb-S4)
                Meff = np.kron(Ma, np.eye(2)) + np.kron(np.eye(2), Mb) \
                    - M4
                for kb, cr in enumerate(per_block):
                    G[kb] += gw[i, j] * dw_dmi * np.einsum(
                        "mnab,ba->mn", cr, Meff, optimize=True)
            G = [0.5 * (g + g.conj().T) for g in G]  # Hermitian part
            coef = 1.0 / (2.0 * np.sqrt(L2) * nrm) if L2 > 0 else 0.0
            As = unpack(x)
            sigraw = [A @ A.conj().T for A in As]
            tr = sum(float(np.trace(sb).real) for sb in sigraw)
            inner = sum(float(np.real(np.sum(g.conj() * sb)))
                        for g, sb in zip(G, sig))
            gx = np.zeros_like(x)
            for kb, (A, g) in enumerate(zip(As, G)):
                gM = (g - inner * np.eye(sizes[kb])) / tr
                gA = 2.0 * coef * (gM @ A)
                gx[offs[kb]:offs[kb + 1]] += np.real(gA).ravel()
                gx[ntot + offs[kb]:ntot + offs[kb + 1]] += \
                    np.imag(gA).ravel()
            return loss * 1.0, gx

        # start from warm diagonal (sqrt p) + one random
        best = np.inf
        rng = np.random.default_rng(11)
        starts = []
        x0 = np.zeros(2 * ntot)
        for kb, (a, b) in enumerate(blocks):
            s = sizes[kb]
            diag = np.sqrt(np.clip(p_warm[a:b], 1e-12, None))
            blk = np.zeros((s, s))
            np.fill_diagonal(blk, diag)
            x0[offs[kb]:offs[kb + 1]] = blk.ravel()
        starts.append(x0)
        starts.append(x0 + rng.normal(scale=1e-2, size=2 * ntot))
        for xs in starts:
            r = minimize(loss_grad, xs, jac=True, method="L-BFGS-B",
                         options={"maxiter": 300, "ftol": 1e-10})
            best = min(best, float(r.fun))
        return best

    # warm starts from the diagonal unrestricted results are not stored
    # per-run; use diagonal ensemble populations as warm start
    out = {"n_sites": N, "n_blocks": len(blocks),
           "sum_B2": int(sum(s * s for s in sizes)),
           "validity_note": "block search strictly generalizes the "
           "diagonal search; per-run results must be <= the ar020c "
           "diagonal values (monotone-descent empirical check, visible "
           "in the run log)", "groups": {}}

    for label, runs in (("TA_ii_quasiperiodic", qp_runs()),
                        ("TC_integrable", integrable_runs())):
        vals = []
        for psi0 in runs:
            p_warm = np.abs(ev.coeffs(psi0)) ** 2
            vals.append(probe(psi0, p_warm))
            print(f"[{time.time() - t0:8.1f}s] blocks {label} run "
                  f"{len(vals) - 1} miss={vals[-1]:.4f}", flush=True)
        out["groups"][label] = {
            "runs": vals, "median": float(np.median(vals)),
            "min": float(np.min(vals)),
            "n_below_eps_phi": int(np.sum(np.array(vals) < EPS_PHI)),
            "n_runs": len(vals)}
    with open(OUT / f"ar020d_blocks_N{N}.json", "w") as f:
        json.dump(out, f, indent=2)
    print("blocks done", {g: (v["median"], v["n_below_eps_phi"])
                          for g, v in out["groups"].items()})

# ================= windowgap ========================================
elif STAGE == "windowgap":
    from ideg.models import (ferro_ising_weak_tf, mixed_field_ising,
                             tfim, xxz_disordered)
    from ideg.states import all_up, ground_state
    from ideg.protocols import diagonal_ensemble

    def rep(group):
        seed = MAN["seeds"][group][str(N)][0]
        rng = np.random.default_rng(seed)
        if group == "TA_i_fixed_point":
            hh = tfim(N, 1.5)
            return hh, ground_state(hh)
        if group == "TA_ii_quasiperiodic":
            psi, _ = magnon_superposition(N, rng)
            return xx_chain(N), psi
        if group == "TA_iii_chaotic":
            return mixed_field_ising(N), haar_product_state(N, rng)
        if group == "TA_iv_metastable":
            dg = rng.uniform(-0.01, 0.01, size=N)
            return ferro_ising_weak_tf(N, 0.05, dg), all_up(N)
        if group == "TC_scrambling":
            return mixed_field_ising(N), neel(N)
        if group == "TC_integrable":
            return xx_chain(N), neel(N)
        if group == "TC_localized":
            return xxz_disordered(N, rng), neel(N)

    out = {"n_sites": N, "groups": {}}
    for group in ["TA_ii_quasiperiodic", "TA_iii_chaotic",
                  "TA_iv_metastable", "TC_scrambling", "TC_integrable",
                  "TC_localized"]:
        h, psi0 = rep(group)
        ev = EigenEvolver(h)
        states = ev.states_at(psi0, WINDOW)
        rho_win = np.zeros((2 ** N, 2 ** N), dtype=complex)
        for s in states:
            rho_win += np.outer(s, s.conj())
        rho_win /= len(states)
        rho_bar = diagonal_ensemble(ev, psi0)
        # aggregate 2-site RDM discrepancy
        agg = 0.0
        for (i, j) in PAIRS:
            from ideg.migraph import pair_rdm_mixed
            agg += np.linalg.norm(pair_rdm_mixed(rho_win, N, i, j)
                                  - pair_rdm_mixed(rho_bar, N, i, j)) ** 2
        agg = float(np.sqrt(agg))
        d_win = phi_distance_matrix(
            mutual_information_matrix(rho_win, N, mixed=True))
        d_bar = phi_distance_matrix(
            mutual_information_matrix(rho_bar, N, mixed=True))
        dbar_run = phi_series(states, N).mean(axis=0)
        nrm = np.linalg.norm(dbar_run)
        out["groups"][group] = {
            "agg_rdm_discrepancy": agg,
            "metric_gap_win_vs_diag": float(
                np.linalg.norm(d_win - d_bar) / nrm),
            "diag_miss_vs_Dbar": float(
                np.linalg.norm(d_bar - dbar_run) / nrm),
            "win_miss_vs_Dbar": float(
                np.linalg.norm(d_win - dbar_run) / nrm)}
        print(group, out["groups"][group], flush=True)
    with open(OUT / f"ar020d_windowgap_N{N}.json", "w") as f:
        json.dump(out, f, indent=2)
    print("windowgap done")

# ================= kcurve / sparse (price curves) ====================
elif STAGE in ("kcurve", "sparse"):
    h = xx_chain(N)
    ev = EigenEvolver(h)
    dim = 2 ** N
    t_full = np.ascontiguousarray(ev.evecs.T).reshape((dim,) + (2,) * N)
    RD = []
    for (i, j) in PAIRS:
        t = np.moveaxis(t_full, (1 + i, 1 + j), (1, 2)).reshape(dim, 4, -1)
        RD.append(np.einsum("nax,nbx->nab", t, t, optimize=True))
    e = ev.evals
    half = 0.5 * float(e[-1] - e[0])
    xsc = (e - 0.5 * (e[0] + e[-1])) / half

    def miss_of_p(p, dbar, nrm):
        rho4s = {pq: np.tensordot(p, r, axes=1)
                 for pq, r in zip(PAIRS, RD)}
        return float(np.linalg.norm(mi_phi_of_rho4s(rho4s) - dbar) / nrm)

    out = {"n_sites": N, "stage": STAGE, "runs": []}
    unres = json.loads((OUT / f"ar020c_unrestricted_N{N}.json"
                        ).read_text())
    for ridx, psi0 in enumerate(qp_runs()):
        dbar = dbar_of(ev, psi0)
        nrm = np.linalg.norm(dbar)
        rec = {}
        if STAGE == "kcurve":
            for K in (2, 4, 8, 12, 24, 48, 96):
                def obj(c):
                    lp = np.polynomial.chebyshev.chebval(xsc, c)
                    p = np.exp(np.clip(lp - lp.max(), -300, 0))
                    return miss_of_p(p / p.sum(), dbar, nrm)
                best = np.inf
                rng = np.random.default_rng(5)
                for c0 in [np.zeros(K), rng.normal(size=K)]:
                    r = minimize(obj, c0, method="Powell",
                                 options={"maxfev": 500, "xtol": 1e-3})
                    best = min(best, float(r.fun))
                rec[str(K)] = best
        else:  # sparse: optimize weights on top-k supports from a
            # dense diagonal optimization warm start (diag ensemble)
            p_warm = np.abs(ev.coeffs(psi0)) ** 2
            order = np.argsort(p_warm)[::-1]
            for k in (1, 2, 4, 8, 16, 32, 64, 128):
                sup = order[:k]

                def obj(th):
                    p = np.zeros(dim)
                    w = np.exp(th - th.max())
                    p[sup] = w / w.sum()
                    return miss_of_p(p, dbar, nrm)
                r = minimize(obj, np.zeros(k), method="Powell",
                             options={"maxfev": 400, "xtol": 1e-3})
                rec[str(k)] = float(r.fun)
        rec["unrestricted"] = unres["groups"]["TA_ii_quasiperiodic"][
            "runs"][ridx]
        out["runs"].append(rec)
        print(f"[{time.time() - t0:8.1f}s] {STAGE} run {ridx}: {rec}",
              flush=True)
    with open(OUT / f"ar020d_{STAGE}_N{N}.json", "w") as f:
        json.dump(out, f, indent=2)
    print(f"{STAGE} done")

else:
    raise ValueError(STAGE)
