"""Re-validate S1 and S2 under the unified analysis implementation.

AR-023 §12 B7 requires the QPU analysis path to be the same one the
simulations validated.  The S1/S2 unification (scripts/analysis.py)
changed the implementation after validation, so every battery is re-run
against it.  The change is numerically equivalent (max relative
difference 1.97e-14, zero clause differences) but "equivalent" is not
"the same code", and B7 asks for the same code.

Runs batteries with bounded concurrency; every battery is resumable, so
an interrupted run costs at most the in-flight experiments.
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
RESULTS = ROOT / "hardware" / "ibm_exp1" / "results"
COND = RESULTS / "sim_s2" / "conditions"
SCRIPTS = Path(__file__).resolve().parent
LEDGER = RESULTS / "revalidation_ledger.log"
CACHE = RESULTS / "sim_common_v2" / "exact_probs.npz"
BASE = "24002"
CONCURRENT = 4        # batteries in flight
WORKERS = "2"         # pool workers per battery


def log(line: str) -> None:
    with LEDGER.open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")
    print(line, flush=True)


def s1_battery(shots: str, out: Path) -> str:
    if not (out / "s1_report.json").exists():
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "run_s1.py"), "--run",
             "--experiments", "100", "--bootstrap", "1000",
             "--workers", WORKERS, "--shots", shots, "--base-seed", BASE,
             "--cache", str(CACHE), "--out", str(out)],
            cwd=ROOT, capture_output=True, text=True)
        if result.returncode != 0:
            return f"FAILED s1-{out.name}: {result.stderr[-300:]!r}"
    gates = json.loads((out / "s1_report.json")
                       .read_text(encoding="utf-8"))["gates"]
    return (f"S1 {out.name}: " + json.dumps(
        {k: v.get("pass") for k, v in gates.items()})
        + f" G1={gates['S1-G1']['measured']:.5f}"
          f" G2={gates['S1-G2']['measured']}"
          f" G3={gates['S1-G3']['measured']:.5f}")


def s2_battery(cond: str) -> str:
    report = COND / cond / "battery_report.json"
    if not report.exists():
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "run_s2.py"), "--run",
             "--condition", cond, "--experiments", "100",
             "--bootstrap", "1000", "--workers", WORKERS],
            cwd=ROOT, capture_output=True, text=True)
        if result.returncode != 0:
            return f"FAILED s2-{cond}: {result.stderr[-300:]!r}"
    b = json.loads(report.read_text(encoding="utf-8"))
    return (f"S2 {cond}: success={b['success_count']}/100 "
            f"floor={b['floor_median']:.4f} delta={b['delta_median']:.4f}")


def main() -> int:
    # Clear prior results ONCE, so nothing pre-refactor survives in the
    # record.  Guarded by a marker: re-running this driver to resume
    # after a failure must NOT destroy batteries already completed
    # under the unified implementation.
    marker = RESULTS / ".unified_revalidation_cleared"
    if marker.exists():
        log("clear step already done; resuming without deleting")
        return _run_jobs()
    stale = []
    for shots in ("768", "896"):
        for suffix in ("", "_replay"):
            stale.append(RESULTS / f"sim_s1_{shots}_v2{suffix}")
    for path in stale:
        if (path / "s1_report.json").exists():
            (path / "s1_report.json").unlink()
        for old in (path / "experiments").glob("*.json"):
            old.unlink()
    for cond_dir in COND.iterdir():
        if cond_dir.is_dir() and not cond_dir.name.startswith("_"):
            report = cond_dir / "battery_report.json"
            if report.exists():
                report.unlink()
            for old in (cond_dir / "experiments").glob("*.json"):
                old.unlink()
    marker.write_text("cleared pre-refactor batteries\n", encoding="utf-8")
    log("cleared pre-refactor batteries")
    return _run_jobs()


def _run_jobs() -> int:
    jobs = []
    for shots in ("768", "896"):
        jobs.append(("s1", shots, RESULTS / f"sim_s1_{shots}_v2"))
        jobs.append(("s1", shots, RESULTS / f"sim_s1_{shots}_v2_replay"))
    conditions = sorted(p.name for p in COND.iterdir()
                        if p.is_dir() and not p.name.startswith("_"))
    for cond in conditions:
        jobs.append(("s2", cond, None))

    def dispatch(job):
        kind, arg, out = job
        return s1_battery(arg, out) if kind == "s1" else s2_battery(arg)

    with ThreadPoolExecutor(max_workers=CONCURRENT) as pool:
        for line in pool.map(dispatch, jobs):
            log(line)

    # determinism: primary vs replay under the unified code
    for shots in ("768", "896"):
        primary = RESULTS / f"sim_s1_{shots}_v2" / "s1_report.json"
        replay = RESULTS / f"sim_s1_{shots}_v2_replay" / "s1_report.json"
        if primary.exists() and replay.exists():
            h1 = sha256(primary.read_bytes()).hexdigest()
            h2 = sha256(replay.read_bytes()).hexdigest()
            log(f"S1-G4({shots}): byte-identical={h1 == h2} {h1[:16]}")

    subprocess.run([sys.executable, str(SCRIPTS / "run_s2.py"),
                    "--report"], cwd=ROOT, capture_output=True, text=True)
    gates = json.loads((RESULTS / "sim_s2" / "s2_report.json")
                       .read_text(encoding="utf-8"))["gates"]
    log("S2 gates: " + json.dumps(
        {k: v.get("pass") for k, v in gates.items()}))
    log("REVALIDATION COMPLETE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
