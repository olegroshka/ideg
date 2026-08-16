"""Build and verify the draft logical circuit bundle for AR-023.

This command is deliberately local-only: it never loads IBM credentials,
selects a backend, transpiles to hardware, or submits a job.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
from importlib.metadata import version
from io import BytesIO
import json
from pathlib import Path
import sys
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

import numpy as np


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

from circuits import (canonical_circuit_descriptors,  # noqa: E402
                      generic_state_preparation, preparation_circuit,
                      preparation_infidelity, qpy_sha256,
                      submission_permutation, tomography_circuit,
                      xxplusyy_state_preparation)
from experiment import (canonical_json_bytes, canonical_json_sha256,  # noqa: E402
                        canonicalize_mode_columns,
                        evolve_one_magnon_amplitudes,
                        one_magnon_hopping,
                        registered_initial_site_amplitudes)


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _verify_manifest(manifest: dict) -> None:
    declared = manifest.get("manifest_sha256")
    unhashed = dict(manifest)
    unhashed.pop("manifest_sha256", None)
    if declared != canonical_json_sha256(unhashed):
        raise RuntimeError("manifest content does not match manifest_sha256")
    if manifest["selection"] != {
        "class": "TA_ii_quasiperiodic",
        "n_sites": 10,
        "run_index": 0,
        "paper_state_seed": 2100294288,
    }:
        raise RuntimeError("manifest does not select the registered AR-023 run")
    if manifest["status"] not in {"DRAFT", "FROZEN"}:
        raise RuntimeError("manifest status must be DRAFT or FROZEN")


def _deterministic_npz(path: Path, arrays: dict[str, np.ndarray]) -> None:
    """Write an allow_pickle=False-compatible NPZ with stable ZIP metadata."""
    with ZipFile(path, mode="w", compression=ZIP_DEFLATED,
                 compresslevel=9) as archive:
        for name in sorted(arrays):
            buffer = BytesIO()
            np.lib.format.write_array(
                buffer, np.ascontiguousarray(arrays[name]), allow_pickle=False
            )
            info = ZipInfo(f"{name}.npy", date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o600 << 16
            archive.writestr(info, buffer.getvalue(), compress_type=ZIP_DEFLATED,
                             compresslevel=9)


def _target_states(manifest: dict, comparator_path: Path):
    with np.load(comparator_path, allow_pickle=False) as archive:
        p_star = np.asarray(archive["p_star"], dtype=float)
        energies = np.asarray(archive["eigenvalues"], dtype=float)
        modes = canonicalize_mode_columns(archive["eigenvectors"])
    hopping = one_magnon_hopping(10)
    residual = float(np.linalg.norm(
        hopping @ modes - modes * energies[None, :]
    ))
    if residual > 1.0e-10:
        raise RuntimeError(f"comparator eigensystem residual {residual:.3g}")
    initial = registered_initial_site_amplitudes(
        manifest["selection"]["paper_state_seed"], 10
    )
    times = np.asarray(manifest["time_grid"]["values"], dtype=float)
    dynamic = evolve_one_magnon_amplitudes(initial, times, energies, modes)
    control_mode = int(np.argmax(p_star))
    targets = {
        **{f"dynamic_t{index:03d}": dynamic[index]
           for index in range(len(dynamic))},
        **{f"sector_e{mode:02d}": modes[:, mode]
           for mode in range(10)},
    }
    return targets, dynamic, modes, energies, p_star, control_mode, residual


def build_bundle(
    manifest_path: Path,
    output_dir: Path,
    method: str,
    overwrite: bool,
) -> dict:
    manifest_path = manifest_path.resolve()
    manifest = _read_json(manifest_path)
    _verify_manifest(manifest)
    comparator_path = (
        ROOT / manifest["comparator"]["npz_path"]
    ).resolve()
    if sha256(comparator_path.read_bytes()).hexdigest() != (
        manifest["comparator"]["npz_sha256"]
    ):
        raise RuntimeError("comparator NPZ hash differs from the manifest")

    output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    outputs = {
        "qpy": output_dir / "logical_circuits.qpy",
        "registry": output_dir / "circuit_registry.json",
        "targets": output_dir / "target_states.npz",
        "report": output_dir / "state_prep_report.json",
        "bundle": output_dir / "logical_bundle.json",
    }
    existing = [path for path in outputs.values() if path.exists()]
    if existing and not overwrite:
        raise FileExistsError(
            "refusing to overwrite existing bundle files: "
            + ", ".join(str(path) for path in existing)
        )

    (targets, dynamic, modes, energies, p_star, control_mode,
     eigensystem_residual) = _target_states(manifest, comparator_path)
    candidate_rows = []
    selected_preparations = {}
    for state_id, target in targets.items():
        ladder = xxplusyy_state_preparation(target, name=state_id + "_xxyy")
        generic = generic_state_preparation(target, name=state_id + "_generic")
        ladder_infidelity = preparation_infidelity(ladder, target)
        generic_infidelity = preparation_infidelity(generic, target)
        if max(ladder_infidelity, generic_infidelity) >= 1.0e-10:
            raise RuntimeError(
                f"state-preparation fidelity gate failed for {state_id}"
            )
        candidate_rows.append({
            "state_id": state_id,
            "xxplusyy_infidelity": ladder_infidelity,
            "generic_infidelity": generic_infidelity,
            "xxplusyy_two_qubit_gates_logical": 9,
        })
        selected_preparations[state_id] = (
            ladder if method == "xxplusyy" else generic
        )

    descriptors = canonical_circuit_descriptors(manifest, control_mode)
    expected = int(manifest["arms"]["primary_circuit_count"])
    if len(descriptors) != expected:
        raise RuntimeError(
            f"registry has {len(descriptors)} circuits, expected {expected}"
        )
    pub_to_canonical, canonical_to_pub = submission_permutation(
        descriptors, manifest["seeds"]["circuit_shuffle_seed"]
    )
    canonical_by_index = {row["canonical_index"]: row
                          for row in descriptors}
    circuits = []
    registry = []
    for pub_index, canonical_index in enumerate(pub_to_canonical):
        row = dict(canonical_by_index[canonical_index])
        preparation = selected_preparations[row["state_id"]]
        circuit = tomography_circuit(
            preparation, row["logical_basis_string"], row["circuit_id"]
        )
        circuit.metadata = {
            "ar_id": "AR-023",
            "circuit_id": row["circuit_id"],
            "canonical_index": canonical_index,
            "pub_index": pub_index,
            "preparation_method": method,
        }
        row["pub_index"] = pub_index
        row["logical_circuit_sha256"] = qpy_sha256(circuit)
        circuits.append(circuit)
        registry.append(row)

    from qiskit import qpy

    with outputs["qpy"].open("wb") as handle:
        qpy.dump(circuits, handle)
    qpy_hash = sha256(outputs["qpy"].read_bytes()).hexdigest()

    registry_payload = {
        "schema_version": 1,
        "experiment_id": manifest["experiment_id"],
        "manifest_sha256": manifest["manifest_sha256"],
        "preparation_method": method,
        "control_mode_selection": "argmax(p_star)",
        "control_mode": control_mode,
        "pub_to_canonical": pub_to_canonical,
        "canonical_to_pub": canonical_to_pub,
        "circuits": registry,
    }
    registry_hash = canonical_json_sha256(registry_payload)
    outputs["registry"].write_text(
        json.dumps(registry_payload, indent=2) + "\n", encoding="utf-8"
    )

    _deterministic_npz(outputs["targets"], {
        "dynamic_site_amplitudes": dynamic.astype("<c16"),
        "hardware_times": np.asarray(manifest["time_grid"]["values"],
                                     dtype="<f8"),
        "one_magnon_energies": energies.astype("<f8"),
        "one_magnon_modes_site": modes.astype("<c16"),
        "p_star": p_star.astype("<f8"),
        "psi0_site": targets["dynamic_t000"].astype("<c16")
        if float(manifest["time_grid"]["values"][0]) == 0.0
        else registered_initial_site_amplitudes(
            manifest["selection"]["paper_state_seed"], 10
        ).astype("<c16"),
    })
    target_hash = sha256(outputs["targets"].read_bytes()).hexdigest()

    report = {
        "schema_version": 1,
        "fidelity_threshold": 1.0e-10,
        "unique_target_count": len(targets),
        "selected_draft_method": method,
        "selection_status": "DRAFT_PENDING_BACKEND_COMPARISON",
        "max_xxplusyy_infidelity": max(
            row["xxplusyy_infidelity"] for row in candidate_rows
        ),
        "max_generic_infidelity": max(
            row["generic_infidelity"] for row in candidate_rows
        ),
        "one_magnon_eigensystem_residual": eigensystem_residual,
        "states": candidate_rows,
    }
    outputs["report"].write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )

    result = {
        "schema_version": 1,
        "status": "DRAFT_LOGICAL",
        "experiment_id": manifest["experiment_id"],
        "manifest_path": str(manifest_path),
        "manifest_sha256": manifest["manifest_sha256"],
        "preparation_method": method,
        "unique_target_count": len(targets),
        "circuit_count": len(circuits),
        "shots": manifest["shots"],
        "control_mode": control_mode,
        "qpy_sha256": qpy_hash,
        "circuit_registry_sha256": registry_hash,
        "target_states_sha256": target_hash,
        "files": {key: path.name for key, path in outputs.items()
                  if key != "bundle"},
        "environment": {
            "python": sys.version.split()[0],
            "numpy": version("numpy"),
            "qiskit": version("qiskit"),
        },
        "submission_ready": False,
        "submission_blockers": [
            "manifest is not frozen",
            "backend and physical path are not selected",
            "finite-shot/noisy simulator gates are incomplete",
            "circuits are not hardware-transpiled",
            "usage including M3 calibration is not estimated",
            "explicit QPU-GO has not been supplied",
        ],
    }
    result["bundle_sha256"] = canonical_json_sha256(result)
    outputs["bundle"].write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest", type=Path,
        default=ROOT / "hardware" / "ibm_exp1" / "manifest"
        / "hardware_manifest.json",
    )
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--method", choices=("xxplusyy", "generic"),
                        default="xxplusyy")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    result = build_bundle(args.manifest, args.output_dir, args.method,
                          args.overwrite)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
