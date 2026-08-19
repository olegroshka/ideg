"""L4 — compile the frozen bundle onto the selected path and estimate usage.

Transpiles all 1,372 logical circuits to the frozen backend/path at
optimization level 3 with seed_transpiler=1701, then checks the AR-023
§7 compilation gates:

  * no SWAP introduced anywhere;
  * only the ten intended physical qubits are touched;
  * every circuit fully bound;
  * two-qubit count, depth and duration recorded.

Usage is then estimated from the COMPILED circuit durations plus the
backend's reset/repetition delay — which is what actually consumes QPU
time — rather than from AR-023 §8's rough per-execution formula.  Both
numbers are reported side by side so the rough formula's error is
visible rather than assumed.

Read-only with respect to the QPU: nothing is submitted, no job object
is sent.  `QPU-GO` is not in this script's vocabulary.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
SCRIPTS = Path(__file__).resolve().parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from select_backend_path import service  # noqa: E402

ROUGH_PER_EXECUTION = 0.00035     # AR-023 §8 rough formula
ROUGH_OVERHEAD = 2.0
M3_CAL_CIRCUITS = 20              # mthree balanced calibration


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--shots", type=int, default=None,
                        help="defaults to the manifest value")
    parser.add_argument(
        "--out", type=Path,
        default=ROOT / "hardware" / "ibm_exp1" / "results" / "l4")
    args = parser.parse_args()

    manifest = json.loads(
        (ROOT / "hardware" / "ibm_exp1" / "manifest"
         / "hardware_manifest.json").read_text(encoding="utf-8"))
    policy = manifest["qpu_policy"]
    backend_name = policy["backend"]
    path = list(policy["physical_path"])
    shots = int(args.shots or manifest["shots"])
    if backend_name is None or not path:
        raise SystemExit("no backend/path frozen in the manifest")

    print(f"backend {backend_name} | path {path} | shots {shots}",
          flush=True)

    from qiskit import qpy
    from qiskit.transpiler.preset_passmanagers import (
        generate_preset_pass_manager)

    backend = service().backend(backend_name)
    bundle = ROOT / "hardware" / "ibm_exp1" / "bundle"
    with (bundle / "logical_circuits.qpy").open("rb") as handle:
        circuits = qpy.load(handle)
    print(f"loaded {len(circuits)} logical circuits", flush=True)

    pm = generate_preset_pass_manager(
        optimization_level=3, backend=backend,
        initial_layout=path, seed_transpiler=1701)
    compiled = pm.run(circuits)
    print("transpiled", flush=True)

    allowed = set(path)
    twoq, depths, durations, unbound, swaps, stray = [], [], [], 0, 0, 0
    for circuit in compiled:
        ops = circuit.count_ops()
        if "swap" in ops:
            swaps += 1
        if circuit.parameters:
            unbound += 1
        used = set()
        n2 = 0
        for inst in circuit.data:
            qubits = [circuit.find_bit(q).index for q in inst.qubits]
            used.update(qubits)
            if len(qubits) == 2 and inst.operation.name != "barrier":
                n2 += 1
        if not used.issubset(allowed):
            stray += 1
        twoq.append(n2)
        depths.append(circuit.depth())
        try:
            durations.append(circuit.duration)
        except Exception:                                  # noqa: BLE001
            durations.append(None)

    gate_pass = (swaps == 0 and stray == 0 and unbound == 0)
    print(f"  SWAPs {swaps} | stray-qubit circuits {stray} | "
          f"unbound {unbound} -> gate {'PASS' if gate_pass else 'FAIL'}",
          flush=True)

    # ---- usage estimate
    dt = getattr(backend, "dt", None)
    valid = [d for d in durations if d]
    duration_s = None
    if valid and dt:
        duration_s = float(np.mean(valid)) * float(dt)
    rep_delay = None
    for attr in ("default_rep_delay", "rep_delay_default"):
        rep_delay = getattr(backend, attr, None) or (
            getattr(backend, "configuration", lambda: None)()
            and getattr(backend.configuration(), attr, None))
        if rep_delay:
            break
    if not rep_delay:
        rep_delay = 250e-6                     # documented default

    n_circuits = len(compiled) + M3_CAL_CIRCUITS
    executions = n_circuits * shots
    rough = ROUGH_OVERHEAD + ROUGH_PER_EXECUTION * executions
    per_execution = (duration_s or 0.0) + float(rep_delay)
    duration_based = ROUGH_OVERHEAD + per_execution * executions

    record = {
        "schema_version": 1,
        "backend": backend_name,
        "physical_path": path,
        "shots": shots,
        "circuits_primary": len(compiled),
        "circuits_with_m3_calibration": n_circuits,
        "executions": executions,
        "compilation_gate": {
            "no_swap": swaps == 0,
            "only_frozen_qubits": stray == 0,
            "all_parameters_bound": unbound == 0,
            "pass": gate_pass,
            "optimization_level": 3,
            "seed_transpiler": 1701,
        },
        "compiled": {
            "two_qubit_count_max": int(max(twoq)),
            "two_qubit_count_median": float(np.median(twoq)),
            "depth_max": int(max(depths)),
            "depth_median": float(np.median(depths)),
            "mean_circuit_duration_seconds": duration_s,
            "backend_dt": float(dt) if dt else None,
            "rep_delay_seconds": float(rep_delay),
        },
        "usage_estimate_seconds": {
            "rough_formula_ar023_s8": rough,
            "duration_based": duration_based,
            "per_execution_seconds": per_execution,
            "cap": 450.0,
            "free_allocation": 600.0,
            "rough_within_cap": bool(rough <= 450.0),
            "duration_based_within_cap": bool(duration_based <= 450.0),
        },
        "submission": "none - this script cannot submit",
    }
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "compile_estimate.json").write_text(
        json.dumps(record, indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    (args.out / "compile_estimate.meta.json").write_text(
        json.dumps({"compiled_utc": datetime.now(timezone.utc).isoformat()},
                   indent=2) + "\n", encoding="utf-8")

    print()
    print(f"two-qubit gates: median {np.median(twoq):.0f}, "
          f"max {max(twoq)} | depth median {np.median(depths):.0f}, "
          f"max {max(depths)}")
    if duration_s:
        print(f"mean compiled circuit duration: {duration_s*1e6:.1f} us "
              f"| rep delay {float(rep_delay)*1e6:.1f} us")
    print(f"usage estimate  rough {rough:.1f} s | duration-based "
          f"{duration_based:.1f} s | cap 450 s | free 600 s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
