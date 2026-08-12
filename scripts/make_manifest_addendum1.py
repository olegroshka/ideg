"""Addendum 1 to the AR-010 confirmatory manifest (2026-08-12).

Measured obstruction: the §1 T-A(ii) incommensurability certificate (no
p/q, q <= 50, within 1e-3 of the magnon gap ratio) is EXHAUSTIVELY
unsatisfiable at N = 8 — 0 of the 56 nondegenerate-gap triples of the
open-chain single-magnon spectrum pass (17/120 pass at N = 10, 27/220 at
N = 12). T-A(ii) therefore cannot be instantiated at N = 8 per the spec's
own preregistered state construction; the manifest's budget-clause size
election (8, 10) is obstructed, and T-A criterion evaluation reverts to
the spec §5.1 PRIMARY sizing (10, 12).

This addendum fixes the T-A N = 12 seeds BEFORE those runs execute. No
preregistered threshold changes. The recorded N = 8 runs for classes
(i)/(iii)/(iv) remain valid (reported descriptively). Dephasing stays
§6.2-bound to N <= 10: T-A dephasing pairs involving class (ii) are
evaluable at N = 10 only and thus CANNOT satisfy the two-size replication
requirement of criterion (b) — recorded as ineligible, not as a null.
"""

import json
import sys
from pathlib import Path

import numpy as np

OUT = Path(__file__).resolve().parent.parent / "results" / "AR-010"
ADDENDUM_MASTER_SEED = 20260813  # distinct from the manifest master seed

GROUPS = {"TA_i_fixed_point": 1, "TA_ii_quasiperiodic": 20,
          "TA_iii_chaotic": 20, "TA_iv_metastable": 20}

ss = np.random.SeedSequence(ADDENDUM_MASTER_SEED)
seeds = {g: {"12": [int(s.generate_state(1)[0]) for s in ss.spawn(r)]}
         for g, r in GROUPS.items()}

addendum = {
    "date_fixed": "2026-08-12",
    "addendum_to": "confirmatory_manifest.json",
    "reason": "T-A(ii) incommensurability certificate exhaustively "
              "unsatisfiable at N = 8 (0/56 triples); spec §5.1 primary "
              "T-A sizing (10, 12) restored (the (8, 10) budget election "
              "is obstructed).",
    "criterion_a_size_pairs_override": {"TA": [10, 12]},
    "criterion_b_size_pairs_override": {"quench": {"TA": [10, 12]},
                                        "loss": {"TA": [10, 12]},
                                        "dephasing": {"TA": [8, 10]}},
    "dephasing_ta_ii_note": "dephasing is spec §6.2-bound to N <= 10; "
                            "T-A pairs involving class (ii) have a single "
                            "evaluable size (10) for the dephasing "
                            "protocol and are INELIGIBLE for criterion-(b) "
                            "two-size replication (recorded, not a null)",
    "n8_runs_status": "recorded N = 8 runs for classes (i)/(iii)/(iv) "
                      "remain valid, reported descriptively",
    "addendum_master_seed": ADDENDUM_MASTER_SEED,
    "seeds": seeds,
}

with open(OUT / "confirmatory_manifest_addendum1.json", "w") as f:
    json.dump(addendum, f, indent=2)
print(f"addendum written: {OUT / 'confirmatory_manifest_addendum1.json'}")
sys.exit(0)
