"""Aggregate AR-010 pilot results -> calibration summary.

Produces per-(group, protocol, strength): mean log_rho, mean R, stationarity
failures; plus the exploratory failure thresholds lambda*/gamma* per group
and a recommended confirmatory (lambda, gamma) per the §5.2.1 criterion:
strengths placing typical |log_rho| in a responsive, non-saturated range
(target band preregistered here as 0.5 <= mean log_rho <= 3.0 across
dynamical groups, chosen before seeing results only in the sense of the
band's definition; the band itself is an analysis convention recorded in
the session log)."""

import json
import sys
from pathlib import Path

import numpy as np

OUT = Path(__file__).resolve().parent.parent / "results" / "AR-010"
MAN = json.loads((OUT / "manifest.json").read_text())

groups = {}
for f in sorted(OUT.glob("pilot_T*.json")):
    data = json.loads(f.read_text())
    groups.update(data["groups"])

if not groups:
    print("no pilot results found")
    sys.exit(1)

LAM = [str(x) for x in MAN["lambda_grid"]]
GAM = [str(x) for x in MAN["gamma_grid"]]
EPS = MAN["epsilon_phi"]

summary = {"per_group": {}, "_groups_present": sorted(groups)}
for g, runs in groups.items():
    entry = {"n_runs": len(runs),
             "baseline_max_delta_phi": [r["baseline"]["max_delta_phi"]
                                        for r in runs],
             "baseline_stationary": sum(r["baseline"]["stationary"]
                                        for r in runs),
             "pr_A": [round(r["baseline"]["pr_A"], 2) for r in runs],
             "xi": [round(r["baseline"]["xi"], 4) for r in runs],
             "quench": {}, "dephasing": {}}
    for lam in LAM:
        lr = [r["quench"][lam]["log_rho"] for r in runs]
        rr = [r["quench"][lam]["retention_R"] for r in runs]
        fails = sum(r["quench"][lam]["fails_stationarity"] for r in runs)
        entry["quench"][lam] = {"mean_log_rho": float(np.mean(lr)),
                                "sd_log_rho": float(np.std(lr)),
                                "mean_R": float(np.mean(rr)),
                                "fails": int(fails)}
    for gam in GAM:
        lr = [r["dephasing"][gam]["log_rho"] for r in runs]
        rr = [r["dephasing"][gam]["retention_R"] for r in runs]
        fails = sum(r["dephasing"][gam]["fails_stationarity"] for r in runs)
        entry["dephasing"][gam] = {"mean_log_rho": float(np.mean(lr)),
                                   "sd_log_rho": float(np.std(lr)),
                                   "mean_R": float(np.mean(rr)),
                                   "fails": int(fails)}
    # exploratory failure thresholds (smallest grid strength failing eps_phi
    # in a majority of runs)
    def _star(proto, grid):
        for s in grid:
            fails = sum(r[proto][s]["fails_stationarity"] for r in runs)
            if fails > len(runs) / 2:
                return s
        return None
    entry["lambda_star"] = _star("quench", LAM)
    entry["gamma_star"] = _star("dephasing", GAM)
    summary["per_group"][g] = entry

# recommendation: strength whose across-dynamical-group mean |log_rho| lies
# in the responsive band [0.5, 3.0] with zero groups saturated at the floor
DYNAMICAL = [g for g in groups if g != "TA_i_fixed_point"]
BAND = (0.5, 3.0)


def recommend(proto, grid):
    scored = []
    for s in grid:
        means = [summary["per_group"][g][proto][s]["mean_log_rho"]
                 for g in DYNAMICAL]
        in_band = sum(BAND[0] <= abs(m) <= BAND[1] for m in means)
        spread = float(np.std(means))
        scored.append((in_band, spread, s, [round(m, 2) for m in means]))
    scored.sort(key=lambda x: (-x[0], -x[1]))
    return {"choice": scored[0][2], "in_band_groups": scored[0][0],
            "across_group_sd": scored[0][1],
            "all": {s: m for _, _, s, m in scored}}


if len(groups) == len(MAN["group_seeds"]):
    summary["recommendation"] = {
        "band": BAND,
        "lambda": recommend("quench", LAM),
        "gamma": recommend("dephasing", GAM),
        "note": "spread is a tiebreak TOWARD class discrimination; final "
                "choice is the owner-logged §8 entry, not this script",
    }

with open(OUT / "pilot_summary.json", "w") as f:
    json.dump(summary, f, indent=2)
print(json.dumps(summary.get("recommendation",
                             {"status": f"{len(groups)}/7 groups done"}),
                 indent=2))
print("\nper-group calibration table:")
for g, e in summary["per_group"].items():
    print(f"\n{g}  (baseline stationary {e['baseline_stationary']}"
          f"/{e['n_runs']}, PR_A~{np.median(e['pr_A']):.3g}, "
          f"Xi~{np.median(e['xi']):.3g})")
    for proto, grid in (("quench", LAM), ("dephasing", GAM)):
        row = "  ".join(
            f"{s}: lr={e[proto][s]['mean_log_rho']:+.2f} "
            f"R={e[proto][s]['mean_R']:.2f} f={e[proto][s]['fails']}"
            for s in grid)
        print(f"  {proto:10s} {row}")
