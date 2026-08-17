"""Pure helpers for the AR-023 IBM hardware pilot.

This module has no IBM imports and no external side effects.  It owns the
tomography design, bit-order contract, density-matrix reconstruction, and
metric parity implementation used by preflight tests and later Qiskit code.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json
from itertools import product
from typing import Mapping

import numpy as np


N_SITES = 10
I0 = 2.0 * np.log(2.0)
X_MIN = 1.0e-6
AXES = ("X", "Y", "Z")
COVERING_VECTORS = (
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (1, 1, 0),
    (1, 2, 0),
    (1, 0, 1),
    (1, 0, 2),
    (0, 1, 1),
    (0, 1, 2),
    (1, 1, 1),
)

ALL_Z_ROW = "Z" * N_SITES
RECONSTRUCTION_ROWS = 27

PAULI = {
    "I": np.eye(2, dtype=complex),
    "X": np.array([[0, 1], [1, 0]], dtype=complex),
    "Y": np.array([[0, -1j], [1j, 0]], dtype=complex),
    "Z": np.array([[1, 0], [0, -1]], dtype=complex),
}


def paper_site_to_qiskit(n_sites: int = N_SITES) -> tuple[int, ...]:
    """Map paper site 0 (MSB tensor factor) to Qiskit qubit indices."""
    if n_sites < 1:
        raise ValueError("n_sites must be positive")
    return tuple(n_sites - 1 - site for site in range(n_sites))


def one_magnon_basis_index(site: int, n_sites: int = N_SITES) -> int:
    """Computational-basis index for one excitation at a paper site."""
    if not 0 <= site < n_sites:
        raise ValueError(f"site {site} outside 0..{n_sites - 1}")
    return 1 << (n_sites - 1 - site)


def one_magnon_hopping(n_sites: int = N_SITES) -> np.ndarray:
    """Return the open-chain hopping matrix in paper-site order."""
    if n_sites < 2:
        raise ValueError("n_sites must be at least two")
    hopping = np.zeros((n_sites, n_sites), dtype=float)
    indices = np.arange(n_sites - 1)
    hopping[indices, indices + 1] = 1.0
    hopping[indices + 1, indices] = 1.0
    return hopping


def canonicalize_mode_columns(modes: np.ndarray) -> np.ndarray:
    """Fix each eigenvector phase at its largest-magnitude component."""
    canonical = np.asarray(modes, dtype=complex).copy()
    if canonical.ndim != 2:
        raise ValueError("modes must be a matrix with eigenvectors in columns")
    for column in range(canonical.shape[1]):
        pivot = int(np.argmax(np.abs(canonical[:, column])))
        value = canonical[pivot, column]
        if abs(value) == 0.0:
            raise ValueError("mode column cannot be the zero vector")
        canonical[:, column] *= np.exp(-1.0j * np.angle(value))
        canonical[pivot, column] = abs(canonical[pivot, column]) + 0.0j
    return np.ascontiguousarray(canonical)


def one_magnon_eigensystem(
    n_sites: int = N_SITES,
) -> tuple[np.ndarray, np.ndarray]:
    """Return ordered energies and canonically phased paper-site modes."""
    energies, modes = np.linalg.eigh(one_magnon_hopping(n_sites))
    return energies, canonicalize_mode_columns(modes)


def extract_one_magnon_amplitudes(
    statevector: np.ndarray,
    n_sites: int = N_SITES,
    tolerance: float = 1.0e-13,
) -> np.ndarray:
    """Extract paper-site amplitudes and reject weight outside q=1."""
    state = np.asarray(statevector, dtype=complex)
    if state.shape != (2 ** n_sites,):
        raise ValueError("statevector has the wrong dimension")
    indices = np.array([
        one_magnon_basis_index(site, n_sites) for site in range(n_sites)
    ])
    amplitudes = state[indices].copy()
    sector_weight = float(np.vdot(amplitudes, amplitudes).real)
    if abs(sector_weight - 1.0) > tolerance:
        raise ValueError(
            f"state has one-magnon sector weight {sector_weight:.16g}"
        )
    return amplitudes


def embed_one_magnon_amplitudes(
    amplitudes: np.ndarray,
    n_sites: int | None = None,
) -> np.ndarray:
    """Embed paper-site amplitudes in Qiskit's little-endian statevector."""
    site = np.asarray(amplitudes, dtype=complex)
    n_sites = len(site) if n_sites is None else n_sites
    if site.shape != (n_sites,):
        raise ValueError("amplitudes must contain one value per paper site")
    norm = float(np.linalg.norm(site))
    if not np.isclose(norm, 1.0, atol=1.0e-12):
        raise ValueError(f"one-magnon amplitudes have norm {norm:.16g}")
    state = np.zeros(2 ** n_sites, dtype=complex)
    for paper_site, value in enumerate(site):
        state[one_magnon_basis_index(paper_site, n_sites)] = value
    return state


def registered_initial_site_amplitudes(
    seed: int,
    n_sites: int = N_SITES,
) -> np.ndarray:
    """Recreate the registered paper state and return its site amplitudes."""
    from ideg.states import magnon_superposition

    state, _ = magnon_superposition(
        n_sites, np.random.default_rng(int(seed))
    )
    return extract_one_magnon_amplitudes(state, n_sites)


def evolve_one_magnon_amplitudes(
    initial_site: np.ndarray,
    times: np.ndarray,
    energies: np.ndarray | None = None,
    modes_site: np.ndarray | None = None,
) -> np.ndarray:
    """Analytically evolve site amplitudes under the open XX hopping block."""
    initial = np.asarray(initial_site, dtype=complex)
    n_sites = len(initial)
    sample_times = np.asarray(times, dtype=float)
    if sample_times.ndim != 1:
        raise ValueError("times must be one-dimensional")
    if energies is None or modes_site is None:
        energies, modes_site = one_magnon_eigensystem(n_sites)
    energies = np.asarray(energies, dtype=float)
    modes = np.asarray(modes_site, dtype=complex)
    if energies.shape != (n_sites,) or modes.shape != (n_sites, n_sites):
        raise ValueError("invalid one-magnon eigensystem shapes")
    coefficients = modes.conj().T @ initial
    phases = np.exp(-1.0j * np.outer(sample_times, energies))
    evolved = (phases * coefficients[None, :]) @ modes.T
    norms = np.linalg.norm(evolved, axis=1)
    if not np.allclose(norms, 1.0, atol=1.0e-12):
        raise RuntimeError("one-magnon evolution did not preserve norm")
    return np.ascontiguousarray(evolved)


def covering_array_rows(n_sites: int = N_SITES) -> tuple[str, ...]:
    """Return the registered 27 tomography basis strings in paper order."""
    if n_sites != len(COVERING_VECTORS):
        raise ValueError("the registered covering array is defined for N=10")
    rows = []
    for r in product(range(3), repeat=3):
        rows.append("".join(
            AXES[sum(rv * vv for rv, vv in zip(r, v)) % 3]
            for v in COVERING_VECTORS
        ))
    return tuple(rows)


def tomography_rows(include_leakage_row: bool = True) -> tuple[str, ...]:
    """Registered settings: 27 covering-array rows + the all-Z witness.

    AR-023a Amendment A2.5: the all-Z row exists because AR-023 §5's
    one-excitation diagnostic needs all ten sites measured in Z
    simultaneously, which no covering-array row provides (maximum 6 of
    10, and the GF(3) construction cannot yield an all-Z row).  It is a
    leakage witness ONLY and is excluded from the RDM reconstruction so
    that the tomography estimator stays identical to the validated one.
    """
    rows = covering_array_rows()
    return rows + (ALL_Z_ROW,) if include_leakage_row else rows


def leakage_row_index(rows: tuple[str, ...] | None = None) -> int:
    """Index of the all-Z witness row; raises when it is absent."""
    rows = tomography_rows() if rows is None else rows
    for index, row in enumerate(rows):
        if row == ALL_Z_ROW:
            return index
    raise ValueError("no all-Z leakage witness row present")


def validate_covering_array(rows: tuple[str, ...] | None = None) -> None:
    """Raise unless every ordered axis pair occurs exactly three times."""
    rows = covering_array_rows() if rows is None else rows
    if len(rows) != 27 or len(set(rows)) != 27:
        raise ValueError("covering array must contain 27 distinct rows")
    expected = {a + b: 3 for a in AXES for b in AXES}
    for i in range(N_SITES):
        for j in range(i + 1, N_SITES):
            got = Counter(row[i] + row[j] for row in rows)
            if dict(got) != expected:
                raise ValueError(f"pair {(i, j)} has invalid coverage: {got}")


def hardware_time_grid(time_count: int = 25) -> tuple[np.ndarray, np.ndarray]:
    """Return deterministic indices and times from the registered 361 grid."""
    if time_count < 2:
        raise ValueError("time_count must be at least 2")
    full = np.arange(20.0, 200.0 + 1.0e-9, 0.5)
    indices = np.unique(np.rint(np.linspace(0, len(full) - 1,
                                           time_count)).astype(int))
    if len(indices) != time_count:
        raise ValueError("rounded time selection produced duplicate indices")
    return indices, full[indices]


def hermitize_and_project(rho: np.ndarray) -> tuple[np.ndarray, dict[str, float]]:
    """Hermitize, clip to the PSD cone, normalize, and return diagnostics."""
    raw = np.asarray(rho, dtype=complex)
    if raw.shape != (4, 4):
        raise ValueError("pair RDM must have shape (4, 4)")
    herm = 0.5 * (raw + raw.conj().T)
    trace_raw = float(np.trace(herm).real)
    vals, vecs = np.linalg.eigh(herm)
    clipped = np.clip(vals, 0.0, None)
    if float(clipped.sum()) <= 0.0:
        raise ValueError("PSD projection has zero trace")
    projected = (vecs * clipped[None, :]) @ vecs.conj().T
    projected /= np.trace(projected)
    return projected, {
        "trace_raw": trace_raw,
        "min_eigenvalue_raw": float(vals.min()),
        "projection_fro": float(np.linalg.norm(projected - raw)),
    }


def reconstruct_pair_rdm(
    expectations: Mapping[tuple[str, str], float],
) -> np.ndarray:
    """Reconstruct a two-site RDM from all I/X/Y/Z Pauli expectations."""
    required = {(a, b) for a in PAULI for b in PAULI}
    missing = required.difference(expectations)
    if missing:
        raise ValueError(f"missing Pauli expectations: {sorted(missing)}")
    rho = np.zeros((4, 4), dtype=complex)
    for a, b in sorted(required):
        rho += float(expectations[(a, b)]) * np.kron(PAULI[a], PAULI[b])
    return 0.25 * rho


def _entropy(rho: np.ndarray) -> float:
    vals = np.linalg.eigvalsh(0.5 * (rho + rho.conj().T))
    vals = vals[vals > 1.0e-14]
    return float(-np.sum(vals * np.log(vals)))


def _floyd_warshall(weights: np.ndarray) -> np.ndarray:
    distances = np.asarray(weights, dtype=float).copy()
    np.fill_diagonal(distances, 0.0)
    for k in range(len(distances)):
        distances = np.minimum(
            distances,
            distances[:, k:k + 1] + distances[k:k + 1, :],
        )
    return distances


def metric_from_pair_rdms(
    pair_rdms: Mapping[tuple[int, int], np.ndarray],
    n_sites: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Apply the paper's natural-log MI and shortest-path metric exactly."""
    expected = {(i, j) for i in range(n_sites) for j in range(i + 1, n_sites)}
    if set(pair_rdms) != expected:
        raise ValueError("pair_rdms must contain every i<j pair exactly once")
    mi = np.zeros((n_sites, n_sites), dtype=float)
    for (i, j), rho4 in pair_rdms.items():
        rho4 = np.asarray(rho4, dtype=complex).reshape(2, 2, 2, 2)
        rho_i = np.trace(rho4, axis1=1, axis2=3)
        rho_j = np.trace(rho4, axis1=0, axis2=2)
        value = max(_entropy(rho_i) + _entropy(rho_j)
                    - _entropy(rho4.reshape(4, 4)), 0.0)
        mi[i, j] = mi[j, i] = value
    normalized = np.clip(mi / I0, X_MIN, 1.0)
    weights = -np.log(normalized)
    np.fill_diagonal(weights, 0.0)
    return mi, _floyd_warshall(weights)


def canonical_json_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False).encode("utf-8")


def canonical_json_sha256(value: object) -> str:
    return sha256(canonical_json_bytes(value)).hexdigest()
