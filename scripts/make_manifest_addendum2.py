"""Addendum 2 to the AR-010 confirmatory manifest (2026-08-13):
FRESH seeds for the Amendment-4 criterion-(a) re-adjudication.

Witness-only runs (statistic set {PR_A, w2_mean, Xi} per Amendment 4;
min d_phys recorded descriptively; no OTOC, no perturbation protocols).
Sizes: the criterion sizes (10, 12) for all T-A classes and T-C regimes;
ensembles exactly as the main manifest. Commit BEFORE execution.
"""

import json
import sys
from pathlib import Path

import numpy as np

OUT = Path(__file__).resolve().parent.parent / "results" / "AR-010"
RERUN_MASTER_SEED = 20260814

GROUPS = {"TA_i_fixed_point": 1, "TA_ii_quasiperiodic": 20,
          "TA_iii_chaotic": 20, "TA_iv_metastable": 20,
          "TC_scrambling": 20, "TC_integrable": 20, "TC_localized": 20}
SIZES = [10, 12]

ss = np.random.SeedSequence(RERUN_MASTER_SEED)
seeds = {}
for g, runs in GROUPS.items():
    seeds[g] = {}
    for n in SIZES:
        seeds[g][str(n)] = [int(s.generate_state(1)[0])
                            for s in ss.spawn(runs)]

addendum = {
    "date_fixed": "2026-08-13",
    "addendum_to": "confirmatory_manifest.json",
    "purpose": "Amendment 4 criterion-(a) re-adjudication on fresh seeds "
               "(the reformalized statistic set was validated on the "
               "original confirmatory data, so those data are exploratory "
               "for this criterion; these seeds are untouched by the "
               "redesign).",
    "statistic_set": ["pr_A", "w2_mean", "xi"],
    "descriptive": ["w2_min"],
    "excluded": "OTOC (W3 is descriptive-only per Amendment 4 and not "
                "needed for (a)); perturbation protocols and comparators "
                "(criterion (b) and §5.3 are NOT re-adjudicated — their "
                "verdicts stand on the original confirmatory data)",
    "sizes": SIZES,
    "ensembles": "as the main manifest (TA_i single deterministic run; "
                 "TC_localized 20 realizations x 5 states, realization = "
                 "resampling unit)",
    "rerun_master_seed": RERUN_MASTER_SEED,
    "seeds": seeds,
}

with open(OUT / "confirmatory_manifest_addendum2.json", "w") as f:
    json.dump(addendum, f, indent=2)
print(f"addendum 2 written: {OUT / 'confirmatory_manifest_addendum2.json'}")
sys.exit(0)
