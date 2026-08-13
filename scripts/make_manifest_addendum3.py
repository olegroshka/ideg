"""Addendum 3: Amendment-5 fresh seeds, n = 40 ensembles (final (a) verdict)."""
import json
import sys
from pathlib import Path

import numpy as np

OUT = Path(__file__).resolve().parent.parent / "results" / "AR-010"
MASTER = 20260815
GROUPS = {"TA_i_fixed_point": 1, "TA_ii_quasiperiodic": 40,
          "TA_iii_chaotic": 40, "TA_iv_metastable": 40,
          "TC_scrambling": 40, "TC_integrable": 40, "TC_localized": 40}
SIZES = [10, 12]

ss = np.random.SeedSequence(MASTER)
seeds = {}
for g, runs in GROUPS.items():
    seeds[g] = {}
    for n in SIZES:
        seeds[g][str(n)] = [int(s.generate_state(1)[0]) for s in ss.spawn(runs)]

addendum = {
    "date_fixed": "2026-08-13",
    "addendum_to": "confirmatory_manifest.json",
    "purpose": "spec 8 Amendment 5: n = 40 ensembles, final criterion-(a) "
               "verdict (stabilizes, cannot rescue; accepted either way per "
               "owner ruling)",
    "statistic_set": ["pr_A", "w2_mean", "xi"],
    "descriptive": ["w2_min"],
    "sizes": SIZES,
    "output_prefix": "rerun40_",
    "rerun_master_seed": MASTER,
    "seeds": seeds,
}
with open(OUT / "confirmatory_manifest_addendum3.json", "w") as f:
    json.dump(addendum, f, indent=2)
print("addendum 3 written")
