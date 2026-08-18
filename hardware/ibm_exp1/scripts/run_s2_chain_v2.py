"""AR-023a Amendment 2 S2 chain (1,372-circuit bundle, drift arm).

Serialized on purpose: the density-matrix preparations and the
batteries are memory-heavy, and concurrent runs have twice triggered
external kills on this workstation.  Everything is resumable, so
re-running the driver continues where it stopped.

Stages, appended to results/chain_s2v2_ledger.log:
  1. prepare any missing condition caches (fakes; sweep/drift assumed)
  2. R=100 battery per condition, drift arm last so its floor can be
     compared against the static conditions already adjudicated
  3. aggregate s2_report.json
"""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
RESULTS = ROOT / "hardware" / "ibm_exp1" / "results"
COND = RESULTS / "sim_s2" / "conditions"
LEDGER = RESULTS / "chain_s2v2_ledger.log"
SCRIPTS = Path(__file__).resolve().parent
WORKERS = "3"


def log(line: str) -> None:
    with LEDGER.open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")
    print(line, flush=True)


def run(args: list[str], tag: str) -> None:
    result = subprocess.run([sys.executable] + args, cwd=ROOT,
                            capture_output=True, text=True)
    if result.returncode != 0:
        log(f"FAILED {tag}: rc={result.returncode} "
            f"out={result.stdout[-400:]!r} err={result.stderr[-400:]!r}")
        raise SystemExit(1)


def main() -> int:
    s2 = str(SCRIPTS / "run_s2.py")

    # ---- stage 1: missing preparations
    fakes = {"fake_a": "fake_fake_aachen", "fake_b": "fake_fake_boston"}
    for only, cond_name in fakes.items():
        if (COND / cond_name / "cache.npz").exists():
            log(f"STAGE1 {only} cache present, skipping prepare")
            continue
        run([s2, "--prepare", "--only", only], f"prepare-{only}")
        log(f"STAGE1 prepared {only}")

    conditions = sorted(p.name for p in COND.iterdir()
                        if p.is_dir() and not p.name.startswith("_"))
    # drift last: adjudicate it against already-measured static floors
    conditions = ([c for c in conditions if c != "drift_ramp"]
                  + [c for c in conditions if c == "drift_ramp"])
    log(f"STAGE1 conditions: {conditions}")

    # ---- stage 2: batteries
    for cond in conditions:
        report = COND / cond / "battery_report.json"
        if not report.exists():
            run([s2, "--run", "--condition", cond, "--experiments", "100",
                 "--bootstrap", "1000", "--workers", WORKERS],
                f"battery-{cond}")
        summary = json.loads(report.read_text(encoding="utf-8"))
        counts = summary["clause_pass_counts"]
        log(f"STAGE2 {cond}: success={summary['success_count']}/100 "
            f"light={summary['traffic_light']} "
            f"delta={summary['delta_median']:.4f} "
            f"floor={summary['floor_median']:.4f} "
            f"c1={counts['1_delta_ci_above_zero']} "
            f"c5={counts['5_no_dominance']}")

    # ---- stage 3: aggregate
    run([s2, "--report"], "s2-report")
    gates = json.loads((RESULTS / "sim_s2" / "s2_report.json")
                       .read_text(encoding="utf-8"))["gates"]
    log("STAGE3 S2 gates: " + json.dumps(
        {k: v.get("pass") for k, v in gates.items()}))
    log("CHAIN S2 V2 COMPLETE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
