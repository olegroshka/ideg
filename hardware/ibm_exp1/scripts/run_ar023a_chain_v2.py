"""AR-023a Amendment 2 confirmatory chain (fresh seeds, A2.7).

Stages, appended to results/chain_v2_ledger.log as they complete:
  1. S1 @ 768, R=100, BASE 24002
  2. S1 @ 768 replay -> S1-G4
  3. S1 @ 896, R=100, BASE 24002
  4. S1 @ 896 replay -> S1-G4
All batteries are resumable; re-running this driver continues.
S2 (drift arm included) is driven separately once its caches are built.
"""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
RESULTS = ROOT / "hardware" / "ibm_exp1" / "results"
LEDGER = RESULTS / "chain_v2_ledger.log"
SCRIPTS = Path(__file__).resolve().parent
CACHE = RESULTS / "sim_common_v2" / "exact_probs.npz"
WORKERS = "3"
BASE = "24002"


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


def battery(shots: str, out: Path) -> None:
    if (out / "s1_report.json").exists():
        return
    run([str(SCRIPTS / "run_s1.py"), "--run", "--experiments", "100",
         "--bootstrap", "1000", "--workers", WORKERS, "--shots", shots,
         "--base-seed", BASE, "--cache", str(CACHE), "--out", str(out)],
        f"s1-{shots}-v2-{out.name}")


def compare(primary: Path, replay: Path, tag: str) -> None:
    h1 = sha256(primary.read_bytes()).hexdigest()
    h2 = sha256(replay.read_bytes()).hexdigest()
    meta = primary.parent / "s1_report.meta.json"
    record = json.loads(meta.read_text(encoding="utf-8"))
    record["determinism_replay"] = {
        "identical": h1 == h2, "primary_sha256": h1, "replay_sha256": h2}
    meta.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8")
    log(f"{tag}: byte-identical={h1 == h2} sha={h1[:16]}")


def main() -> int:
    for shots in ("768", "896"):
        primary = RESULTS / f"sim_s1_{shots}_v2"
        replay = RESULTS / f"sim_s1_{shots}_v2_replay"
        battery(shots, primary)
        gates = json.loads((primary / "s1_report.json")
                           .read_text(encoding="utf-8"))["gates"]
        log(f"STAGE S1-{shots}-v2 gates: " + json.dumps(
            {k: v.get("pass") for k, v in gates.items()})
            + f" | G1={gates['S1-G1']['measured']:.5f}"
              f" G2={gates['S1-G2']['measured']}"
              f" G3={gates['S1-G3']['measured']:.5f}")
        battery(shots, replay)
        compare(primary / "s1_report.json", replay / "s1_report.json",
                f"STAGE S1-G4({shots}-v2)")
    log("CHAIN V2 (S1) COMPLETE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
