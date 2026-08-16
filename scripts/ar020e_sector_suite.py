"""AR-020e: round-3 sector/channel suite.

    python scripts/ar020e_sector_suite.py <n_sites> <stage>
    stages: channels | sector
    env: IDEG_GROUP     (channels: run one group; default = all six)
         IDEG_RUN_SLICE (sector: "lo:hi" run indices per class)

(1) channels — corrected motion-removal channels, ALL runs per class:
    rho_inf  = sum_E P_E rho P_E   (true infinite-time average: removes
               coherence between distinct energies ONLY)
    rho_diag = full eigenbasis diagonalization (stronger ablation: also
               deletes stationary within-block structure)
    rho_win  = trapezoidal window average of rho(t) on the sampling grid
    Misses of each vs the run's window-mean metric Dbar, plus win-vs-inf
    gaps at metric and reduced-state level.

(2) sector — invariance/admissibility controls for the commutant search
    (XX-based classes), three nested stationary algebras per run:
    T1 = commutant of {H}          (degenerate-energy blocks; AR-020d)
    T2 = commutant of {H, N_mag}   (joint (E, q) blocks: no cross-sector
                                    coherence; sector weights free)
    T3 = T2 + sector weights pinned to the run's Tr(rho Pi_q)
         (for the one-magnon quasiperiodic states this collapses to
          diagonal populations on the N nondegenerate magnon levels)
    Every optimized sigma gets an independent validation battery:
    trace, min block eigenvalue, ||[sigma, N_mag]||_F, sector weights,
    <H>, and the objective recomputed from the assembled full density
    matrix through the mixed-state metric path.

Outputs: results/AR-010/ar020e_channels_<group>_N<n>.json
         results/AR-010/ar020e_sector_N<n>[_slice<lo>-<hi>].json
"""

import json
import os
import sys
import time
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ideg.evolve import EigenEvolver                        # noqa: E402
from ideg.migraph import (I0, X_MIN,                        # noqa: E402
                          mutual_information_matrix, phi_distance_matrix,
                          phi_series)
from ideg.models import (ferro_ising_weak_tf,               # noqa: E402
                         mixed_field_ising, tfim, xx_chain, xxz_disordered)
from ideg.states import (all_up, ground_state,              # noqa: E402
                         haar_product_state, magnon_superposition, neel)

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
DIM = 2 ** N
NMAG_COMP = np.array([bin(x).count("1") for x in range(DIM)])

t0 = time.time()


def build_runs(group):
    """Yield (H, psi0) per manifest run (ar020b construction)."""
    seeds = MAN["seeds"][group][str(N)]
    for run_idx, seed in enumerate(seeds):
        rng = np.random.default_rng(seed)
        if group == "TA_ii_quasiperiodic":
            psi, _ = magnon_superposition(N, rng)
            yield xx_chain(N), psi
        elif group == "TA_iii_chaotic":
            yield mixed_field_ising(N), haar_product_state(N, rng)
        elif group == "TA_iv_metastable":
            dg = rng.uniform(-0.01, 0.01, size=N)
            yield ferro_ising_weak_tf(N, g=0.05, dg=dg), all_up(N)
        elif group == "TC_scrambling":
            psi = neel(N) if run_idx == 0 else haar_product_state(N, rng)
            yield mixed_field_ising(N), psi
        elif group == "TC_integrable":
            psi = neel(N) if run_idx == 0 else haar_product_state(N, rng)
            yield xx_chain(N), psi
        elif group == "TC_localized":
            yield xxz_disordered(N, rng), neel(N)


def energy_blocks(evals, tol=1e-10):
    bnd = np.concatenate([[0], np.nonzero(np.diff(evals) > tol)[0] + 1,
                          [len(evals)]])
    return [(int(a), int(b)) for a, b in zip(bnd[:-1], bnd[1:])]


def phi_of_mixed(rho):
    return phi_distance_matrix(mutual_information_matrix(rho, N, mixed=True))


def miss_of(rho, dbar, nrm):
    return float(np.linalg.norm(phi_of_mixed(rho) - dbar) / nrm)


# ================= channels =========================================
if STAGE == "channels":
    groups = ([os.environ["IDEG_GROUP"]] if os.environ.get("IDEG_GROUP")
              else ["TA_ii_quasiperiodic", "TA_iii_chaotic",
                    "TA_iv_metastable", "TC_scrambling", "TC_integrable",
                    "TC_localized"])
    for group in groups:
        recs = []
        for ridx, (h, psi0) in enumerate(build_runs(group)):
            ev = EigenEvolver(h)
            V, E = ev.evecs, ev.evals
            states = ev.states_at(psi0, WINDOW)
            dbar = phi_series(states, N).mean(axis=0)
            nrm = float(np.linalg.norm(dbar))
            # trapezoid on the uniform sampling grid
            wts = np.ones(len(states))
            wts[0] = wts[-1] = 0.5
            wts /= wts.sum()
            rho_win = np.zeros((DIM, DIM), dtype=complex)
            for wt, s in zip(wts, states):
                rho_win += wt * np.outer(s, s.conj())
            c = V.conj().T @ psi0
            p = np.abs(c) ** 2
            rho_diag = (V * p[None, :]) @ V.conj().T
            blocks = energy_blocks(E)
            rho_inf = np.zeros((DIM, DIM), dtype=complex)
            for a, b in blocks:
                v = V[:, a:b] @ c[a:b]
                rho_inf += np.outer(v, v.conj())
            d_inf = phi_of_mixed(rho_inf)
            d_diag = phi_of_mixed(rho_diag)
            d_win = phi_of_mixed(rho_win)
            # within-block stationary coherence weight of the run
            wcoh = float(sum(np.sum(np.abs(np.outer(c[a:b],
                                                    c[a:b].conj())) ** 2)
                             - np.sum(p[a:b] ** 2)
                             for a, b in blocks if b - a > 1))
            recs.append({
                "miss_inf": float(np.linalg.norm(d_inf - dbar) / nrm),
                "miss_diag": float(np.linalg.norm(d_diag - dbar) / nrm),
                "miss_win": float(np.linalg.norm(d_win - dbar) / nrm),
                "gap_win_vs_inf": float(
                    np.linalg.norm(d_win - d_inf) / nrm),
                "within_block_coherence_weight": wcoh,
                "purity_inf": float(np.real(np.trace(rho_inf @ rho_inf))),
                "purity_diag": float(np.sum(p ** 2))})
            print(f"[{time.time() - t0:8.1f}s] channels {group} run "
                  f"{ridx} inf={recs[-1]['miss_inf']:.4f} "
                  f"diag={recs[-1]['miss_diag']:.4f} "
                  f"win={recs[-1]['miss_win']:.4f}", flush=True)
        keys = ["miss_inf", "miss_diag", "miss_win", "gap_win_vs_inf"]
        summ = {k: {"median": float(np.median([r[k] for r in recs])),
                    "min": float(np.min([r[k] for r in recs])),
                    "max": float(np.max([r[k] for r in recs]))}
                for k in keys}
        with open(OUT / f"ar020e_channels_{group}_N{N}.json", "w") as f:
            json.dump({"n_sites": N, "group": group, "runs": recs,
                       "summary": summ}, f, indent=2)
        print(f"channels {group} done", summ, flush=True)

# ================= sector ===========================================
elif STAGE == "sector":
    h = xx_chain(N)
    ev = EigenEvolver(h)
    V, E = ev.evecs, ev.evals
    eblocks = energy_blocks(E)

    # joint (E, q) basis: rotate each degenerate block to diagonalize
    # the restriction of N_mag; eigenvalues must be near-integers
    U2 = V.copy()
    sub_blocks = []      # (a, b) in U2 column order
    sub_sector = []      # integer q per sub-block
    sub_eblock = []      # parent energy-block index
    for kb, (a, b) in enumerate(eblocks):
        Vb = V[:, a:b]
        Nb = Vb.conj().T @ (NMAG_COMP[:, None] * Vb)
        q, R = np.linalg.eigh(Nb)
        assert np.max(np.abs(q - np.round(q))) < 1e-8, "non-integer q"
        qi = np.round(q).astype(int)
        order = np.argsort(qi, kind="stable")
        U2[:, a:b] = Vb @ R[:, order]
        qs = qi[order]
        s0 = 0
        for i in range(1, b - a + 1):
            if i == b - a or qs[i] != qs[s0]:
                sub_blocks.append((a + s0, a + i))
                sub_sector.append(int(qs[s0]))
                sub_eblock.append(kb)
                s0 = i
    # sanity: U2 orthonormal, H-diagonal, N_mag-diagonal
    ortho_err = float(np.max(np.abs(U2.conj().T @ U2 - np.eye(DIM))))
    hd = U2.conj().T @ (h @ U2)
    hdiag_err = float(np.max(np.abs(hd - np.diag(np.diag(hd)))))
    nd = U2.conj().T @ (NMAG_COMP[:, None] * U2)
    ndiag_err = float(np.max(np.abs(nd - np.diag(np.diag(nd)))))
    assert ortho_err < 1e-9 and hdiag_err < 1e-7 and ndiag_err < 1e-7
    print(f"joint basis ok: {len(eblocks)} E-blocks -> "
          f"{len(sub_blocks)} (E,q)-blocks; errs {ortho_err:.1e} "
          f"{hdiag_err:.1e} {ndiag_err:.1e}", flush=True)

    def cross_tensors(basis, blocks):
        tf = np.ascontiguousarray(basis.T).reshape((DIM,) + (2,) * N)
        CROSS = []
        for (i, j) in PAIRS:
            t = np.moveaxis(tf, (1 + i, 1 + j), (1, 2)).reshape(DIM, 4, -1)
            CROSS.append([np.einsum("max,nbx->mnab", t[a:b],
                                    t[a:b].conj(), optimize=True)
                          for (a, b) in blocks])
        return CROSS

    CROSS1 = cross_tensors(V, eblocks)
    CROSS2 = cross_tensors(U2, sub_blocks)

    def make_search(blocks, CROSS, sec_of_block=None, sec_weights=None):
        """Return search(warm_As, extra_starts) over sigma = (+)A_B A_B^dag,
        globally normalized, or per-sector normalized to sec_weights."""
        sizes = [b - a for a, b in blocks]
        offs = np.cumsum([0] + [s * s for s in sizes])
        ntot = int(offs[-1])
        if sec_weights is not None:
            live = [k for k in range(len(blocks))
                    if sec_weights.get(sec_of_block[k], 0.0) > 1e-10]
        else:
            live = list(range(len(blocks)))
        lsizes = [sizes[k] for k in live]
        loffs = np.cumsum([0] + [s * s for s in lsizes])
        lntot = int(loffs[-1])
        by_sector = {}
        if sec_weights is not None:
            for li, k in enumerate(live):
                by_sector.setdefault(sec_of_block[k], []).append(li)

        def unpack(x):
            xr, xi = x[:lntot], x[lntot:]
            return [(xr[loffs[i]:loffs[i + 1]]
                     + 1j * xi[loffs[i]:loffs[i + 1]]).reshape(s, s)
                    for i, s in enumerate(lsizes)]

        def normalize(Ms):
            if sec_weights is None:
                tr = sum(float(np.trace(M).real) for M in Ms)
                return [M / tr for M in Ms], {None: tr}
            trs = {q: sum(float(np.trace(Ms[li]).real)
                          for li in idx)
                   for q, idx in by_sector.items()}
            sig = [None] * len(Ms)
            for q, idx in by_sector.items():
                for li in idx:
                    sig[li] = Ms[li] * (sec_weights[q] / trs[q])
            return sig, trs

        def loss_grad(x, dbar, nrm):
            As = unpack(x)
            Ms = [A @ A.conj().T for A in As]
            sig, trs = normalize(Ms)
            rho4s = {}
            for pq, per_block in zip(PAIRS, CROSS):
                r = np.zeros((4, 4), dtype=complex)
                for li, k in enumerate(live):
                    r += np.einsum("mn,mnab->ab", sig[li], per_block[k],
                                   optimize=True)
                rho4s[pq] = r
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
            d = w.copy()
            np.fill_diagonal(d, 0.0)
            nxt = np.tile(np.arange(N), (N, 1))
            for mm in range(N):
                alt = d[:, mm:mm + 1] + d[mm:mm + 1, :]
                mask = alt < d - 1e-15
                d = np.where(mask, alt, d)
                nxt = np.where(mask,
                               np.tile(nxt[:, mm:mm + 1], (1, N)), nxt)
            diff = d - dbar
            L2 = float(np.sum(diff ** 2))
            loss = np.sqrt(L2) / nrm
            gw = np.zeros((N, N))
            for k in range(N):
                for l in range(k + 1, N):
                    cc = 4.0 * diff[k, l]
                    if cc == 0.0:
                        continue
                    a1 = k
                    guard = 0
                    while a1 != l and guard <= N:
                        b1 = nxt[a1, l]
                        gw[min(a1, b1), max(a1, b1)] += cc
                        a1 = b1
                        guard += 1
            G = [np.zeros((s, s), dtype=complex) for s in lsizes]
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
                Meff = np.kron(Ma, np.eye(2)) \
                    + np.kron(np.eye(2), Mb) - M4
                for li, k in enumerate(live):
                    G[li] += gw[i, j] * dw_dmi * np.einsum(
                        "mnab,ba->mn", per_block[k], Meff, optimize=True)
            G = [0.5 * (g + g.conj().T) for g in G]
            coef = 1.0 / (2.0 * np.sqrt(L2) * nrm) if L2 > 0 else 0.0
            gx = np.zeros_like(x)
            if sec_weights is None:
                tr = trs[None]
                inner = sum(float(np.real(np.sum(g.conj() * s_)))
                            for g, s_ in zip(G, sig))
                for li, (A, g) in enumerate(zip(As, G)):
                    gM = (g - inner * np.eye(lsizes[li])) / tr
                    gA = 2.0 * coef * (gM @ A)
                    gx[loffs[li]:loffs[li + 1]] += np.real(gA).ravel()
                    gx[lntot + loffs[li]:lntot + loffs[li + 1]] += \
                        np.imag(gA).ravel()
            else:
                for q, idx in by_sector.items():
                    s_q = sum(float(np.real(np.sum(G[li].conj().T
                                                   * sig[li])))
                              for li in idx) / sec_weights[q]
                    for li in idx:
                        gM = (sec_weights[q] / trs[q]) \
                            * (G[li] - s_q * np.eye(lsizes[li]))
                        gA = 2.0 * coef * (gM @ As[li])
                        gx[loffs[li]:loffs[li + 1]] += \
                            np.real(gA).ravel()
                        gx[lntot + loffs[li]:lntot + loffs[li + 1]] += \
                            np.imag(gA).ravel()
            return loss, gx

        def search(dbar, nrm, warm_As, n_extra=1, seed=11):
            rng = np.random.default_rng(seed)
            x0 = np.zeros(2 * lntot)
            for li, k in enumerate(live):
                A = warm_As[k]
                x0[loffs[li]:loffs[li + 1]] = np.real(A).ravel()
                x0[lntot + loffs[li]:lntot + loffs[li + 1]] = \
                    np.imag(A).ravel()
            starts = [x0, x0 + rng.normal(scale=1e-2, size=2 * lntot)]
            for _ in range(n_extra - 1):
                starts.append(rng.normal(scale=1.0, size=2 * lntot))
            if os.environ.get("IDEG_FD_CHECK") == "1":
                xt = x0 + rng.normal(scale=1e-2, size=2 * lntot)
                l0, g0 = loss_grad(xt, dbar, nrm)
                hstep = 1e-6
                errs = []
                for i in rng.choice(2 * lntot, size=6, replace=False):
                    xp = xt.copy()
                    xp[i] += hstep
                    lp, _ = loss_grad(xp, dbar, nrm)
                    fd = (lp - l0) / hstep
                    errs.append(abs(fd - g0[i]) / max(abs(fd), 1e-12))
                print(f"    FD check ({'sector' if sec_weights else 'global'}"
                      f"-norm): max rel err {max(errs):.2e}", flush=True)
            best, bx = np.inf, None
            for xs in starts:
                r = minimize(loss_grad, xs, args=(dbar, nrm), jac=True,
                             method="L-BFGS-B",
                             options={"maxiter": 300, "ftol": 1e-10})
                if float(r.fun) < best:
                    best, bx = float(r.fun), r.x
            As = unpack(bx)
            Ms = [A @ A.conj().T for A in As]
            sig, _ = normalize(Ms)
            full_sig = [np.zeros((s, s), dtype=complex) for s in sizes]
            for li, k in enumerate(live):
                full_sig[k] = sig[li]
            return best, full_sig

        return search

    def diagnostics(sig_blocks, blocks, basis, sec_of_block, dbar, nrm,
                    full_recheck):
        tr = sum(float(np.trace(s).real) for s in sig_blocks)
        min_eig = min((float(np.min(np.linalg.eigvalsh(s)))
                       if s.shape[0] else 0.0) for s in sig_blocks)
        # sector weights + ||[sigma, N_mag]|| per block
        wq = {}
        cnorm2 = 0.0
        energy = 0.0
        for (a, b), s in zip(blocks, sig_blocks):
            Vb = basis[:, a:b]
            Nb = Vb.conj().T @ (NMAG_COMP[:, None] * Vb)
            comm = s @ Nb - Nb @ s
            cnorm2 += float(np.sum(np.abs(comm) ** 2))
            qv, R = np.linalg.eigh(Nb)
            qi = np.round(qv).astype(int)
            pops = np.real(np.diag(R.conj().T @ s @ R))
            for q, pp in zip(qi, pops):
                wq[int(q)] = wq.get(int(q), 0.0) + float(pp)
        # <H> from block structure: energies constant per E-block
        d = {"trace": tr, "min_block_eig": min_eig,
             "comm_nmag_fro": float(np.sqrt(cnorm2)),
             "sector_weights": {str(q): w for q, w in sorted(wq.items())
                                if w > 1e-12}}
        eener = 0.0
        for kb, ((a, b), s) in enumerate(zip(blocks, sig_blocks)):
            eener += float(np.real(np.trace(s))) * float(E[a])
        d["mean_energy"] = eener
        if full_recheck:
            full = np.zeros((DIM, DIM), dtype=complex)
            for (a, b), s in zip(blocks, sig_blocks):
                Vb = basis[:, a:b]
                full += Vb @ s @ Vb.conj().T
            d["objective_recheck_fullrho"] = miss_of(full, dbar, nrm)
        return d

    search_T1 = make_search(eblocks, CROSS1)
    search_T2 = make_search(sub_blocks, CROSS2)

    slice_env = os.environ.get("IDEG_RUN_SLICE", "")
    lo, hi = ((int(x) for x in slice_env.split(":")) if slice_env
              else (0, 10 ** 9))
    full_recheck = (N <= 10) or os.environ.get("IDEG_FULL_RECHECK") == "1"

    out = {"n_sites": N, "n_eblocks": len(eblocks),
           "n_subblocks": len(sub_blocks),
           "sum_B2_T1": int(sum((b - a) ** 2 for a, b in eblocks)),
           "sum_B2_T2": int(sum((b - a) ** 2 for a, b in sub_blocks)),
           "groups": {}}
    for label in ("TA_ii_quasiperiodic", "TC_integrable"):
        recs = {}
        for ridx, (hh, psi0) in enumerate(build_runs(label)):
            if not (lo <= ridx < hi):
                continue
            states = ev.states_at(psi0, WINDOW)
            dbar = phi_series(states, N).mean(axis=0)
            nrm = float(np.linalg.norm(dbar))
            c1 = V.conj().T @ psi0
            c2 = U2.conj().T @ psi0
            # run's own sector weights
            wrun = {}
            for (a, b), q in zip(sub_blocks, sub_sector):
                wrun[q] = wrun.get(q, 0.0) + float(
                    np.sum(np.abs(c2[a:b]) ** 2))
            wrun = {q: w for q, w in wrun.items() if w > 1e-10}
            # T1: warm = sqrt diagonal-ensemble populations
            warm1 = []
            for (a, b) in eblocks:
                A = np.zeros((b - a, b - a), dtype=complex)
                np.fill_diagonal(A, np.sqrt(np.clip(
                    np.abs(c1[a:b]) ** 2, 1e-12, None)))
                warm1.append(A)
            m1, sig1 = search_T1(dbar, nrm, warm1)
            d1 = diagnostics(sig1, eblocks, V, None, dbar, nrm,
                             full_recheck)
            # T2: warm = P_{E,q} rho0 P_{E,q} (rank-1 columns) + diag fill
            warm2 = []
            for (a, b) in sub_blocks:
                s = b - a
                A = np.zeros((s, s), dtype=complex)
                A[:, 0] = c2[a:b]
                np.fill_diagonal(A, np.diag(A) + 1e-6)
                warm2.append(A)
            m2, sig2 = search_T2(dbar, nrm, warm2)
            d2 = diagnostics(sig2, sub_blocks, U2, sub_sector, dbar, nrm,
                             full_recheck)
            # T3: per-sector pinned to wrun
            search_T3 = make_search(sub_blocks, CROSS2,
                                    sec_of_block=sub_sector,
                                    sec_weights=wrun)
            m3, sig3 = search_T3(dbar, nrm, warm2)
            d3 = diagnostics(sig3, sub_blocks, U2, sub_sector, dbar, nrm,
                             full_recheck)
            recs[ridx] = {
                "run_sector_weights": {str(q): w
                                       for q, w in sorted(wrun.items())},
                "run_mean_energy": float(np.real(psi0.conj()
                                                 @ (hh @ psi0))),
                "T1": {"miss": m1, **d1}, "T2": {"miss": m2, **d2},
                "T3": {"miss": m3, **d3}}
            print(f"[{time.time() - t0:8.1f}s] sector {label} run {ridx} "
                  f"T1={m1:.4f} T2={m2:.4f} T3={m3:.4f} "
                  f"T1_comm_nmag={d1['comm_nmag_fro']:.3f}", flush=True)
        out["groups"][label] = {
            "run_indices": sorted(recs),
            "runs": [recs[k] for k in sorted(recs)]}
        for tier in ("T1", "T2", "T3"):
            vals = [recs[k][tier]["miss"] for k in sorted(recs)]
            if vals:
                out["groups"][label][f"{tier}_median"] = float(
                    np.median(vals))
                out["groups"][label][f"{tier}_n_below"] = int(
                    np.sum(np.array(vals) < EPS_PHI))
    slice_tag = f"_slice{lo}-{hi}" if slice_env else ""
    with open(OUT / f"ar020e_sector_N{N}{slice_tag}.json", "w") as f:
        json.dump(out, f, indent=2)
    print("sector done", flush=True)

else:
    raise ValueError(STAGE)
