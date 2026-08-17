"""Write the AR-023a environment/provenance freeze (spec §3).

Records the interpreter, the complete installed distribution list, the
content hashes of every frozen input and every produced report, and the
seed enumeration — everything needed to re-run S1/S2 from a clean
checkout and check the numbers.

Deterministic: no timestamps in the frozen record itself.
"""

from __future__ import annotations

from hashlib import sha256
from importlib.metadata import distributions
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
HW = ROOT / "hardware" / "ibm_exp1"
RES = HW / "results"

TRACKED = [
    HW / "manifest" / "hardware_manifest.json",
    HW / "manifest" / "sector_comparator_N10_run0.npz",
    HW / "manifest" / "sector_comparator_N10_run0.json",
    HW / "bundle" / "logical_circuits.qpy",
    HW / "bundle" / "circuit_registry.json",
    HW / "bundle" / "target_states.npz",
    HW / "bundle" / "logical_bundle.json",
    RES / "sim_reference" / "s1_reference.json",
    RES / "sim_reference" / "s1_reference_arrays.npz",
    RES / "sim_common" / "exact_probs_provenance.json",
    RES / "sim_s1_768" / "s1_report.json",
    RES / "sim_s1_896" / "s1_report.json",
    RES / "sim_s2" / "s2_report.json",
]

SCRIPTS = ["experiment.py", "circuits.py", "build_circuits.py",
           "export_sector_comparator.py", "prepare_manifest.py",
           "compute_s1_reference.py", "sampling.py", "run_s1.py",
           "s2lib.py", "run_s2.py", "run_ar023a_chain.py",
           "make_s1s2_figure.py"]


def sha(path: Path) -> str | None:
    return sha256(path.read_bytes()).hexdigest() if path.exists() else None


def main() -> int:
    manifest = json.loads(
        (HW / "manifest" / "hardware_manifest.json").read_text(
            encoding="utf-8"))
    record = {
        "schema_version": 1,
        "stage": "AR-023a S1/S2",
        "python": sys.version.split()[0],
        "packages": {d.metadata["Name"].lower(): d.version
                     for d in sorted(distributions(),
                                     key=lambda x: x.metadata["Name"].lower())
                     if d.metadata.get("Name")},
        "artifact_sha256": {
            str(p.relative_to(ROOT)).replace("\\", "/"): sha(p)
            for p in TRACKED},
        "script_sha256": {
            name: sha(HW / "scripts" / name) for name in SCRIPTS},
        "seeds": manifest["seeds"],
        "s1_execution": manifest.get("s1_execution"),
        "conditions": sorted(
            p.name for p in (RES / "sim_s2" / "conditions").iterdir()
            if p.is_dir()) if (RES / "sim_s2" / "conditions").exists()
        else [],
        "note": "S1/S2 are local simulations; no IBM credential, network "
                "call, or QPU submission occurred at any point.",
    }
    out = RES / "environment_freeze.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print("wrote", out)
    print("packages:", len(record["packages"]),
          "| artifacts:", sum(1 for v in record["artifact_sha256"].values()
                              if v))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
