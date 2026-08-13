"""AR-020: can ANY natural stationary state match a run's mean geometry?

For one representative run per class (N = 10, manifest seed 0), minimize
||Phi[sigma] - Dbar||_F / ||Dbar||_F over three stationary families
([H, sigma] = 0 by construction):
  (a) thermal            sigma ∝ exp(-beta H), beta grid (incl. beta<0)
  (b) depolarized-rho̅    sigma = (1-lam) rho_bar + lam I/D, lam grid
  (c) microcanonical     populations ∝ exp(-(E-E0)^2 / 2 s^2), (E0, s) grid
Evidence question (AR-011 -> AR-020 requirement): if every family misses
by >> eps_Phi, "no natural stationary state holds the running geometry" —
sharpening sustained-by. Output: results/AR-010/ar020_comparator_probe.json
"""

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ideg.evolve import EigenEvolver                        # noqa: E402
from ideg.migraph import (mutual_information_matrix,        # noqa: E402
                          phi_distance_matrix, phi_series)
from ideg.models import (ferro_ising_weak_tf,               # noqa: E402
                         mixed_field_ising, xx_chain, xxz_disordered)
from ideg.protocols import diagonal_ensemble                # noqa: E402
from ideg.states import (all_up, haar_product_state,        # noqa: E402
                         magnon_superposition, neel)

OUT = ROOT / "results" / "AR-010"
MAN = json.loads((OUT / "confirmatory_manifest.json").read_text())
N = 10
WINDOW = np.arange(20.0, 200.0 + 1e-9, 0.5)


def rep_run(group):
    seed = MAN["seeds"][group]["10"][0]
    rng = np.random.default_rng(seed)
    if group == "TA_ii_quasiperiodic":
        psi, _ = magnon_superposition(N, rng)
        return xx_chain(N), psi
    if group == "TA_iii_chaotic":
        return mixed_field_ising(N), haar_product_state(N, rng)
    if group == "TA_iv_metastable":
        dg = rng.uniform(-0.01, 0.01, size=N)
        return ferro_ising_weak_tf(N, g=0.05, dg=dg), all_up(N)
    if group == "TC_localized":
        return xxz_disordered(N, rng), neel(N)
    raise ValueError(group)


def phi_of_diag(ev, p):
    sig = (ev.evecs * p[None, :]) @ ev.evecs.conj().T
    return phi_distance_matrix(mutual_information_matrix(sig, N, mixed=True))


results = {"date": "2026-08-13", "n_sites": N, "eps_phi": 0.25,
           "groups": {}}
for group in ["TA_ii_quasiperiodic", "TA_iii_chaotic", "TA_iv_metastable",
              "TC_localized"]:
    h, psi0 = rep_run(group)
    ev = EigenEvolver(h)
    states = ev.states_at(psi0, WINDOW)
    dbar = phi_series(states, N).mean(axis=0)
    nrm = np.linalg.norm(dbar)
    e = ev.evals
    p_bar = np.abs(ev.coeffs(psi0)) ** 2
    e_mean = float(p_bar @ e)

    def miss(p):
        p = np.clip(p, 0.0, None)
        p = p / p.sum()
        return float(np.linalg.norm(phi_of_diag(ev, p) - dbar) / nrm)

    best = {}
    # (a) thermal, beta grid incl. negative temperatures
    betas = np.concatenate([-np.geomspace(5.0, 0.01, 12), [0.0],
                            np.geomspace(0.01, 5.0, 12)])
    vals = []
    for b in betas:
        w = np.exp(-b * (e - e.mean()))
        vals.append(miss(w))
    best["thermal"] = {"min_miss": float(np.min(vals)),
                       "beta": float(betas[int(np.argmin(vals))])}
    # (b) depolarized diagonal ensemble
    lams = np.linspace(0.0, 1.0, 21)
    vals = [miss((1 - lam) * p_bar + lam / len(e)) for lam in lams]
    best["depolarized_rho_bar"] = {"min_miss": float(np.min(vals)),
                                   "lambda": float(lams[int(np.argmin(vals))])}
    # (c) Gaussian microcanonical around scanned E0
    span = float(e[-1] - e[0])
    e0s = np.linspace(e_mean - 0.3 * span, e_mean + 0.3 * span, 9)
    sigmas = np.geomspace(0.01 * span, 0.5 * span, 8)
    vals, args = [], []
    for e0 in e0s:
        for s in sigmas:
            w = np.exp(-((e - e0) ** 2) / (2 * s ** 2))
            if w.sum() < 1e-300:
                continue
            vals.append(miss(w))
            args.append((float(e0), float(s)))
    k = int(np.argmin(vals))
    best["microcanonical"] = {"min_miss": float(vals[k]),
                              "E0": args[k][0], "sigma_E": args[k][1]}

    rho_bar_miss = float(np.linalg.norm(
        phi_of_diag(ev, p_bar) - dbar) / nrm)
    results["groups"][group] = {
        "rho_bar_miss": rho_bar_miss,
        "families": best,
        "overall_min_miss": float(min(v["min_miss"] for v in best.values())),
    }
    print(f"{group}: rho_bar {rho_bar_miss:.3f} | " +
          " ".join(f"{k} {v['min_miss']:.3f}" for k, v in best.items()),
          flush=True)

with open(OUT / "ar020_comparator_probe.json", "w") as f:
    json.dump(results, f, indent=2)
print("done")
