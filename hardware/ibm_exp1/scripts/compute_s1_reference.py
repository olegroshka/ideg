"""Compute and record the exact 37-grid S1 reference endpoint (AR-023a §0).

First required computation before any sampling: the exact finite-grid
endpoint eps_sector^(37) = ||Phi[sigma*] - Dbar_37||_F / ||Dbar_37||_F,
computed from the frozen comparator artifact and the registered state
through the paper's own metric implementation (ideg.migraph).

Fail-closed: refuses to run unless the manifest self-hash and the frozen
comparator NPZ hash verify; refuses to overwrite an existing reference
record without --overwrite.  Cross-checks before recording anything:

  1. the 361-grid replay endpoint must match the registered replay
     objective 0.22410775407580497 within --replay-tolerance;
  2. the 37-vs-361 quadrature error must match the recorded manifest
     value within --quadrature-tolerance;
  3. the comparator metric via RDM-first mixing (the hardware arm's
     definition) must match the full-density-matrix route within 1e-10.

No IBM credentials, no network access, no sampling.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
from importlib.metadata import version
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

from ideg.migraph import (mutual_information_matrix,  # noqa: E402
                          pair_rdm, phi_distance_matrix)
from experiment import (I0, X_MIN, canonical_json_sha256,  # noqa: E402
                        canonicalize_mode_columns,
                        embed_one_magnon_amplitudes,
                        evolve_one_magnon_amplitudes,
                        one_magnon_hopping,
                        registered_initial_site_amplitudes)
from build_circuits import _deterministic_npz  # noqa: E402


def _entropy4(rho: np.ndarray) -> float:
    vals = np.linalg.eigvalsh(0.5 * (rho + rho.conj().T))
    vals = vals[vals > 1.0e-14]
    return float(-np.sum(vals * np.log(vals)))


def metric_from_mixed_pair_rdms(pair_rdms: np.ndarray,
                                pairs: list[tuple[int, int]],
                                n_sites: int) -> np.ndarray:
    """Phi from (45, 4, 4) pair RDMs — the hardware comparator-arm path."""
    mi = np.zeros((n_sites, n_sites))
    for index, (i, j) in enumerate(pairs):
        rho4 = pair_rdms[index]
        r = rho4.reshape(2, 2, 2, 2)
        rho_i = np.trace(r, axis1=1, axis2=3)
        rho_j = np.trace(r, axis1=0, axis2=2)
        mi[i, j] = mi[j, i] = max(
            _entropy4(rho_i) + _entropy4(rho_j) - _entropy4(rho4), 0.0
        )
    return phi_distance_matrix(mi)


def exact_phi_series(site_amplitudes: np.ndarray, n_sites: int) -> np.ndarray:
    """(T, n, n) exact metric stack for one-magnon site-amplitude rows."""
    out = np.empty((len(site_amplitudes), n_sites, n_sites))
    for t, row in enumerate(site_amplitudes):
        psi = embed_one_magnon_amplitudes(row, n_sites)
        mi = mutual_information_matrix(psi, n_sites, mixed=False)
        out[t] = phi_distance_matrix(mi)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest", type=Path,
        default=ROOT / "hardware" / "ibm_exp1" / "manifest"
        / "hardware_manifest.json")
    parser.add_argument(
        "--output-dir", type=Path,
        default=ROOT / "hardware" / "ibm_exp1" / "results" / "sim_reference")
    parser.add_argument("--replay-tolerance", type=float, default=1.0e-8)
    parser.add_argument("--quadrature-tolerance", type=float, default=1.0e-8)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    manifest_path = args.manifest.resolve()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    declared = dict(manifest)
    declared_hash = declared.pop("manifest_sha256")
    if canonical_json_sha256(declared) != declared_hash:
        raise RuntimeError("manifest content does not match manifest_sha256")
    if "s1_reference" in manifest and not args.overwrite:
        raise RuntimeError("s1_reference already recorded; use --overwrite")

    n_sites = int(manifest["selection"]["n_sites"])
    comparator_path = (ROOT / manifest["comparator"]["npz_path"]).resolve()
    npz_bytes = comparator_path.read_bytes()
    if sha256(npz_bytes).hexdigest() != manifest["comparator"]["npz_sha256"]:
        raise RuntimeError("comparator NPZ hash differs from the manifest")
    with np.load(comparator_path, allow_pickle=False) as archive:
        p_star = np.asarray(archive["p_star"], dtype=float)
        energies = np.asarray(archive["eigenvalues"], dtype=float)
        modes = canonicalize_mode_columns(archive["eigenvectors"])
        mode_pair_rdms = np.asarray(archive["mode_pair_rdms"], dtype=complex)

    residual = float(np.linalg.norm(
        one_magnon_hopping(n_sites) @ modes - modes * energies[None, :]))
    if residual > 1.0e-10:
        raise RuntimeError(f"comparator eigensystem residual {residual:.3g}")

    pairs = [(i, j) for i in range(n_sites) for j in range(i + 1, n_sites)]

    # Registered state, exact evolution on both grids.
    initial = registered_initial_site_amplitudes(
        manifest["selection"]["paper_state_seed"], n_sites)
    start, stop = manifest["model"]["time_window"]
    full_times = np.arange(start, stop + 1.0e-9,
                           manifest["model"]["full_time_step"])
    grid_indices = np.asarray(manifest["time_grid"]["indices"], dtype=int)
    grid_times = np.asarray(manifest["time_grid"]["values"], dtype=float)
    if not np.allclose(full_times[grid_indices], grid_times, atol=1.0e-12):
        raise RuntimeError("manifest time grid does not index the full grid")

    dynamic_full = evolve_one_magnon_amplitudes(
        initial, full_times, energies, modes)
    d_series_full = exact_phi_series(dynamic_full, n_sites)
    dbar_full = d_series_full.mean(axis=0)
    d_series_grid = d_series_full[grid_indices]
    dbar_grid = d_series_grid.mean(axis=0)

    # Comparator metric, both routes.
    sigma_pair_rdms = np.tensordot(p_star, mode_pair_rdms, axes=(0, 0))
    d_star_rdm = metric_from_mixed_pair_rdms(sigma_pair_rdms, pairs, n_sites)

    full_modes = np.stack([
        embed_one_magnon_amplitudes(modes[:, k], n_sites)
        for k in range(n_sites)], axis=1)
    sigma_full = (full_modes * p_star[None, :]) @ full_modes.conj().T
    mi_sigma_full = mutual_information_matrix(sigma_full, n_sites, mixed=True)
    d_star_full = phi_distance_matrix(mi_sigma_full)
    rdm_vs_full = float(np.linalg.norm(d_star_rdm - d_star_full))
    if rdm_vs_full > 1.0e-10:
        raise RuntimeError(
            f"RDM-mix vs full-rho comparator mismatch {rdm_vs_full:.3g}")

    dbar_full_norm = float(np.linalg.norm(dbar_full))
    dbar_grid_norm = float(np.linalg.norm(dbar_grid))
    eps_361 = float(np.linalg.norm(d_star_rdm - dbar_full) / dbar_full_norm)
    eps_grid = float(np.linalg.norm(d_star_rdm - dbar_grid) / dbar_grid_norm)
    quadrature = float(
        np.linalg.norm(dbar_grid - dbar_full) / dbar_full_norm)

    registered_replay = float(manifest["comparator"]["objective"])
    replay_diff = abs(eps_361 - registered_replay)
    if replay_diff > args.replay_tolerance:
        raise RuntimeError(
            f"361-grid replay {eps_361!r} differs from registered "
            f"{registered_replay!r} by {replay_diff:.3g}")
    recorded_quadrature = float(
        manifest["time_grid"]["ideal_relative_quadrature_error"])
    quadrature_diff = abs(quadrature - recorded_quadrature)
    if quadrature_diff > args.quadrature_tolerance:
        raise RuntimeError(
            f"quadrature replay {quadrature!r} differs from recorded "
            f"{recorded_quadrature!r} by {quadrature_diff:.3g}")

    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    arrays_path = output_dir / "s1_reference_arrays.npz"
    _deterministic_npz(arrays_path, {
        "dbar_37_ideal": dbar_grid.astype("<f8"),
        "d_series_37_ideal": d_series_grid.astype("<f8"),
        "dbar_361_ideal": dbar_full.astype("<f8"),
        "d_star_ideal": d_star_rdm.astype("<f8"),
        "sigma_pair_rdms": sigma_pair_rdms.astype("<c16"),
        "pairs": np.asarray(pairs, dtype="<i8"),
        "hardware_times": grid_times.astype("<f8"),
    })
    arrays_hash = sha256(arrays_path.read_bytes()).hexdigest()

    record = {
        "schema_version": 1,
        "eps_sector_37": eps_grid,
        "eps_sector_361_replay": eps_361,
        "registered_replay_objective": registered_replay,
        "replay_abs_difference": replay_diff,
        "quadrature_error_replay": quadrature,
        "quadrature_error_recorded": recorded_quadrature,
        "quadrature_abs_difference": quadrature_diff,
        "d_star_rdm_vs_fullrho_fro": rdm_vs_full,
        "dbar_37_fro_norm": dbar_grid_norm,
        "dbar_361_fro_norm": dbar_full_norm,
        "comparator_npz_sha256": manifest["comparator"]["npz_sha256"],
        "metric_constants": {"I0": float(I0), "x_min": float(X_MIN)},
        "arrays_file": arrays_path.name,
        "arrays_sha256": arrays_hash,
        "environment": {
            "python": sys.version.split()[0],
            "numpy": version("numpy"),
            "scipy": version("scipy"),
        },
        "computed_by": Path(__file__).name,
    }
    (output_dir / "s1_reference.json").write_text(
        json.dumps(record, indent=2) + "\n", encoding="utf-8")

    manifest.pop("manifest_sha256", None)
    manifest["s1_reference"] = record
    manifest["manifest_sha256"] = canonical_json_sha256(manifest)
    manifest_path.write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({
        "eps_sector_37": eps_grid,
        "eps_sector_361_replay": eps_361,
        "replay_abs_difference": replay_diff,
        "quadrature_abs_difference": quadrature_diff,
        "manifest_sha256": manifest["manifest_sha256"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
