"""AR-020b: HARDENED motionless-comparator probe (paper reflection ruling
2026-08-13 — closes the weak-quantifier flag on the class-split claim).

    python scripts/ar020b_hardened_probe.py <n_sites>

Upgrades over ar020_comparator_probe.py:
- FULL ensembles (every manifest run; TC_localized: the Neel primary
  state per realization — scope recorded) at BOTH criterion sizes.
- A GENERAL smooth-f(H) optimization on top of the three natural
  families: stationary sigma = f(H) with log-populations parameterized
  by K = 12 Chebyshev coefficients in the scaled energy, optimized by
  Powell from two starts (uniform; best thermal). Claim wording is
  bound to this scope: "no stationary state that is a smooth function
  of H, within the searched families and parameterization."
- Per-eigenstate pair-RDM precomputation: sigma(p) two-site RDMs are
  population-weighted sums of eigenstate RDMs, so each candidate
  evaluation costs ~ms independent of dimension.

Output: results/AR-010/ar020b_hardened_probe_N<n>.json
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
K_CHEB = 12
PAIRS = [(i, j) for i in range(N) for j in range(i + 1, N)]


def eigenstate_pair_rdms(evecs):
    """R[pair][n] = 4x4 two-site RDM of eigenstate n (real symmetric H)."""
    d = evecs.shape[0]
    out = []
    t_full = np.ascontiguousarray(evecs.T).reshape((d,) + (2,) * N)
    for (i, j) in PAIRS:
        t = np.moveaxis(t_full, (1 + i, 1 + j), (1, 2)).reshape(d, 4, -1)
        out.append(np.einsum("nax,nbx->nab", t, t, optimize=True))
    return out


def phi_of_populations(p, rdms):
    mi = np.zeros((N, N))
    for (i, j), r in zip(PAIRS, rdms):
        rho4 = np.tensordot(p, r, axes=1)
        s_i, s_j = _single_entropies_from_pair(rho4)
        mi[i, j] = mi[j, i] = max(s_i + s_j - _vn_entropy(rho4), 0.0)
    return phi_distance_matrix(mi)


def build_runs(group):
    """Yield (tag, H, psi0) per manifest run. Shared-H groups reuse tag."""
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
            # probe scope: the Neel primary state per realization
            yield f"loc{run_idx}", xxz_disordered(N, rng), neel(N)


CACHE = {}


def get_ev_rdms(tag, h):
    if tag not in CACHE:
        ev = EigenEvolver(h)
        CACHE[tag] = (ev, eigenstate_pair_rdms(ev.evecs))
        if len(CACHE) > 3:  # keep memory bounded; per-run tags never reused
            for k in list(CACHE)[:-3]:
                if k not in ("tfim", "xx", "mfi"):
                    CACHE.pop(k, None)
    return CACHE[tag]


def probe_run(ev, rdms, psi0):
    states = ev.states_at(psi0, WINDOW)
    dbar = phi_series(states, N).mean(axis=0)
    nrm = np.linalg.norm(dbar)
    e = ev.evals
    p_bar = np.abs(ev.coeffs(psi0)) ** 2
    half = 0.5 * float(e[-1] - e[0])
    x = (e - 0.5 * (e[0] + e[-1])) / max(half, 1e-12)

    def miss(p):
        p = np.clip(p, 0.0, None)
        s = p.sum()
        if s <= 0:
            return 10.0
        return float(np.linalg.norm(phi_of_populations(p / s, rdms) - dbar)
                     / nrm)

    rec = {}
    # families
    betas = np.concatenate([-np.geomspace(5.0, 0.01, 10), [0.0],
                            np.geomspace(0.01, 5.0, 10)])
    th = [(miss(np.exp(-b * (e - e.mean()))), b) for b in betas]
    rec["thermal"] = float(min(th)[0])
    beta_best = min(th)[1]
    lams = np.linspace(0.0, 1.0, 11)
    rec["depolarized_rho_bar"] = float(min(
        miss((1 - lam) * p_bar + lam / len(e)) for lam in lams))
    e_mean = float(p_bar @ e)
    span = 2 * half
    mc = [miss(np.exp(-((e - e0) ** 2) / (2 * s ** 2)))
          for e0 in np.linspace(e_mean - 0.3 * span, e_mean + 0.3 * span, 7)
          for s in np.geomspace(0.01 * span, 0.5 * span, 6)]
    rec["microcanonical"] = float(np.min(mc))

    # general smooth f(H): log p = chebval(x, c)
    def obj(c):
        lp = np.polynomial.chebyshev.chebval(x, c)
        return miss(np.exp(np.clip(lp - lp.max(), -300.0, 0.0)))

    starts = [np.zeros(K_CHEB)]
    c_th = np.zeros(K_CHEB)
    c_th[1] = -beta_best * half
    starts.append(c_th)
    best = np.inf
    for c0 in starts:
        r = minimize(obj, c0, method="Powell",
                     options={"maxfev": 600, "xtol": 1e-3, "ftol": 1e-4})
        best = min(best, float(r.fun))
    rec["smooth_fH_chebyshev"] = best
    rec["overall_min"] = float(min(rec.values()))
    return rec


results = {"date": "2026-08-13", "n_sites": N, "eps_phi": EPS_PHI,
           "k_chebyshev": K_CHEB,
           "probe_scope": "full manifest ensembles; TC_localized = Neel "
                          "primary per realization; families + smooth-f(H) "
                          "Chebyshev-Powell (2 starts, maxfev 600)",
           "groups": {}}
t0 = time.time()
for group in ["TA_i_fixed_point", "TA_ii_quasiperiodic", "TA_iii_chaotic",
              "TA_iv_metastable", "TC_scrambling", "TC_integrable",
              "TC_localized"]:
    recs = []
    for tag, h, psi0 in build_runs(group):
        ev, rdms = get_ev_rdms(tag, h)
        recs.append(probe_run(ev, rdms, psi0))
        print(f"[{time.time() - t0:8.1f}s] {group} N={N} run "
              f"{len(recs) - 1} overall={recs[-1]['overall_min']:.3f}",
              flush=True)
    ov = [r["overall_min"] for r in recs]
    results["groups"][group] = {
        "runs": recs,
        "overall_min_min": float(np.min(ov)),
        "overall_min_median": float(np.median(ov)),
        "overall_min_max": float(np.max(ov)),
        "n_below_eps_phi": int(sum(v < EPS_PHI for v in ov)),
        "n_runs": len(ov),
    }

with open(OUT / f"ar020b_hardened_probe_N{N}.json", "w") as f:
    json.dump(results, f, indent=2)
print(f"done ({time.time() - t0:.1f}s)")
for g, v in results["groups"].items():
    print(f"{g}: median {v['overall_min_median']:.3f} "
          f"[{v['overall_min_min']:.3f}, {v['overall_min_max']:.3f}] "
          f"matched {v['n_below_eps_phi']}/{v['n_runs']}")
