"""Pre-draft quality sprint: dephasing gamma-grid (the pre-approved
decay-rate-law trigger; descriptive curve upgrading Fig 4 from a point
to a curve). Manifest seeds, first 10 runs/group, N = 10.

    python scripts/quality_sprint_gamma.py

Output: results/AR-010/quality_sprint_gamma.json
"""

import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ideg.evolve import DephasingEvolver, EigenEvolver      # noqa: E402
from ideg.migraph import (delta_phi, mutual_information_matrix,  # noqa: E402
                          phi_distance_matrix, phi_series)
from ideg.models import (ferro_ising_weak_tf,               # noqa: E402
                         mixed_field_ising, xx_chain, xxz_disordered)
from ideg.protocols import log_rho_effect                   # noqa: E402
from ideg.states import (all_up, haar_product_state,        # noqa: E402
                         magnon_superposition, neel)

OUT = ROOT / "results" / "AR-010"
MAN = json.loads((OUT / "confirmatory_manifest.json").read_text())
N = 10
WINDOW = np.arange(20.0, 200.0 + 1e-9, 0.5)
T_P, T_END = 100.0, 200.0
FLOOR = MAN["delta_floor"]
GAMMAS = [0.001, 0.003, 0.01, 0.03, 0.1]
N_RUNS = 10

GROUPS = ["TA_ii_quasiperiodic", "TA_iii_chaotic", "TA_iv_metastable",
          "TC_scrambling", "TC_integrable", "TC_localized"]


def build(group, seed, run_idx):
    rng = np.random.default_rng(seed)
    if group == "TA_ii_quasiperiodic":
        psi, _ = magnon_superposition(N, rng)
        return xx_chain(N), psi
    if group == "TA_iii_chaotic":
        return mixed_field_ising(N), haar_product_state(N, rng)
    if group == "TA_iv_metastable":
        dg = rng.uniform(-0.01, 0.01, size=N)
        return ferro_ising_weak_tf(N, g=0.05, dg=dg), all_up(N)
    if group == "TC_scrambling":
        psi = neel(N) if run_idx == 0 else haar_product_state(N, rng)
        return mixed_field_ising(N), psi
    if group == "TC_integrable":
        psi = neel(N) if run_idx == 0 else haar_product_state(N, rng)
        return xx_chain(N), psi
    if group == "TC_localized":
        return xxz_disordered(N, rng), neel(N)


t0 = time.time()
out = {"date": "2026-08-13", "n_sites": N, "gammas": GAMMAS,
       "runs_per_group": N_RUNS,
       "note": "descriptive gamma-response curves (decay-rate-law "
               "trigger); manifest seeds, first 10 runs/group; "
               "no preregistered verdict touched", "groups": {}}
for group in GROUPS:
    seeds = MAN["seeds"][group]["10"][:N_RUNS]
    per_gamma = {str(g): [] for g in GAMMAS}
    for run_idx, seed in enumerate(seeds):
        h, psi0 = build(group, seed, run_idx)
        ev = EigenEvolver(h)
        states = ev.states_at(psi0, WINDOW)
        delta, dbar = delta_phi(phi_series(states, N))
        max_unpert = float(np.max(delta[WINDOW > T_P]))
        psi_tp = ev.state_at(psi0, T_P)
        for gam in GAMMAS:
            rho = np.outer(psi_tp, psi_tp.conj())
            deph = DephasingEvolver(h, N, gam, dt=0.5)
            mx = 0.0
            for _, r in deph.run(rho, int((T_END - T_P) / 0.5),
                                 sample_every=5):
                d = phi_distance_matrix(
                    mutual_information_matrix(r, N, mixed=True))
                mx = max(mx, float(np.linalg.norm(d - dbar)
                                   / np.linalg.norm(dbar)))
            per_gamma[str(gam)].append(log_rho_effect(mx, max_unpert,
                                                      FLOOR))
        print(f"[{time.time() - t0:7.1f}s] {group} run {run_idx} done",
              flush=True)
    out["groups"][group] = {g: {"mean_log_rho": float(np.mean(v)),
                                "min": float(np.min(v)),
                                "max": float(np.max(v))}
                            for g, v in per_gamma.items()}

with open(OUT / "quality_sprint_gamma.json", "w") as f:
    json.dump(out, f, indent=2)
print(f"done ({time.time() - t0:.1f}s)")
for g, v in out["groups"].items():
    print(g, {k: round(x["mean_log_rho"], 2) for k, x in v.items()})
