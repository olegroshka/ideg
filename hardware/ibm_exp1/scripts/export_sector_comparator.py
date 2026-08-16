"""Replay AR-020e and export the frozen run-0 T3 comparator populations.

The command invokes an opt-in, T3-only path in the original AR-020e script.
It writes no final artifact unless the replayed objective matches the already
committed scalar result and all independent reconstruction checks pass.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
from importlib.metadata import version
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import tempfile

import numpy as np


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

from ideg.migraph import (mutual_information_matrix, pair_rdm,  # noqa: E402
                          phi_distance_matrix, phi_series)
from ideg.states import magnon_superposition  # noqa: E402
from experiment import (hardware_time_grid,  # noqa: E402
                        one_magnon_basis_index)


REGISTERED_CLASS = "TA_ii_quasiperiodic"
REGISTERED_N = 10
REGISTERED_RUN = 0
REGISTERED_TOLERANCE = 5.0e-10


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _array_hash(*arrays: np.ndarray) -> str:
    digest = sha256()
    for array in arrays:
        canonical = np.ascontiguousarray(array)
        digest.update(str(canonical.dtype).encode("ascii"))
        digest.update(np.asarray(canonical.shape, dtype="<i8").tobytes())
        digest.update(canonical.tobytes())
    return digest.hexdigest()


def _full_one_magnon_modes(site_modes: np.ndarray) -> np.ndarray:
    n_sites = site_modes.shape[0]
    full_modes = np.zeros((2 ** n_sites, n_sites), dtype=complex)
    for site in range(n_sites):
        full_modes[one_magnon_basis_index(site, n_sites), :] = site_modes[site]
    return full_modes


def _dynamic_states(
    initial_state: np.ndarray,
    energies: np.ndarray,
    full_modes: np.ndarray,
    times: np.ndarray,
) -> np.ndarray:
    coefficients = full_modes.conj().T @ initial_state
    phases = np.exp(-1.0j * np.outer(times, energies))
    return (full_modes @ (phases * coefficients[None, :]).T).T


def _run_registered_export(temp_dir: Path) -> tuple[dict, dict[str, np.ndarray]]:
    env = os.environ.copy()
    env["IDEG_EXPORT_COMPARATOR_DIR"] = str(temp_dir)
    env["IDEG_RUN_SLICE"] = "0:1"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "ar020e_sector_suite.py"),
         str(REGISTERED_N), "sector"],
        cwd=ROOT,
        env=env,
        check=True,
    )
    raw_json = temp_dir / "sector_comparator_raw_N10_run0.json"
    raw_npz = temp_dir / "sector_comparator_raw_N10_run0.npz"
    if not raw_json.exists() or not raw_npz.exists():
        raise RuntimeError("AR-020e export path did not produce both artifacts")
    metadata = _read_json(raw_json)
    with np.load(raw_npz, allow_pickle=False) as archive:
        arrays = {key: archive[key].copy() for key in archive.files}
    return metadata, arrays


def export_comparator(n_sites: int, run_index: int, output_dir: Path) -> dict:
    if (n_sites, run_index) != (REGISTERED_N, REGISTERED_RUN):
        raise ValueError("AR-023 is frozen to N=10 and run_index=0")

    results_dir = ROOT / "results" / "AR-010"
    manifest_path = results_dir / "confirmatory_manifest.json"
    sector_path = results_dir / "ar020e_sector_N10.json"
    manifest = _read_json(manifest_path)
    sector = _read_json(sector_path)
    seed = int(manifest["seeds"][REGISTERED_CLASS][str(n_sites)][run_index])
    group = sector["groups"][REGISTERED_CLASS]
    registered_position = group["run_indices"].index(run_index)
    registered_run = group["runs"][registered_position]
    registered_miss = float(registered_run["T3"]["miss"])
    registered_recheck = float(
        registered_run["T3"]["objective_recheck_fullrho"]
    )

    with tempfile.TemporaryDirectory(prefix="ideg-ar023-export-") as temp:
        raw, arrays = _run_registered_export(Path(temp))

    if (raw["n_sites"], raw["run_index"], raw["class"]) != (
        n_sites, run_index, REGISTERED_CLASS
    ):
        raise RuntimeError("AR-020e export selection metadata is inconsistent")
    if int(raw["paper_state_seed"]) != seed:
        raise RuntimeError("AR-020e export seed differs from the frozen manifest")
    replayed_miss = float(raw["T3"]["miss"])
    replayed_recheck = float(raw["T3"]["objective_recheck_fullrho"])
    if abs(replayed_miss - registered_miss) > REGISTERED_TOLERANCE:
        raise RuntimeError(
            "refusing export: replayed T3 miss "
            f"{replayed_miss:.12g} differs from registered "
            f"{registered_miss:.12g}"
        )
    if abs(replayed_recheck - registered_recheck) > REGISTERED_TOLERANCE:
        raise RuntimeError("replayed full-density recheck differs from AR-020e")

    p_star = np.asarray(arrays["p_star"], dtype="<f8")
    energies = np.asarray(arrays["eigenvalues"], dtype="<f8")
    site_modes = np.asarray(arrays["eigenvectors"], dtype="<c16")
    if p_star.shape != (n_sites,) or energies.shape != (n_sites,):
        raise RuntimeError("exported population/eigenvalue shapes are invalid")
    if site_modes.shape != (n_sites, n_sites):
        raise RuntimeError("exported one-magnon eigenvector shape is invalid")
    if not np.isclose(p_star.sum(), 1.0, atol=1.0e-12):
        raise RuntimeError("exported populations do not sum to one")
    if np.min(p_star) < -1.0e-12:
        raise RuntimeError("exported populations contain a negative value")
    if not np.all(np.diff(energies) > 0.0):
        raise RuntimeError("one-magnon energies are not strictly increasing")

    full_modes = _full_one_magnon_modes(site_modes)
    if not np.allclose(full_modes.conj().T @ full_modes, np.eye(n_sites),
                       atol=1.0e-10):
        raise RuntimeError("exported one-magnon modes are not orthonormal")
    initial_state, _ = magnon_superposition(
        n_sites, np.random.default_rng(seed)
    )
    full_times = np.arange(20.0, 200.0 + 1.0e-9, 0.5)
    dynamic = _dynamic_states(initial_state, energies, full_modes, full_times)
    dbar = phi_series(dynamic, n_sites).mean(axis=0)
    dbar_norm = float(np.linalg.norm(dbar))

    comparator = (full_modes * p_star[None, :]) @ full_modes.conj().T
    independent_recheck = float(np.linalg.norm(
        phi_distance_matrix(mutual_information_matrix(
            comparator, n_sites, mixed=True
        )) - dbar
    ) / dbar_norm)
    if abs(independent_recheck - replayed_miss) > 1.0e-10:
        raise RuntimeError("independent full-density objective recheck disagrees")

    pairs = [(i, j) for i in range(n_sites) for j in range(i + 1, n_sites)]
    mode_rdms = np.empty((n_sites, len(pairs), 4, 4), dtype=complex)
    for mode in range(n_sites):
        for pair_index, (i, j) in enumerate(pairs):
            mode_rdms[mode, pair_index] = pair_rdm(
                full_modes[:, mode], n_sites, i, j
            )

    indices, _ = hardware_time_grid(25)
    dbar_25 = phi_series(dynamic[indices], n_sites).mean(axis=0)
    quadrature_error = float(np.linalg.norm(dbar_25 - dbar) / dbar_norm)
    hopping = site_modes @ np.diag(energies) @ site_modes.conj().T
    comparator_site = site_modes @ np.diag(p_star) @ site_modes.conj().T
    stationarity_residual = float(np.linalg.norm(
        hopping @ comparator_site - comparator_site @ hopping
    ))

    source_hashes = {
        "confirmatory_manifest_sha256": sha256(
            manifest_path.read_bytes()
        ).hexdigest(),
        "ar020e_sector_sha256": sha256(sector_path.read_bytes()).hexdigest(),
        "ar020e_script_sha256": sha256(
            (ROOT / "scripts" / "ar020e_sector_suite.py").read_bytes()
        ).hexdigest(),
        "one_magnon_eigensystem_sha256": _array_hash(energies, site_modes),
    }
    metadata = {
        "schema_version": 1,
        "experiment_id": "ibm-exp1-qp-sector",
        "class": REGISTERED_CLASS,
        "n_sites": n_sites,
        "run_index": run_index,
        "paper_state_seed": seed,
        "eigenvalue_order": "ascending one-magnon hopping energy",
        "p_star": [float(value) for value in p_star],
        "eigenvalues": [float(value) for value in energies],
        "optimizer": {
            "method": "exact AR-020e T3 replay",
            "seed": 11,
            "starts": 2,
            "objective": replayed_miss,
            "registered_objective": registered_miss,
            "registered_fullrho_recheck": registered_recheck,
            "fullrho_recheck": independent_recheck,
        },
        "checks": {
            "population_sum": float(p_star.sum()),
            "minimum_population": float(p_star.min()),
            "stationarity_residual_one_magnon": stationarity_residual,
            "sector_weight_q1": 1.0,
            "time_count_preflight": len(indices),
            "time_quadrature_error": quadrature_error,
        },
        "source_hashes": source_hashes,
        "environment": {
            "python": platform.python_version(),
            "numpy": version("numpy"),
            "scipy": version("scipy"),
        },
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "sector_comparator_N10_run0.json"
    npz_path = output_dir / "sector_comparator_N10_run0.npz"
    with tempfile.NamedTemporaryFile(dir=output_dir, suffix=".npz",
                                     delete=False) as handle:
        temporary_npz = Path(handle.name)
    try:
        np.savez(
            temporary_npz,
            p_star=p_star,
            eigenvalues=energies,
            eigenvectors=site_modes,
            mode_pair_rdms=np.asarray(mode_rdms, dtype="<c16"),
        )
        temporary_npz.replace(npz_path)
    finally:
        temporary_npz.unlink(missing_ok=True)
    metadata["npz_sha256"] = sha256(npz_path.read_bytes()).hexdigest()
    json_path.write_text(json.dumps(metadata, indent=2) + "\n",
                         encoding="utf-8")
    return metadata


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-sites", type=int, default=REGISTERED_N)
    parser.add_argument("--run-index", type=int, default=REGISTERED_RUN)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "hardware" / "ibm_exp1" / "manifest",
    )
    args = parser.parse_args()
    metadata = export_comparator(args.n_sites, args.run_index,
                                 args.output_dir)
    print(json.dumps({
        "status": "exported",
        "objective": metadata["optimizer"]["objective"],
        "fullrho_recheck": metadata["optimizer"]["fullrho_recheck"],
        "npz_sha256": metadata["npz_sha256"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
