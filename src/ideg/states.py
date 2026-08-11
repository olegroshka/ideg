"""Initial-state ensembles of the AR-009 spec (frozen §1)."""

from __future__ import annotations

from fractions import Fraction

import numpy as np


def ground_state(h: np.ndarray) -> np.ndarray:
    evals, evecs = np.linalg.eigh(h)
    return np.ascontiguousarray(evecs[:, 0].astype(complex))


def all_up(n: int) -> np.ndarray:
    psi = np.zeros(2**n, dtype=complex)
    psi[0] = 1.0  # bit 0 = up at every site
    return psi


def neel(n: int) -> np.ndarray:
    """|up down up down ...> (site 0 = most significant bit)."""
    idx = 0
    for site in range(n):
        if site % 2 == 1:
            idx |= 1 << (n - 1 - site)
    psi = np.zeros(2**n, dtype=complex)
    psi[idx] = 1.0
    return psi


def haar_product_state(n: int, rng: np.random.Generator) -> np.ndarray:
    psi = np.array([1.0], dtype=complex)
    for _ in range(n):
        v = rng.normal(size=2) + 1.0j * rng.normal(size=2)
        v /= np.linalg.norm(v)
        psi = np.kron(psi, v)
    return psi


def z_product_state(n: int, rng: np.random.Generator) -> np.ndarray:
    idx = 0
    for site in range(n):
        if rng.integers(2):
            idx |= 1 << (n - 1 - site)
    psi = np.zeros(2**n, dtype=complex)
    psi[idx] = 1.0
    return psi


def _is_commensurate(ratio: float, qmax: int = 50, tol: float = 1e-3) -> bool:
    frac = Fraction(ratio).limit_denominator(qmax)
    return abs(ratio - float(frac)) < tol


def magnon_superposition(n: int, rng: np.random.Generator,
                         n_modes: int = 3, max_tries: int = 200):
    """T-A(ii): equal-weight superposition of `n_modes` single-magnon XX
    eigenstates whose two independent Bohr-frequency gaps have an
    incommensurate ratio (no p/q, q <= 50, within 1e-3; spec §1).

    Single-magnon sector of the open XX chain = one down spin hopping with
    amplitude 1; modes/energies from the n x n hopping matrix (numerical,
    no literature formula relied on).

    Returns (psi, energies_of_modes)."""
    hop = np.zeros((n, n))
    for i in range(n - 1):
        hop[i, i + 1] = hop[i + 1, i] = 1.0
    e1, v1 = np.linalg.eigh(hop)  # single-particle modes phi_k(site)

    # magnon basis states: down spin at `site` on the all-up background;
    # XX chain energy of the 1-magnon state relative to the background is
    # the single-particle eigenvalue (background itself has E = 0 blocks
    # handled by working entirely inside the sector).
    for _ in range(max_tries):
        modes = rng.choice(n, size=n_modes, replace=False)
        e = np.sort(e1[modes])
        g1, g2 = e[1] - e[0], e[2] - e[1]
        if abs(g1) < 1e-9 or abs(g2) < 1e-9:
            continue
        if not _is_commensurate(g1 / g2):
            psi = np.zeros(2**n, dtype=complex)
            phases = np.exp(2.0j * np.pi * rng.random(n_modes))
            for m, ph in zip(modes, phases):
                for site in range(n):
                    idx = 1 << (n - 1 - site)  # one down spin at `site`
                    psi[idx] += ph * v1[site, m]
            psi /= np.linalg.norm(psi)
            return psi, e1[modes]
    raise RuntimeError("no incommensurate magnon triple found")
