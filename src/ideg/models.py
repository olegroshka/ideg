"""Hamiltonians and Floquet drives of the AR-009 spec (frozen §1).

All chains are open-boundary, J = 1 units, spec conventions §0."""

from __future__ import annotations

import numpy as np
import scipy.sparse as sp

from .pauli import SX, SY, SZ, op_on, sz_diag


def _dense(h: sp.spmatrix) -> np.ndarray:
    h = h.toarray()
    assert np.allclose(h.imag, 0.0, atol=1e-12), "expected a real Hamiltonian"
    return np.ascontiguousarray(h.real)


def tfim(n: int, g: float = 1.5) -> np.ndarray:
    """T-A(i): H = -sum sz sz - g sum sx (gapped for g=1.5)."""
    h = sp.csr_matrix((2**n, 2**n))
    for i in range(n - 1):
        h = h - op_on(n, {i: SZ, i + 1: SZ})
    for i in range(n):
        h = h - g * op_on(n, {i: SX})
    return _dense(h)


def xx_chain(n: int) -> np.ndarray:
    """T-A(ii)/T-C integrable: H = sum (sx sx + sy sy)/2."""
    h = sp.csr_matrix((2**n, 2**n))
    for i in range(n - 1):
        h = h + 0.5 * (op_on(n, {i: SX, i + 1: SX}) + op_on(n, {i: SY, i + 1: SY}))
    return _dense(h)


def mixed_field_ising(n: int, hx: float = 0.9045, hz: float = 0.8090) -> np.ndarray:
    """T-A(iii)/T-C scrambling: H = sum sz sz + hx sum sx + hz sum sz."""
    h = sp.csr_matrix((2**n, 2**n))
    for i in range(n - 1):
        h = h + op_on(n, {i: SZ, i + 1: SZ})
    for i in range(n):
        h = h + hx * op_on(n, {i: SX}) + hz * op_on(n, {i: SZ})
    return _dense(h)


def ferro_ising_weak_tf(n: int, g: float = 0.05,
                        dg: np.ndarray | None = None) -> np.ndarray:
    """T-A(iv): H = -sum sz sz - sum (g + dg_i) sx  (quasi-degenerate doublet).

    `dg` is the per-site weak-disorder dressing of the ensemble (spec §1)."""
    h = sp.csr_matrix((2**n, 2**n))
    for i in range(n - 1):
        h = h - op_on(n, {i: SZ, i + 1: SZ})
    for i in range(n):
        gi = g + (0.0 if dg is None else float(dg[i]))
        h = h - gi * op_on(n, {i: SX})
    return _dense(h)


def xxz_disordered(n: int, rng: np.random.Generator, delta: float = 1.0,
                   w: float = 8.0) -> np.ndarray:
    """T-C localized: H = sum (sx sx + sy sy + delta sz sz) + sum h_i sz."""
    fields = rng.uniform(-w, w, size=n)
    h = sp.csr_matrix((2**n, 2**n))
    for i in range(n - 1):
        h = h + (op_on(n, {i: SX, i + 1: SX}) + op_on(n, {i: SY, i + 1: SY})
                 + delta * op_on(n, {i: SZ, i + 1: SZ}))
    for i in range(n):
        h = h + fields[i] * op_on(n, {i: SZ})
    return _dense(h)


def floquet_dtc(n: int, eps: float, rng: np.random.Generator,
                interactions: bool = True, disorder: bool = True):
    """T-B drive: U_F = exp(-i H2 t2) exp(-i H1 t1), t1 = t2 = 1 (spec §1).

    H1 = (pi/2)(1 - eps) sum sy    -> per-site y-rotation (exact kron form)
    H2 = sum J_i sz sz + sum h_i sz -> diagonal phase
    J_i ~ U([0.05, 0.15] pi) (or 0), h_i ~ U([0, pi]) (or 0).

    Returns (U_F, h2_diag) with U_F dense complex, h2_diag the diagonal of H2."""
    dim = 2**n
    theta = 0.5 * np.pi * (1.0 - eps)
    r = np.array([[np.cos(theta), -np.sin(theta)],
                  [np.sin(theta), np.cos(theta)]])  # exp(-i theta sy) is real
    rot = np.array([[1.0]])
    for _ in range(n):
        rot = np.kron(rot, r)

    # draws are unconditional so comparator regimes (r1/r2) share the same
    # realization stream as the DTC regime at equal seed (paired design);
    # draw order matches the original (J then h), so eps-regime realizations
    # are unchanged
    j = rng.uniform(0.05 * np.pi, 0.15 * np.pi, size=n - 1)
    hz = rng.uniform(0.0, np.pi, size=n)
    if not interactions:
        j = np.zeros(n - 1)
    if not disorder:
        hz = np.zeros(n)
    h2 = np.zeros(dim)
    for i in range(n - 1):
        h2 += j[i] * sz_diag(n, i) * sz_diag(n, i + 1)
    for i in range(n):
        h2 += hz[i] * sz_diag(n, i)

    u_f = np.exp(-1.0j * h2)[:, None] * rot
    return u_f, h2
