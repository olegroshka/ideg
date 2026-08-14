"""AR-020c: UNRESTRICTED stationary-state comparator search
(review response — closes the smooth-f(H) search-space criticism).

    python scripts/ar020c_unrestricted_probe.py <n_sites>

For every manifest run of every class: minimize
    miss(p) = ||Phi[sigma(p)] - Dbar||_F / ||Dbar||_F,
sigma(p) = sum_n p_n |n><n|, over the FULL probability simplex
(p = softmax(theta), theta in R^D unconstrained; D = 2^N parameters)
with an ANALYTIC gradient:
  dS(rho)/dp_n = -tr[R_n (ln rho + 1)]   (rho = sum_n p_n R_n),
  dw_ij/dx_ij = -1/x_ij (zero at the weight floor),
  dD_kl/dw_ij = [edge (i,j) lies on the shortest k->l path]
  (predecessor-tracked Floyd--Warshall; subgradient at ties).
L-BFGS-B, multi-start (best smooth-f(H) solution + uniform + 3 random).
Gradient is verified against finite differences at start-up.

Output: results/AR-010/ar020c_unrestricted_N<n>.json
"""

import json
import sys
import time
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ideg.evolve import EigenEvolver                        # noqa: E402
from ideg.migraph import I0, X_MIN, phi_series              # noqa: E402
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
WINDOW = np.arange(20.0, 200.0 + 1e-9, 0.5)
EPS_PHI = MAN["epsilon_phi"]
PAIRS = [(i, j) for i in range(N) for j in range(i + 1, N)]
NP_ = len(PAIRS)


def eigenstate_rdms(evecs):
    d = evecs.shape[0]
    t_full = np.ascontiguousarray(evecs.T).reshape((d,) + (2,) * N)
    out = []
    for (i, j) in PAIRS:
        t = np.moveaxis(t_full, (1 + i, 1 + j), (1, 2)).reshape(d, 4, -1)
        out.append(np.einsum("nax,nbx->nab", t, t, optimize=True))
    return out  # list of (D, 4, 4) real arrays


def fw_with_pred(w):
    """Floyd-Warshall distances + predecessor matrix."""
    n = w.shape[0]
    d = w.copy()
    np.fill_diagonal(d, 0.0)
    nxt = np.tile(np.arange(n), (n, 1))  # nxt[k,l] = next hop from k to l
    for m in range(n):
        alt = d[:, m:m + 1] + d[m:m + 1, :]
        mask = alt < d - 1e-15
        d = np.where(mask, alt, d)
        nxt = np.where(mask, np.tile(nxt[:, m:m + 1], (1, n)), nxt)
    return d, nxt


def path_edges(nxt, k, l):
    edges = []
    a = k
    guard = 0
    while a != l and guard <= len(nxt):
        b = nxt[a, l]
        edges.append((min(a, b), max(a, b)))
        a = b
        guard += 1
    return edges


def make_objective(rdms, dbar):
    nrm = np.linalg.norm(dbar)
    pair_index = {pq: k for k, pq in enumerate(PAIRS)}

    def loss_grad_p(p):
        # rho_ij, entropies, MI, weights
        mi = np.zeros((N, N))
        w = np.zeros((N, N))
        # per-pair caches for gradient
        pair_cache = []
        for (i, j), r in zip(PAIRS, rdms):
            rho4 = np.tensordot(p, r, axes=1)
            lam4, u4 = np.linalg.eigh(rho4)
            lam4c = np.clip(lam4, 1e-14, None)
            s4 = float(-np.sum(lam4c * np.log(lam4c)))
            rr = rho4.reshape(2, 2, 2, 2)
            rho_a = np.trace(rr, axis1=1, axis2=3)
            rho_b = np.trace(rr, axis1=0, axis2=2)
            la, ua = np.linalg.eigh(rho_a)
            lb, ub = np.linalg.eigh(rho_b)
            lac = np.clip(la, 1e-14, None)
            lbc = np.clip(lb, 1e-14, None)
            sa = float(-np.sum(lac * np.log(lac)))
            sb = float(-np.sum(lbc * np.log(lbc)))
            m = max(sa + sb - s4, 0.0)
            mi[i, j] = mi[j, i] = m
            x = min(max(m / I0, X_MIN), 1.0)
            w[i, j] = w[j, i] = -np.log(x)
            pair_cache.append((lam4c, u4, lac, ua, lbc, ub, m))
        np.fill_diagonal(w, 0.0)
        d, nxt = fw_with_pred(w)
        diff = d - dbar
        loss = float(np.linalg.norm(diff) / nrm)

        # dL/dw_ij via shortest-path edge accumulation
        gw = np.zeros((N, N))
        for k in range(N):
            for l in range(k + 1, N):
                c = 2.0 * diff[k, l] * 2.0  # symmetric matrix double-count
                if c == 0.0:
                    continue
                for (a, b) in path_edges(nxt, k, l):
                    gw[a, b] += c
        # chain: dw/dMI (zero at floor/ceiling), then dMI/dp
        gp = np.zeros(len(p))
        for idx, ((i, j), r) in enumerate(zip(PAIRS, rdms)):
            lam4c, u4, lac, ua, lbc, ub, m = pair_cache[idx]
            x = m / I0
            if gw[i, j] == 0.0 or x <= X_MIN or x >= 1.0:
                continue
            dw_dmi = -1.0 / (x * I0)
            # dS4/dp_n = -tr[R_n (ln rho4 + 1)]
            ln4 = (u4 * np.log(lam4c)[None, :]) @ u4.conj().T
            m4 = -(ln4 + np.eye(4))
            ds4 = np.einsum("nab,ba->n", r, m4, optimize=True)
            # single-site pieces
            lna = (ua * np.log(lac)[None, :]) @ ua.conj().T
            lnb = (ub * np.log(lbc)[None, :]) @ ub.conj().T
            ma = -(lna + np.eye(2))
            mb = -(lnb + np.eye(2))
            r_r = r.reshape(len(p), 2, 2, 2, 2)
            ra = np.trace(r_r, axis1=2, axis2=4)
            rb = np.trace(r_r, axis1=1, axis2=3)
            dsa = np.einsum("nab,ba->n", ra, ma, optimize=True)
            dsb = np.einsum("nab,ba->n", rb, mb, optimize=True)
            dmi = np.real(dsa + dsb - ds4)
            gp += gw[i, j] * dw_dmi * dmi
        # loss = sqrt(L)/nrm; dloss/dp = (1/(2*sqrt(L)*nrm)) * dL/dp
        L = float(np.sum(diff ** 2))
        if L > 0:
            gp = gp / (2.0 * np.sqrt(L) * nrm)
        return loss, gp

    def obj_theta(theta):
        t = theta - theta.max()
        e = np.exp(np.clip(t, -300.0, 0.0))
        p = e / e.sum()
        loss, gp = loss_grad_p(p)
        # softmax chain rule
        gt = p * (gp - float(gp @ p))
        return loss, gt

    return obj_theta, loss_grad_p


def rep_runs(group):
    seeds = MAN["seeds"][group][str(N)]
    for run_idx, seed in enumerate(seeds):
        rng = np.random.default_rng(seed)
        if group == "TA_i_fixed_point":
            h = tfim(N, g=1.5)
            yield "tfim", h, ground_state(h)
        elif group == "TA_ii_quasiperiodic":
            psi, _ = magnon_superposition(N, rng)
            yield "xx", xx_chain(N), psi
        elif group == "TA_iii_chaotic":
            yield "mfi", mixed_field_ising(N), haar_product_state(N, rng)
        elif group == "TA_iv_metastable":
            dg = rng.uniform(-0.01, 0.01, size=N)
            yield f"iv{run_idx}", ferro_ising_weak_tf(N, g=0.05, dg=dg), \
                all_up(N)
        elif group == "TC_scrambling":
            psi = neel(N) if run_idx == 0 else haar_product_state(N, rng)
            yield "mfi", mixed_field_ising(N), psi
        elif group == "TC_integrable":
            psi = neel(N) if run_idx == 0 else haar_product_state(N, rng)
            yield "xx", xx_chain(N), psi
        elif group == "TC_localized":
            yield f"loc{run_idx}", xxz_disordered(N, rng), neel(N)


CACHE = {}


def get(tag, h):
    if tag not in CACHE:
        ev = EigenEvolver(h)
        CACHE[tag] = (ev, eigenstate_rdms(ev.evecs))
        for k in list(CACHE)[:-3]:
            if k not in ("tfim", "xx", "mfi"):
                CACHE.pop(k, None)
    return CACHE[tag]


t0 = time.time()
results = {"date": "2026-08-14", "n_sites": N, "eps_phi": EPS_PHI,
           "method": "unrestricted diagonal populations, softmax + "
                     "analytic gradient, L-BFGS-B, 5 starts", "groups": {}}

# gradient self-check on the first available system
_checked = False
for group in ["TA_i_fixed_point", "TA_ii_quasiperiodic", "TA_iii_chaotic",
              "TA_iv_metastable", "TC_scrambling", "TC_integrable",
              "TC_localized"]:
    recs = []
    for tag, h, psi0 in rep_runs(group):
        ev, rdms = get(tag, h)
        states = ev.states_at(psi0, WINDOW)
        dbar = phi_series(states, N).mean(axis=0)
        obj, loss_grad_p = make_objective(rdms, dbar)

        if not _checked:
            rng = np.random.default_rng(0)
            th = rng.normal(size=len(ev.evals)) * 0.1
            f0, g0 = obj(th)
            fd = np.zeros(5)
            for k in range(5):
                e = np.zeros_like(th)
                e[k] = 1e-6
                fp, _ = obj(th + e)
                fd[k] = (fp - f0) / 1e-6
            err = float(np.max(np.abs(fd - g0[:5])
                               / np.maximum(np.abs(fd), 1e-8)))
            print(f"gradient check rel err: {err:.2e}", flush=True)
            results["gradient_check_rel_err"] = err
            _checked = True

        p_bar = np.abs(ev.coeffs(psi0)) ** 2
        e = ev.evals
        starts = []
        # thermal-ish + uniform + rho_bar-informed + randoms
        starts.append(np.zeros(len(e)))
        starts.append(np.log(np.clip(p_bar, 1e-12, None)))
        b = 1.0 / max(float(e.std()), 1e-9)
        starts.append(-b * (e - e.mean()))
        rng = np.random.default_rng(1234)
        for _ in range(2):
            starts.append(rng.normal(size=len(e)))
        best = np.inf
        for th0 in starts:
            r = minimize(obj, th0, jac=True, method="L-BFGS-B",
                         options={"maxiter": 400, "ftol": 1e-10,
                                  "gtol": 1e-8})
            best = min(best, float(r.fun))
        recs.append(best)
        print(f"[{time.time() - t0:8.1f}s] {group} run {len(recs) - 1} "
              f"unrestricted miss={best:.4f}", flush=True)
    ov = np.array(recs)
    results["groups"][group] = {
        "runs": recs, "min": float(ov.min()), "median": float(np.median(ov)),
        "max": float(ov.max()),
        "n_below_eps_phi": int(np.sum(ov < EPS_PHI)), "n_runs": len(recs),
    }

with open(OUT / f"ar020c_unrestricted_N{N}.json", "w") as f:
    json.dump(results, f, indent=2)
print(f"done ({time.time() - t0:.1f}s)")
for g, v in results["groups"].items():
    print(f"{g}: median {v['median']:.3f} matched "
          f"{v['n_below_eps_phi']}/{v['n_runs']}")
