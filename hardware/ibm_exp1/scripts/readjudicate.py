"""Re-adjudicate a committed battery under a named rule variant.

Adjudication is separated from data generation on purpose: every
per-experiment record stores each diagnostic quantity, so a change to a
DECISION RULE never requires re-running the simulation.  This is what
makes the AR-020 dual-record discipline cheap — the same data can be
adjudicated under the original and the amended rule, and both recorded.

Rule variants:
  a2-max     AR-023a A2.3 as first written: per-experiment MAXIMUM
             per-RDM ||rho_proj - rho_raw||_F < 0.05
  a2-median  A2.10 (owner ruling 2026-08-17): per-experiment MEDIAN
             per-RDM correction < 0.05, restoring the statistic the
             0.05 threshold was originally calibrated against; the
             maximum is still reported as a diagnostic

Never modifies s1_report.json; writes adjudication_<variant>.json.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
VARIANTS = ("a2-max", "a2-median")


def clause_five(record: dict, variant: str) -> bool:
    """Clause 5 under the named variant."""
    within = (record["loto_lopo_excess_max"]
              <= record["clause_5a_tolerance"])
    no_flip = not record["loto_lopo_sign_flip"]
    if variant == "a2-max":
        projection = record["proj_fro_max_main"] < 0.05
    elif variant == "a2-median":
        projection = record["proj_fro_median_main"] < 0.05
    else:
        raise ValueError(f"unknown variant {variant}")
    return bool(within and no_flip and projection)


def adjudicate(battery_dir: Path, variant: str, eps_ref: float) -> dict:
    records = [json.loads(p.read_text(encoding="utf-8"))
               for p in sorted((battery_dir / "experiments").glob("*.json"))]
    if not records:
        raise RuntimeError(f"no experiment records in {battery_dir}")

    rows = []
    for record in records:
        clauses = dict(record["clauses"])
        clauses["5_no_dominance"] = clause_five(record, variant)
        rows.append({
            "experiment": record["experiment"],
            "clauses": clauses,
            "success_rule": all(clauses.values()),
        })

    eps = np.array([r["eps_main"] for r in records])
    floors = np.array([r["eps_floor_experiment"] for r in records])
    successes = int(sum(row["success_rule"] for row in rows))
    g1 = float(abs(np.median(eps) - eps_ref))
    g3 = float(np.median(floors))
    proj_max = np.array([r["proj_fro_max_main"] for r in records])
    proj_med = np.array([r["proj_fro_median_main"] for r in records])

    return {
        "schema_version": 1,
        "battery": battery_dir.name,
        "variant": variant,
        "n_experiments": len(records),
        "gates": {
            "S1-G1": {"measured": g1, "threshold": 0.02,
                      "pass": bool(g1 < 0.02)},
            "S1-G2": {"measured": successes, "threshold": 95,
                      "pass": bool(successes >= 95)},
            "S1-G3": {"measured": g3, "threshold": 0.05,
                      "pass": bool(g3 < 0.05)},
        },
        "clause_pass_counts": {
            key: int(sum(row["clauses"][key] for row in rows))
            for key in rows[0]["clauses"]},
        "projection_diagnostics": {
            "max_statistic_worst": float(proj_max.max()),
            "max_statistic_margin_to_threshold": float(0.05 - proj_max.max()),
            "median_statistic_worst": float(proj_med.max()),
            "median_statistic_headroom_factor": float(
                0.05 / max(proj_med.max(), 1e-12)),
        },
        "eps_median": float(np.median(eps)),
        "eps_reference": eps_ref,
        "floor_median": g3,
        "experiments": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--battery", type=Path, required=True)
    parser.add_argument("--variant", choices=VARIANTS, required=True)
    parser.add_argument("--all-variants", action="store_true",
                        help="write an adjudication for every variant")
    args = parser.parse_args()

    manifest = json.loads(
        (ROOT / "hardware" / "ibm_exp1" / "manifest"
         / "hardware_manifest.json").read_text(encoding="utf-8"))
    eps_ref = float(manifest["s1_reference"]["eps_sector_37"])

    variants = VARIANTS if args.all_variants else (args.variant,)
    for variant in variants:
        record = adjudicate(args.battery, variant, eps_ref)
        out = args.battery / f"adjudication_{variant}.json"
        out.write_text(json.dumps(record, indent=1, sort_keys=True) + "\n",
                       encoding="utf-8")
        gates = {k: v["pass"] for k, v in record["gates"].items()}
        print(f'{args.battery.name} [{variant}]: {gates} '
              f'G2={record["gates"]["S1-G2"]["measured"]}/'
              f'{record["n_experiments"]} -> {out.name}')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
