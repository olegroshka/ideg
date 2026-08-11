"""Fix the AR-010 pilot run manifest (seeds, grids, parameters) BEFORE
execution, per spec §6.2. Deterministic; commit the output, then run pilot."""

import json
import sys
from pathlib import Path

import numpy as np

OUT = Path(__file__).resolve().parent.parent / "results" / "AR-010"
OUT.mkdir(parents=True, exist_ok=True)

MASTER_SEED = 20260811
GROUPS = [
    "TA_i_fixed_point",      # TFIM g=1.5 ground state (doubles as null)
    "TA_ii_quasiperiodic",   # XX 3-magnon incommensurate superpositions
    "TA_iii_chaotic",        # mixed-field Ising, Haar product states
    "TA_iv_metastable",      # ferro Ising g=0.05 + dressings, |all-up>
    "TC_scrambling",         # mixed-field Ising, Neel + random product
    "TC_integrable",         # XX chain, Neel + random product
    "TC_localized",          # XXZ W=8 disorder realizations, Neel
]
RUNS_PER_GROUP = 5

ss = np.random.SeedSequence(MASTER_SEED)
group_seeds = {g: [int(s.generate_state(1)[0]) for s in ss.spawn(RUNS_PER_GROUP)]
               for g in GROUPS}

manifest = {
    "date_fixed": "2026-08-11",
    "spec": "ar/AR-009_spec.md (incl. §8 Amendments 1-2); KB-005 v0.5",
    "phase": "calibration pilot §5.2.1 (EXPLORATORY; excluded from "
             "confirmatory statistics)",
    "n_sites": 10,
    "window": {"t_eq": 20.0, "t_end": 200.0, "dt_sample": 0.5},
    "t_p": 100.0,
    "epsilon_phi": 0.05,
    "delta_floor": 1e-3,
    "lambda_grid": [0.02, 0.05, 0.1, 0.2],
    "gamma_grid": [0.003, 0.01, 0.03],
    "dephasing": {"dt_step": 0.5, "phi_sample_stride_steps": 5,
                  "note": "Trotter split H/dephasing at dt=0.5; Phi sampled "
                          "every 2.5 time units (pilot implementation "
                          "parameter)"},
    "runs_per_group": RUNS_PER_GROUP,
    "master_seed": MASTER_SEED,
    "group_seeds": group_seeds,
    "exclusions": "T-B excluded from pilot (session-log clarification: its "
                  "robustness instrument is the rigidity curve h_sub(eps), "
                  "confirmatory phase); subsystem-loss protocol excluded "
                  "(k = 2 fixed, no calibration dial)",
    "sanity_checks": "results/AR-010/sanity_checks.json — ALL PASS "
                     "(2026-08-11, post-Amendment-2)",
}

with open(OUT / "manifest.json", "w") as f:
    json.dump(manifest, f, indent=2)
print(f"manifest written: {OUT / 'manifest.json'}")
sys.exit(0)
