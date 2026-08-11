"""CON-034 witness battery W1-W5 (AR-009 spec §3, frozen).

W1 Bohr spectral measure includes the m = n weight at omega = 0 so that an
exact eigenstate gives PR_A = 1 (session-log clarification of the §3
formula; matches the spec's own §5.1 class-(i) prediction)."""

from __future__ import annotations

import numpy as np

from .evolve import EigenEvolver
from .pauli import sz_diag


def bohr_measure_pr(evolver: EigenEvolver, psi0: np.ndarray,
                    bin_width: float = 1e-3) -> float:
    """W1: participation ratio of the binned Bohr spectral measure
    A(w) = sum_{m,n} p_m p_n delta(w - |E_m - E_n|), including m = n."""
    p = np.abs(evolver.coeffs(psi0)) ** 2
    keep = p > 1e-12
    p = p[keep]
    e = evolver.evals[keep]
    freqs = np.abs(e[:, None] - e[None, :]).ravel()
    weights = (p[:, None] * p[None, :]).ravel()
    bins = np.round(freqs / bin_width).astype(np.int64)
    a = {}
    for b, w in zip(bins, weights):
        a[b] = a.get(b, 0.0) + w
    vals = np.array(list(a.values()))
    return float(vals.sum() ** 2 / np.sum(vals ** 2))


def recurrence_distance(states: np.ndarray, ref_index: int = 0) -> np.ndarray:
    """W2: d_phys(t) = 1 - |<psi(t_ref)|psi(t)>|^2 along a trajectory."""
    ref = states[ref_index]
    overlaps = np.abs(states @ ref.conj()) ** 2
    return 1.0 - overlaps


def otoc(evolver: EigenEvolver, psi: np.ndarray, n: int, site_w: int,
         site_v: int, times: np.ndarray) -> np.ndarray:
    """W3: C(t) = 1/2 <psi| [W(t), V]^dag [W(t), V] |psi>, W = Z_w, V = Z_v."""
    zw = sz_diag(n, site_w)
    zv = sz_diag(n, site_v)
    out = np.empty(len(times))
    v_psi = zv * psi
    for k, t in enumerate(times):
        a = evolver.apply_heisenberg(zw, t, v_psi)          # W(t) V |psi>
        b = zv * evolver.apply_heisenberg(zw, t, psi)       # V W(t) |psi>
        out[k] = 0.5 * float(np.linalg.norm(a - b) ** 2)
    return out


def otoc_stats(c_rt: np.ndarray, times: np.ndarray,
               arrival_threshold: float = 0.1):
    """Saturation value (mean over last quarter) and arrival time t*."""
    q = len(times) // 4
    c_sat = float(np.mean(c_rt[-q:]))
    above = np.nonzero(c_rt >= arrival_threshold)[0]
    t_star = float(times[above[0]]) if len(above) else float("inf")
    return c_sat, t_star


def xi_offdiagonal_pure(evolver: EigenEvolver, psi0: np.ndarray) -> float:
    """W4 for a pure state: Xi = sum_{m != n} p_m p_n = 1 - sum p_n^2."""
    p = np.abs(evolver.coeffs(psi0)) ** 2
    return float(1.0 - np.sum(p ** 2))


def xi_offdiagonal_rho(evolver: EigenEvolver, rho: np.ndarray) -> float:
    """W4 for a density matrix: sum_{m != n} |rho_mn|^2 in the H eigenbasis."""
    r = evolver.evecs.conj().T @ rho @ evolver.evecs
    off = np.sum(np.abs(r) ** 2) - np.sum(np.abs(np.diag(r)) ** 2)
    return float(off)


def subharmonic_peak(mag_series: np.ndarray) -> float:
    """W5: normalized Fourier power of a stroboscopic magnetization series
    at half the drive frequency (period-2T line). Series shape (M,) or
    (M, n_sites) -> site-averaged."""
    m = np.atleast_2d(mag_series.T).T  # (M, sites)
    m = m - m.mean(axis=0, keepdims=True)
    spec = np.abs(np.fft.rfft(m, axis=0)) ** 2
    total = spec.sum(axis=0)
    total[total == 0.0] = 1.0
    half_index = m.shape[0] // 2  # rfft bin at f = 1/2 per-period sampling
    if half_index >= spec.shape[0]:
        half_index = spec.shape[0] - 1
    frac = spec[half_index] / total
    return float(np.mean(frac))
