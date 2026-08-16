"""Create a draft or frozen scientific manifest for AR-023.

This command performs only local, credential-free work.  It refuses to build
without the validated comparator export and does not select or contact an IBM
backend.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

from ideg.migraph import phi_series  # noqa: E402
from ideg.states import magnon_superposition  # noqa: E402
from experiment import (canonical_json_sha256, covering_array_rows,  # noqa: E402
                        hardware_time_grid, one_magnon_basis_index,
                        paper_site_to_qiskit, validate_covering_array)


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _git(args: list[str]) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=ROOT, text=True, stderr=subprocess.DEVNULL
    ).strip()


def _dynamic_states(initial: np.ndarray, times: np.ndarray) -> np.ndarray:
    n_sites = 10
    hopping = np.zeros((n_sites, n_sites), dtype=float)
    for site in range(n_sites - 1):
        hopping[site, site + 1] = hopping[site + 1, site] = 1.0
    energies, modes = np.linalg.eigh(hopping)
    amplitudes = np.array([
        initial[one_magnon_basis_index(site, n_sites)]
        for site in range(n_sites)
    ])
    coefficients = modes.conj().T @ amplitudes
    evolved = (modes @ (
        np.exp(-1.0j * np.outer(times, energies))
        * coefficients[None, :]
    ).T).T
    states = np.zeros((len(times), 2 ** n_sites), dtype=complex)
    for site in range(n_sites):
        states[:, one_magnon_basis_index(site, n_sites)] = evolved[:, site]
    return states


def build_manifest(args: argparse.Namespace) -> dict:
    if (args.n_sites, args.run_index) != (10, 0):
        raise ValueError("AR-023 is frozen to N=10 and run_index=0")
    if args.shots not in (768, 1024):
        raise ValueError("shots must be a separately declared 768 or 1024")
    validate_covering_array()

    manifest_dir = ROOT / "hardware" / "ibm_exp1" / "manifest"
    comparator_json = manifest_dir / "sector_comparator_N10_run0.json"
    comparator_npz = manifest_dir / "sector_comparator_N10_run0.npz"
    if not comparator_json.exists() or not comparator_npz.exists():
        raise FileNotFoundError(
            "validated comparator export is missing; run "
            "export_sector_comparator.py first"
        )
    comparator = _read_json(comparator_json)
    actual_npz_hash = sha256(comparator_npz.read_bytes()).hexdigest()
    if actual_npz_hash != comparator["npz_sha256"]:
        raise RuntimeError("comparator NPZ hash does not match metadata")
    with np.load(comparator_npz, allow_pickle=False) as archive:
        p_star = archive["p_star"]
        if p_star.shape != (10,) or not np.isclose(p_star.sum(), 1.0,
                                                   atol=1.0e-12):
            raise RuntimeError("invalid comparator population array")

    paper_manifest_path = ROOT / "results" / "AR-010" / "confirmatory_manifest.json"
    paper_manifest = _read_json(paper_manifest_path)
    seed = int(paper_manifest["seeds"]["TA_ii_quasiperiodic"]["10"][0])
    if seed != int(comparator["paper_state_seed"]):
        raise RuntimeError("paper seed and comparator seed disagree")
    initial, _ = magnon_superposition(10, np.random.default_rng(seed))
    full_times = np.arange(20.0, 200.0 + 1.0e-9, 0.5)
    full_metrics = phi_series(_dynamic_states(initial, full_times), 10)
    dbar_full = full_metrics.mean(axis=0)
    time_indices, times = hardware_time_grid(args.time_count)
    dbar_selected = full_metrics[time_indices].mean(axis=0)
    quadrature_error = float(
        np.linalg.norm(dbar_selected - dbar_full) / np.linalg.norm(dbar_full)
    )
    if quadrature_error > 0.025:
        raise RuntimeError(
            f"time quadrature error {quadrature_error:.6g} exceeds 0.025; "
            "retry deterministically with 37 and then 49 points"
        )

    dirty = _git(["status", "--porcelain"]).splitlines()
    if args.freeze and dirty:
        raise RuntimeError("cannot freeze a manifest from a dirty worktree")
    rows = covering_array_rows()
    primary_circuit_count = (len(times) + 10 + 2) * len(rows)
    executions = primary_circuit_count * args.shots
    rough_seconds = 2.0 + 0.00035 * executions
    if rough_seconds > 450.0:
        raise RuntimeError(
            f"rough QPU estimate {rough_seconds:.3f}s exceeds the 450s cap; "
            "follow the registered degradation ladder"
        )
    result = {
        "schema_version": 1,
        "experiment_id": "ibm-exp1-qp-sector",
        "status": "FROZEN" if args.freeze else "DRAFT",
        "source": {
            "git_commit": _git(["rev-parse", "HEAD"]),
            "worktree_dirty": bool(dirty),
            "dirty_paths": dirty,
            "paper_manifest_sha256": sha256(
                paper_manifest_path.read_bytes()
            ).hexdigest(),
        },
        "selection": {
            "class": "TA_ii_quasiperiodic",
            "n_sites": 10,
            "run_index": 0,
            "paper_state_seed": seed,
        },
        "model": {
            "name": "open XX chain",
            "clock": "external laboratory time in J=1 units",
            "time_window": [20.0, 200.0],
            "full_time_step": 0.5,
        },
        "time_grid": {
            "count": len(times),
            "indices": [int(value) for value in time_indices],
            "values": [float(value) for value in times],
            "ideal_relative_quadrature_error": quadrature_error,
            "maximum_allowed_error": 0.025,
        },
        "tomography": {
            "design": "GF(3)^3 strength-two covering array",
            "settings": len(rows),
            "basis_strings_paper_order": list(rows),
            "pair_axis_multiplicity": 3,
        },
        "bit_order": {
            "paper_site_to_qiskit_qubit": list(paper_site_to_qiskit()),
            "paper_site_zero": "most-significant tensor factor",
            "qiskit_qubit_zero": "least-significant statevector bit",
        },
        "shots": args.shots,
        "arms": {
            "dynamic_states": len(times),
            "sector_basis_states": 10,
            "control_states": 2,
            "primary_circuit_count": primary_circuit_count,
            "primary_executions": executions,
        },
        "comparator": {
            "metadata_path": str(comparator_json.relative_to(ROOT)).replace("\\", "/"),
            "npz_path": str(comparator_npz.relative_to(ROOT)).replace("\\", "/"),
            "npz_sha256": actual_npz_hash,
            "objective": comparator["optimizer"]["objective"],
            "fullrho_recheck": comparator["optimizer"]["fullrho_recheck"],
        },
        "seeds": {
            "paper_state_seed": seed,
            "optimizer_seed": 11,
            "transpiler_seed": 1701,
            "circuit_shuffle_seed": 23001,
            "ideal_sampler_seed": 23002,
            "noisy_sampler_seed": 23003,
            "bootstrap_seed": 23004,
            "shot_split_seed": 23005,
        },
        "qpu_policy": {
            "backend": None,
            "physical_path": None,
            "estimated_seconds": None,
            "rough_formula_seconds": rough_seconds,
            "maximum_estimated_seconds": 450,
            "minimum_remaining_seconds": 500,
            "submission_confirmation": "QPU-GO",
        },
    }
    result["manifest_sha256"] = canonical_json_sha256(result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-sites", type=int, default=10)
    parser.add_argument("--run-index", type=int, default=0)
    parser.add_argument("--time-count", type=int, default=25)
    parser.add_argument("--shots", type=int, default=1024)
    parser.add_argument("--freeze", action="store_true")
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "hardware" / "ibm_exp1" / "manifest"
        / "hardware_manifest.json",
    )
    args = parser.parse_args()
    manifest = build_manifest(args)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(manifest, indent=2) + "\n",
                           encoding="utf-8")
    print(json.dumps({
        "status": manifest["status"],
        "manifest_sha256": manifest["manifest_sha256"],
        "time_quadrature_error": manifest["time_grid"][
            "ideal_relative_quadrature_error"
        ],
        "primary_circuit_count": manifest["arms"]["primary_circuit_count"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
