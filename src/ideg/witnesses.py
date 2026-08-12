"""CON-034 witness battery W1-W5 (AR-009 spec §3, frozen).

W1 Bohr spectral measure includes the m = n weight at omega = 0 so that an
exact eigenstate gives PR_A = 1 (session-log clarification of the §3
formula; matches the spec's own §5.1 class-(i) prediction)."""

from __future__ import annotations

import numpy as np

from .evolve import EigenEvolver
from .pauli import sz_diag


def _binned_pr(freqs_fn, p: np.ndarray, bin_width: float,
               n_bins: int, chunk: int = 256) -> float:
    """PR of a binned line measure; freqs_fn(i0, i1) yields the |gap| block
    for rows i0:i1 against all columns. Vectorized bincount accumulation
    (identical sums to the original dict loop; zero bins drop out of PR)."""
    acc = np.zeros(n_bins)
    m = len(p)
    for i0 in range(0, m, chunk):
        i1 = min(i0 + chunk, m)
        f = freqs_fn(i0, i1)
        w = p[i0:i1, None] * p[None, :]
        b = np.round(f / bin_width).astype(np.int64).ravel()
        acc += np.bincount(b, weights=w.ravel(), minlength=n_bins)
    return float(acc.sum() ** 2 / np.sum(acc ** 2))


def bohr_measure_pr(evolver: EigenEvolver, psi0: np.ndarray,
                    bin_width: float = 1e-3) -> float:
    """W1: participation ratio of the binned Bohr spectral measure
    A(w) = sum_{m,n} p_m p_n delta(w - |E_m - E_n|), including m = n."""
    p = np.abs(evolver.coeffs(psi0)) ** 2
    keep = p > 1e-12
    p = p[keep]
    e = evolver.evals[keep]
    span = float(e.max() - e.min()) if len(e) > 1 else 0.0
    n_bins = int(round(span / bin_width)) + 2
    return _binned_pr(lambda i0, i1: np.abs(e[i0:i1, None] - e[None, :]),
                      p, bin_width, n_bins)


def floquet_eigenbasis(u_f: np.ndarray):
    """Quasienergies theta in (-pi, pi] and orthonormal Floquet eigenbasis
    (columns) via complex Schur (exact eigenbasis for a normal matrix)."""
    from scipy.linalg import schur
    t, z = schur(u_f, output="complex")
    theta = -np.angle(np.diag(t))
    return theta, z


def bohr_measure_pr_floquet(theta: np.ndarray, evecs: np.ndarray,
                            psi0: np.ndarray,
                            bin_width: float = 1e-3) -> float:
    """W1 for T-B: binned measure over circular quasienergy gaps
    |theta_m - theta_n| taken as the principal value in [0, pi]."""
    p = np.abs(evecs.conj().T @ psi0) ** 2
    keep = p > 1e-12
    p = p[keep]
    th = theta[keep]
    n_bins = int(round(np.pi / bin_width)) + 2

    def gaps(i0, i1):
        d = np.abs(th[i0:i1, None] - th[None, :])
        return np.minimum(d, 2.0 * np.pi - d)

    return _binned_pr(gaps, p, bin_width, n_bins)


def recurrence_distance(states: np.ndarray, ref_index: int = 0) -> np.ndarray:
    """W2: d_phys(t) = 1 - |<psi(t_ref)|psi(t)>|^2 along a trajectory."""
    ref = states[ref_index]
    overlaps = np.abs(states @ ref.conj()) ** 2
    return 1.0 - overlaps


def otoc_series(evolver: EigenEvolver, psi: np.ndarray, n: int,
                site_v: int, sites_w, times: np.ndarray) -> np.ndarray:
    """W3, batched: C(w, t) = 1/2 || [W(t), V] |psi> ||^2 for W = Z_w over
    `sites_w`, V = Z_{site_v}, all `times` at once (BLAS matmuls; identical
    values to the per-time evolver loop)."""
    v = evolver.evecs
    e = evolver.evals
    fwd = np.exp(-1.0j * np.outer(times, e))     # (T, dim) phases of U(t)
    zv = sz_diag(n, site_v)

    def u_t(vec):
        """U(t) vec for all t -> (T, dim) in the site basis."""
        return (fwd * (v.conj().T @ vec)[None, :]) @ v.T

    def u_dag_t(rows):
        """U(t)^dag applied row-wise to a (T, dim) site-basis array."""
        return ((rows @ v.conj()) * fwd.conj()) @ v.T

    s_v = u_t(zv * psi)                          # U(t) V |psi>
    s_0 = u_t(psi)                               # U(t) |psi>
    out = np.empty((len(sites_w), len(times)))
    for k, sw in enumerate(sites_w):
        zw = sz_diag(n, sw)
        a = u_dag_t(zw[None, :] * s_v)           # W(t) V |psi>
        b = zv[None, :] * u_dag_t(zw[None, :] * s_0)  # V W(t) |psi>
        out[k] = 0.5 * np.linalg.norm(a - b, axis=1) ** 2
    return out


def otoc(evolver: EigenEvolver, psi: np.ndarray, n: int, site_w: int,
         site_v: int, times: np.ndarray) -> np.ndarray:
    """W3: C(t) = 1/2 <psi| [W(t), V]^dag [W(t), V] |psi>, W = Z_w, V = Z_v."""
    return otoc_series(evolver, psi, n, site_v, [site_w], times)[0]


def otoc_stats(c_rt: np.ndarray, times: np.ndarray,
               arrival_threshold: float = 0.1):
    """Saturation value (mean over last quarter) and arrival time t*."""
    q = len(times) // 4
    c_sat = float(np.mean(c_rt[-q:]))
    above = np.nonzero(c_rt >= arrival_threshold)[0]
    t_star = float(times[above[0]]) if len(above) else float("inf")
    return c_sat, t_star


def _level_starts(evals: np.ndarray, tol: float = 1e-10) -> np.ndarray:
    """Group indices of (sorted) eigenvalues into degenerate levels; returns
    the group label of each index."""
    gaps = np.diff(evals) > tol
    return np.concatenate([[0], np.cumsum(gaps)])


def xi_offdiagonal_pure(evolver: EigenEvolver, psi0: np.ndarray,
                        degeneracy_tol: float = 1e-10) -> float:
    """W4 for a pure state: Xi = sum over ENERGY-DISTINCT pairs p_m p_n
    = 1 - sum_levels P_level^2. Degenerate levels are grouped so that the
    spec's defining property (Xi > 0 iff the state moves under H) holds for
    degenerate spectra: coherence inside a degenerate level is stationary."""
    p = np.abs(evolver.coeffs(psi0)) ** 2
    labels = _level_starts(evolver.evals, degeneracy_tol)
    p_level = np.bincount(labels, weights=p)
    return float(1.0 - np.sum(p_level ** 2))


def xi_offdiagonal_rho(evolver: EigenEvolver, rho: np.ndarray,
                       degeneracy_tol: float = 1e-10) -> float:
    """W4 for a density matrix: sum |rho_mn|^2 over energy-distinct pairs
    (m, n) in the H eigenbasis (same degeneracy grouping as the pure case)."""
    r = evolver.evecs.conj().T @ rho @ evolver.evecs
    labels = _level_starts(evolver.evals, degeneracy_tol)
    a2 = np.abs(r) ** 2
    # levels are contiguous runs of the sorted spectrum
    bounds = np.concatenate([[0], np.nonzero(np.diff(labels))[0] + 1,
                             [len(labels)]])
    same_level = sum(float(np.sum(a2[b0:b1, b0:b1]))
                     for b0, b1 in zip(bounds[:-1], bounds[1:]))
    return float(np.sum(a2) - same_level)


def xi_offdiagonal_pure_floquet(theta: np.ndarray, evecs: np.ndarray,
                                psi0: np.ndarray,
                                degeneracy_tol: float = 1e-10) -> float:
    """W4 for T-B: quasienergy-distinct pairs (circular grouping by sorted
    theta; the 2pi wrap-around join is negligible for generic disorder)."""
    p = np.abs(evecs.conj().T @ psi0) ** 2
    order = np.argsort(theta)
    labels = _level_starts(theta[order], degeneracy_tol)
    p_level = np.bincount(labels, weights=p[order])
    return float(1.0 - np.sum(p_level ** 2))


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
