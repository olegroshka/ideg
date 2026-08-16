"""Sequential AR-023a completion chain (detached driver).

Stages, each appended to results/chain_ledger.log as it completes:
  1. S1-G4 replay at 768 shots into a fresh directory + byte compare
  2. A1.1 escalation battery at 896 shots
  3. 896-shot replay + byte compare
  4. All 11 S2 condition batteries (resumable)
  5. s2_report.json aggregation

Every stage runs in a subprocess under the same interpreter; batteries
are resumable, so re-running this driver continues where it stopped.
"""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
RESULTS = ROOT / "hardware" / "ibm_exp1" / "results"
LEDGER = RESULTS / "chain_ledger.log"
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
            f"tail={result.stdout[-300:]!r} err={result.stderr[-300:]!r}")
        raise SystemExit(1)


def file_hash(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def compare_reports(primary: Path, replay: Path, tag: str) -> bool:
    h1, h2 = file_hash(primary), file_hash(replay)
    identical = h1 == h2
    meta_path = primary.parent / (primary.stem + ".meta.json")
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    meta["determinism_replay"] = {
        "identical": identical,
        "primary_sha256": h1,
        "replay_sha256": h2,
        "replay_dir": str(replay.parent.name),
    }
    meta_path.write_text(json.dumps(meta, indent=2, sort_keys=True) + "\n",
                         encoding="utf-8")
    log(f"{tag}: byte-identical={identical} sha={h1[:16]}")
    return identical


def main() -> int:
    s1 = SCRIPTS / "run_s1.py"
    s2 = SCRIPTS / "run_s2.py"

    # Stage 1 — S1-G4 replay at 768 shots
    if not (RESULTS / "sim_s1_768_replay" / "s1_report.json").exists():
        run([str(s1), "--run", "--experiments", "100", "--bootstrap",
             "1000", "--workers", WORKERS, "--shots", "768", "--out",
             str(RESULTS / "sim_s1_768_replay")], "s1-768-replay")
    compare_reports(RESULTS / "sim_s1_768" / "s1_report.json",
                    RESULTS / "sim_s1_768_replay" / "s1_report.json",
                    "STAGE1 S1-G4(768)")

    # Stage 2 — A1.1 escalation battery at 896 shots
    if not (RESULTS / "sim_s1_896" / "s1_report.json").exists():
        run([str(s1), "--run", "--experiments", "100", "--bootstrap",
             "1000", "--workers", WORKERS, "--shots", "896", "--out",
             str(RESULTS / "sim_s1_896")], "s1-896")
    gates = json.loads((RESULTS / "sim_s1_896" / "s1_report.json")
                       .read_text(encoding="utf-8"))["gates"]
    log("STAGE2 896 gates: " + json.dumps({
        k: v.get("pass") for k, v in gates.items()}))

    # Stage 3 — 896 replay
    if not (RESULTS / "sim_s1_896_replay" / "s1_report.json").exists():
        run([str(s1), "--run", "--experiments", "100", "--bootstrap",
             "1000", "--workers", WORKERS, "--shots", "896", "--out",
             str(RESULTS / "sim_s1_896_replay")], "s1-896-replay")
    compare_reports(RESULTS / "sim_s1_896" / "s1_report.json",
                    RESULTS / "sim_s1_896_replay" / "s1_report.json",
                    "STAGE3 S1-G4(896)")

    # Stage 4 — S2 condition batteries
    conditions = [
        "fake_fake_aachen", "fake_fake_boston",
        "grid_p2-0.003_ro-0.01", "grid_p2-0.003_ro-0.02",
        "grid_p2-0.003_ro-0.03", "grid_p2-0.006_ro-0.01",
        "grid_p2-0.006_ro-0.02", "grid_p2-0.006_ro-0.03",
        "grid_p2-0.01_ro-0.01", "grid_p2-0.01_ro-0.02",
        "grid_p2-0.01_ro-0.03",
    ]
    for cond in conditions:
        report = (RESULTS / "sim_s2" / "conditions" / cond
                  / "battery_report.json")
        if not report.exists():
            run([str(s2), "--run", "--condition", cond, "--experiments",
                 "100", "--bootstrap", "1000", "--workers", WORKERS],
                f"s2-{cond}")
        summary = json.loads(report.read_text(encoding="utf-8"))
        log(f"STAGE4 {cond}: success={summary['success_count']}/100 "
            f"light={summary['traffic_light']} "
            f"delta={summary['delta_median']:.4f}")

    # Stage 5 — aggregate report
    run([str(s2), "--report"], "s2-report")
    gates = json.loads((RESULTS / "sim_s2" / "s2_report.json")
                       .read_text(encoding="utf-8"))["gates"]
    log("STAGE5 S2 gates: " + json.dumps({
        k: v.get("pass") for k, v in gates.items()}))
    log("CHAIN COMPLETE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
