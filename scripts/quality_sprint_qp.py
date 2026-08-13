"""Pre-draft quality sprint: quasiperiodic-headline reinforcement
(descriptive; in-script fixed seeds; no preregistered verdict touched).

    python scripts/quality_sprint_qp.py <n_sites>

(a) Ensemble doubling: 20 EXTRA magnon-triple runs (fresh in-script
    seeds) probed for stationary matchability — total quasiperiodic
    evidence becomes 40/size.
(b) Probe stress-test on ALL quasiperiodic runs (manifest + extra):
    K = 24 Chebyshev + 5 extra random Powell starts — can a richer
    smooth-f(H) close the gap?
(c) m-mode scan at m = 3, 4, 5 (10 runs each): does unmatchability
    trend with the number of incommensurate frequencies?
    (m > 3 states drop the pairwise-incommensurability certificate —
    labeled exploratory; construction = equal-weight random distinct
    magnon modes.)

Output: results/AR-010/quality_sprint_qp_N<n>.json
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
from ideg.migraph import (_single_entropies_from_pair,      # noqa: E402
                          _vn_entropy, phi_distance_matrix, phi_series)
from ideg.models import xx_chain                            # noqa: E402
from ideg.states import magnon_superposition                # noqa: E402

OUT = ROOT / "results" / "AR-010"
MAN = json.loads((OUT / "confirmatory_manifest.json").read_text())
ADD1 = json.loads((OUT / "confirmatory_manifest_addendum1.json").read_text())
for g, per in ADD1["seeds"].items():
    MAN["seeds"].setdefault(g, {}).update(per)

N = int(sys.argv[1])
WINDOW = np.arange(20.0, 200.0 + 1e-9, 0.5)
EPS_PHI = MAN["epsilon_phi"]
PAIRS = [(i, j) for i in range(N) for j in range(i + 1, N)]
EXTRA_MASTER = 20260816  # in-script fixed seed, documented


def multi_magnon(n, rng, m):
    """Equal-weight superposition of m random distinct magnon modes
    (m > 3: exploratory construction, no incommensurability filter)."""
    hop = np.zeros((n, n))
    for i in range(n - 1):
        hop[i, i + 1] = hop[i + 1, i] = 1.0
    _, v1 = np.linalg.eigh(hop)
    modes = rng.choice(n, size=m, replace=False)
    psi = np.zeros(2 ** n, dtype=complex)
    for mm in modes:
        ph = np.exp(2.0j * np.pi * rng.random())
        for site in range(n):
            psi[1 << (n - 1 - site)] += ph * v1[site, mm]
    return psi / np.linalg.norm(psi)


ev = EigenEvolver(xx_chain(N))
print("eigh done", flush=True)
t_full = np.ascontiguousarray(ev.evecs.T).reshape((ev.evecs.shape[0],)
                                                  + (2,) * N)
RDMS = []
for (i, j) in PAIRS:
    t = np.moveaxis(t_full, (1 + i, 1 + j), (1, 2)).reshape(
        ev.evecs.shape[0], 4, -1)
    RDMS.append(np.einsum("nax,nbx->nab", t, t, optimize=True))
print("rdms done", flush=True)
e = ev.evals
half = 0.5 * float(e[-1] - e[0])
x = (e - 0.5 * (e[0] + e[-1])) / half


def phi_of(p):
    mi = np.zeros((N, N))
    for (i, j), r in zip(PAIRS, RDMS):
        rho4 = np.tensordot(p, r, axes=1)
        s_i, s_j = _single_entropies_from_pair(rho4)
        mi[i, j] = mi[j, i] = max(s_i + s_j - _vn_entropy(rho4), 0.0)
    return phi_distance_matrix(mi)


def best_miss(psi0, k_cheb, n_rand, rng):
    states = ev.states_at(psi0, WINDOW)
    dbar = phi_series(states, N).mean(axis=0)
    nrm = np.linalg.norm(dbar)

    def miss(p):
        p = np.clip(p, 0.0, None)
        s = p.sum()
        return 10.0 if s <= 0 else float(
            np.linalg.norm(phi_of(p / s) - dbar) / nrm)

    def obj(c):
        lp = np.polynomial.chebyshev.chebval(x, c)
        return miss(np.exp(np.clip(lp - lp.max(), -300.0, 0.0)))

    starts = [np.zeros(k_cheb)]
    for b in (-1.0, 1.0):
        c = np.zeros(k_cheb)
        c[1] = b * half
        starts.append(c)
    for _ in range(n_rand):
        starts.append(rng.normal(scale=1.0, size=k_cheb))
    best = np.inf
    for c0 in starts:
        r = minimize(obj, c0, method="Powell",
                     options={"maxfev": 800, "xtol": 1e-3, "ftol": 1e-4})
        best = min(best, float(r.fun))
    return best


t0 = time.time()
out = {"date": "2026-08-13", "n_sites": N, "eps_phi": EPS_PHI,
       "extra_master_seed": EXTRA_MASTER}

# (a)+(b): manifest runs + 20 extra, stress settings K=24, +5 random starts
ss = np.random.SeedSequence(EXTRA_MASTER)
extra_seeds = [int(s.generate_state(1)[0]) for s in ss.spawn(20)]
res = {"manifest": [], "extra": []}
srng = np.random.default_rng(EXTRA_MASTER + 1)
for label, seeds in [("manifest", MAN["seeds"]["TA_ii_quasiperiodic"]
                      [str(N)]), ("extra", extra_seeds)]:
    for seed in seeds:
        rng = np.random.default_rng(seed)
        psi, _ = magnon_superposition(N, rng)
        m = best_miss(psi, 24, 5, srng)
        res[label].append(m)
        print(f"[{time.time() - t0:7.1f}s] qp {label} seed {seed} "
              f"miss={m:.3f}", flush=True)
allv = res["manifest"] + res["extra"]
out["qp_stress"] = {
    "k_chebyshev": 24, "extra_random_starts": 5,
    "manifest": res["manifest"], "extra": res["extra"],
    "n_runs": len(allv), "min": float(np.min(allv)),
    "median": float(np.median(allv)),
    "n_below_eps_phi": int(sum(v < EPS_PHI for v in allv)),
}

# (c) m-mode scan (exploratory)
mscan = {}
for m in (3, 4, 5):
    vals = []
    rng = np.random.default_rng(EXTRA_MASTER + 100 + m)
    for k in range(10):
        psi = multi_magnon(N, rng, m)
        vals.append(best_miss(psi, 12, 2, srng))
        print(f"[{time.time() - t0:7.1f}s] m={m} run {k} "
              f"miss={vals[-1]:.3f}", flush=True)
    mscan[str(m)] = {"misses": vals, "median": float(np.median(vals)),
                     "min": float(np.min(vals))}
out["m_mode_scan"] = mscan

with open(OUT / f"quality_sprint_qp_N{N}.json", "w") as f:
    json.dump(out, f, indent=2)
print(f"done ({time.time() - t0:.1f}s)")
print("stress:", out["qp_stress"]["n_below_eps_phi"], "/",
      out["qp_stress"]["n_runs"], "matched; median",
      round(out["qp_stress"]["median"], 3))
print("m-scan medians:", {m: round(v["median"], 3)
                          for m, v in mscan.items()})
