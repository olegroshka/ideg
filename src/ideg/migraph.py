"""The emergent-geometry functional Phi (AR-009 spec §2, frozen).

Verified TH-037 construction (SRC-049 eqs. 13-14): pairwise mutual
information -> weights w = -ln(I / I0) with cap -> shortest-path distance
matrix. I0 = 2 ln 2 (qubit pair maximum); x floored at X_MIN = 1e-6."""

from __future__ import annotations

import numpy as np

I0 = 2.0 * np.log(2.0)
X_MIN = 1.0e-6
W_MAX = -np.log(X_MIN)


def _vn_entropy(rho: np.ndarray) -> float:
    lam = np.linalg.eigvalsh(rho)
    lam = lam[lam > 1e-14]
    return float(-np.sum(lam * np.log(lam)))


def pair_rdm(psi: np.ndarray, n: int, i: int, j: int) -> np.ndarray:
    """Two-site RDM of a pure state (site 0 = most significant factor)."""
    t = psi.reshape([2] * n)
    t = np.moveaxis(t, (i, j), (0, 1)).reshape(4, -1)
    return t @ t.conj().T


_GATHER_CACHE: dict = {}


def _pair_gather_indices(n: int, i: int, j: int) -> np.ndarray:
    """(4, 2^(n-2)) basis indices grouped by the (s_i, s_j) configuration,
    each group ordered identically by the remaining ('rest') bits."""
    key = (n, i, j)
    if key in _GATHER_CACHE:
        return _GATHER_CACHE[key]

    def insert_bit(x: np.ndarray, pos: int, b: int) -> np.ndarray:
        low = x & ((1 << pos) - 1)
        high = x >> pos
        return (high << (pos + 1)) | (b << pos) | low

    p_i, p_j = n - 1 - i, n - 1 - j  # bit positions (site 0 = MSB)
    p_hi, p_lo = max(p_i, p_j), min(p_i, p_j)
    rest = np.arange(2 ** (n - 2))
    groups = []
    for s_i in (0, 1):
        for s_j in (0, 1):
            b_hi = s_i if p_i == p_hi else s_j
            b_lo = s_j if p_i == p_hi else s_i
            groups.append(insert_bit(insert_bit(rest, p_lo, b_lo),
                                     p_hi, b_hi))
    out = np.array(groups)
    _GATHER_CACHE[key] = out
    return out


def pair_rdm_mixed(rho: np.ndarray, n: int, i: int, j: int) -> np.ndarray:
    """Two-site RDM of a density matrix via cached index gathers (fast)."""
    g = _pair_gather_indices(n, i, j)
    rho4 = np.empty((4, 4), dtype=complex)
    for a in range(4):
        for b in range(4):
            rho4[a, b] = np.sum(rho[g[a], g[b]])
    return rho4


def _single_entropies_from_pair(rho4: np.ndarray):
    r = rho4.reshape(2, 2, 2, 2)
    rho_a = np.trace(r, axis1=1, axis2=3)
    rho_b = np.trace(r, axis1=0, axis2=2)
    return _vn_entropy(rho_a), _vn_entropy(rho_b)


def mutual_information_matrix(state: np.ndarray, n: int,
                              mixed: bool = False) -> np.ndarray:
    """I(i:j) = S_i + S_j - S_ij for all pairs (natural log)."""
    mi = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            rho4 = pair_rdm_mixed(state, n, i, j) if mixed \
                else pair_rdm(state, n, i, j)
            s_i, s_j = _single_entropies_from_pair(rho4)
            s_ij = _vn_entropy(rho4)
            mi[i, j] = mi[j, i] = max(s_i + s_j - s_ij, 0.0)
    return mi


def floyd_warshall(w: np.ndarray) -> np.ndarray:
    d = w.copy()
    np.fill_diagonal(d, 0.0)
    n = d.shape[0]
    for k in range(n):
        d = np.minimum(d, d[:, k:k + 1] + d[k:k + 1, :])
    return d


def phi_distance_matrix(mi: np.ndarray) -> np.ndarray:
    """Spec §2 steps 2-4: normalize, cap, weight, shortest path."""
    x = np.clip(mi / I0, X_MIN, 1.0)
    w = -np.log(x)
    np.fill_diagonal(w, 0.0)
    return floyd_warshall(w)


def phi_series(states, n: int, mixed: bool = False) -> np.ndarray:
    """(T, n, n) stack of distance matrices for a state trajectory."""
    return np.array([phi_distance_matrix(
        mutual_information_matrix(s, n, mixed=mixed)) for s in states])


def delta_phi(d_series: np.ndarray, d_ref: np.ndarray | None = None):
    """Spec §2 drift: dPhi(t) = ||D(t) - Dbar||_F / ||Dbar||_F.

    `d_ref` defaults to the series' own window mean; for perturbed runs pass
    the UNPERTURBED run's window mean (session-log clarification)."""
    dbar = d_series.mean(axis=0) if d_ref is None else d_ref
    denom = np.linalg.norm(dbar)
    return np.array([np.linalg.norm(d - dbar) / denom for d in d_series]), dbar


def above_cap_mask(mi_bar: np.ndarray) -> np.ndarray:
    """Pairs whose mean normalized MI exceeds X_MIN (cap diagnostic, spec §2)."""
    x = mi_bar / I0
    mask = x > X_MIN
    np.fill_diagonal(mask, False)
    return mask


def delta_phi_subgraph(d_series: np.ndarray, dbar: np.ndarray,
                       mask: np.ndarray) -> np.ndarray:
    """Cap diagnostic: drift restricted to the above-cap pair set."""
    denom = np.linalg.norm(dbar[mask])
    if denom == 0.0:
        return np.zeros(len(d_series))
    return np.array([np.linalg.norm((d - dbar)[mask]) / denom
                     for d in d_series])
