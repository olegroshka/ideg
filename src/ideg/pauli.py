"""Operator construction for small spin-1/2 chains (dense, N <= 12)."""

from __future__ import annotations

import numpy as np
import scipy.sparse as sp

I2 = sp.identity(2, format="csr")
SX = sp.csr_matrix(np.array([[0.0, 1.0], [1.0, 0.0]]))
SY = sp.csr_matrix(np.array([[0.0, -1.0j], [1.0j, 0.0]]))
SZ = sp.csr_matrix(np.array([[1.0, 0.0], [0.0, -1.0]]))


def op_on(n_sites: int, site_ops: dict) -> sp.csr_matrix:
    """Tensor product operator with `site_ops[i]` at site i, identity elsewhere.

    Site 0 is the leftmost (most significant bit of the basis index)."""
    out = sp.identity(1, format="csr")
    for i in range(n_sites):
        out = sp.kron(out, site_ops.get(i, I2), format="csr")
    return out


def sz_diag(n_sites: int, site: int) -> np.ndarray:
    """Diagonal of sigma^z_site in the computational basis (cheap)."""
    dim = 2**n_sites
    idx = np.arange(dim)
    bit = (idx >> (n_sites - 1 - site)) & 1
    return 1.0 - 2.0 * bit  # bit 0 -> +1 (up), bit 1 -> -1 (down)


def hamming_matrix(n_sites: int) -> np.ndarray:
    """d_H(a, b) between computational basis states (uint8, dim x dim)."""
    dim = 2**n_sites
    idx = np.arange(dim)
    x = idx[:, None] ^ idx[None, :]
    d = np.zeros((dim, dim), dtype=np.uint8)
    for s in range(n_sites):
        d += ((x >> s) & 1).astype(np.uint8)
    return d


def reflection_permutation(n_sites: int) -> np.ndarray:
    """Index permutation of the site-reversal (parity) operator."""
    dim = 2**n_sites
    perm = np.zeros(dim, dtype=np.int64)
    for a in range(dim):
        b = 0
        for s in range(n_sites):
            if (a >> s) & 1:
                b |= 1 << (n_sites - 1 - s)
        perm[a] = b
    return perm


def reflection_sector_basis(n_sites: int, even: bool = True) -> np.ndarray:
    """Orthonormal basis (columns) of the reflection-even/odd subspace."""
    dim = 2**n_sites
    perm = reflection_permutation(n_sites)
    cols = []
    for a in range(dim):
        b = perm[a]
        if a < b:
            v = np.zeros(dim)
            v[a] = 1.0 / np.sqrt(2.0)
            v[b] = (1.0 if even else -1.0) / np.sqrt(2.0)
            cols.append(v)
        elif a == b and even:
            v = np.zeros(dim)
            v[a] = 1.0
            cols.append(v)
    return np.array(cols).T


def sz_sector_indices(n_sites: int, n_down: int) -> np.ndarray:
    """Basis indices with exactly n_down down spins (set bits)."""
    idx = np.arange(2**n_sites)
    pop = np.zeros_like(idx)
    for s in range(n_sites):
        pop += (idx >> s) & 1
    return idx[pop == n_down]
