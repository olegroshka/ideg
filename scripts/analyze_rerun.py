"""Amendment-4 criterion-(a) re-adjudication on the fresh-seed witness
runs (results/AR-010/confirmatory/rerun_*.json).

Statistic set {pr_A, w2_mean, xi} (spec §8 Amendment 4); thresholds
unchanged (AUC >= 0.95 exact Mann-Whitney, >= 2 statistics per pair,
both criterion sizes, exact-value rule for class (i); TC_localized
aggregated to realization means). Writes
results/AR-010/rerun_summary.json and prints the verdict.
"""

import json
import sys
from itertools import combinations
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from ideg.stats import auc  # noqa: E402

OUT = ROOT / "results" / "AR-010"
CONF = OUT / "confirmatory"
TA = ["TA_i_fixed_point", "TA_ii_quasiperiodic", "TA_iii_chaotic",
      "TA_iv_metastable"]
TC = ["TC_scrambling", "TC_integrable", "TC_localized"]
STATS = ["pr_A", "w2_mean", "xi"]
SIZES = [10, 12]


def vals(g, n, stat):
    d = json.loads((CONF / f"rerun_{g}_N{n}.json").read_text())
    return np.array([float(np.mean([s[stat] for s in run["states"]]))
                     for run in d["runs"]])


def sep(a, b):
    if len(a) == 1 or len(b) == 1:
        exact, ens = (a[0], b) if len(a) == 1 else (b[0], a)
        return {"rule": "exact-value", "exact": float(exact),
                "separates": bool(np.min(ens) > exact
                                  or np.max(ens) < exact)}
    x = auc(a, b)
    return {"rule": "auc", "auc": x, "separates": bool(x >= 0.95)}


summary = {"date": "2026-08-13", "amendment": "spec §8 Amendment 4",
           "manifest": "confirmatory_manifest_addendum2.json",
           "statistics": STATS, "tracks": {}}
for track, groups in [("TA", TA), ("TC", TC)]:
    tout = {}
    for n in SIZES:
        v = {g: {s: vals(g, n, s) for s in STATS} for g in groups}
        pairs = {}
        for ga, gb in combinations(groups, 2):
            per = {s: sep(v[ga][s], v[gb][s]) for s in STATS}
            n_sep = sum(p["separates"] for p in per.values())
            pairs[f"{ga}|{gb}"] = {"stats": per, "n_separating": n_sep,
                                   "pass": bool(n_sep >= 2)}
        tout[str(n)] = {"pairs": pairs,
                        "all_pairs_pass": bool(all(p["pass"]
                                                   for p in pairs.values()))}
    tout["holds"] = bool(all(tout[str(n)]["all_pairs_pass"] for n in SIZES))
    summary["tracks"][track] = tout
summary["criterion_a_holds"] = bool(all(t["holds"]
                                        for t in summary["tracks"].values()))

with open(OUT / "rerun_summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print("Amendment-4 criterion (a) re-adjudication (fresh seeds)")
for track in ("TA", "TC"):
    t = summary["tracks"][track]
    for n in SIZES:
        for pair, p in t[str(n)]["pairs"].items():
            stats_str = {s: (round(x["auc"], 4) if x["rule"] == "auc"
                             else "exact") for s, x in p["stats"].items()}
            print(f"{track} N={n} {pair}: "
                  f"{'PASS' if p['pass'] else 'FAIL'} {stats_str}")
    print(f"{track}: {'HOLDS' if t['holds'] else 'FAILS'}")
print(f"\ncriterion (a) under Amendment 4: "
      f"{'HOLDS' if summary['criterion_a_holds'] else 'FAILS'}")
print(f"written: {OUT / 'rerun_summary.json'}")
