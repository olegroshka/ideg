"""Time evolution: eigenbasis propagation, Floquet stroboscopics, dephasing.

Clock: external lab clock throughout (spec §0, scope-noted)."""

from __future__ import annotations

import numpy as np

from .pauli import hamming_matrix


class EigenEvolver:
    """Pure-state evolution via one-time eigendecomposition of H."""

    def __init__(self, h: np.ndarray):
        self.evals, self.evecs = np.linalg.eigh(h)

    def coeffs(self, psi0: np.ndarray) -> np.ndarray:
        """Energy-eigenbasis coefficients c_n of psi0."""
        return self.evecs.conj().T @ psi0

    def state_at(self, psi0: np.ndarray, t: float) -> np.ndarray:
        c = self.coeffs(psi0)
        return self.evecs @ (np.exp(-1.0j * self.evals * t) * c)

    def states_at(self, psi0: np.ndarray, times: np.ndarray) -> np.ndarray:
        """(len(times), dim) array of states."""
        c = self.coeffs(psi0)
        phases = np.exp(-1.0j * np.outer(times, self.evals))
        return (phases * c[None, :]) @ self.evecs.T

    def unitary_at(self, t: float) -> np.ndarray:
        return (self.evecs * np.exp(-1.0j * self.evals * t)[None, :]) \
            @ self.evecs.conj().T

    def apply_heisenberg(self, w_diag: np.ndarray, t: float,
                         phi: np.ndarray) -> np.ndarray:
        """Apply W(t) = U(t)^dag W U(t) (W diagonal in the site basis) to phi."""
        c = self.evecs.conj().T @ phi
        c *= np.exp(-1.0j * self.evals * t)
        v = self.evecs @ c            # U(t) phi
        v *= w_diag                   # W U(t) phi
        c = self.evecs.conj().T @ v
        c *= np.exp(+1.0j * self.evals * t)
        return self.evecs @ c         # U(t)^dag W U(t) phi

    def rho_stream(self, rho0: np.ndarray, times: np.ndarray):
        """Yield (t, rho(t)) for density-matrix evolution under H
        (one eigenbasis transform up front, per-sample phase mask + back)."""
        r_e = self.evecs.conj().T @ rho0 @ self.evecs
        for t in times:
            ph = np.exp(-1.0j * self.evals * t)
            r_t = (ph[:, None] * r_e) * ph.conj()[None, :]
            yield t, self.evecs @ r_t @ self.evecs.conj().T


def floquet_states(u_f: np.ndarray, psi0: np.ndarray,
                   n_periods: int) -> np.ndarray:
    """Stroboscopic states psi(nT), n = 0..n_periods (inclusive)."""
    out = np.empty((n_periods + 1, len(psi0)), dtype=complex)
    out[0] = psi0
    psi = psi0.copy()
    for k in range(1, n_periods + 1):
        psi = u_f @ psi
        out[k] = psi
    return out


class FloquetDephasingEvolver:
    """T-B density-matrix stroboscopics: one Floquet period U_F then the exact
    per-period dephasing damping mask exp(-2 gamma T_period d_H). gamma is in
    lab-time units (matching T-A/T-C); T_period = t1 + t2 = 2 (spec §1 T-B).
    Descriptive-protocol use only (manifest-recorded implementation choice)."""

    def __init__(self, u_f: np.ndarray, n_sites: int, gamma: float,
                 t_period: float = 2.0):
        self.u_f = u_f
        self.mask = np.exp(-2.0 * gamma * t_period
                           * hamming_matrix(n_sites).astype(float))

    def run(self, rho0: np.ndarray, n_periods: int, sample_every: int = 1):
        rho = rho0.copy()
        for k in range(1, n_periods + 1):
            rho = (self.u_f @ rho @ self.u_f.conj().T) * self.mask
            if k % sample_every == 0:
                yield k, rho


class DephasingEvolver:
    """Density-matrix evolution under H with local sigma^z dephasing rate gamma.

    Trotter step: exact unitary half-step handling via precomputed U(dt),
    then the exact dephasing damping mask exp(-2 gamma dt d_H(a, b)) —
    exact for the commuting pure-dephasing Lindblad part; splitting error
    O(dt^2) (pilot/exploratory use recorded in the session log)."""

    def __init__(self, h: np.ndarray, n_sites: int, gamma: float,
                 dt: float = 0.5):
        ev = EigenEvolver(h)
        self.u_dt = ev.unitary_at(dt)
        self.mask = np.exp(-2.0 * gamma * dt
                           * hamming_matrix(n_sites).astype(float))
        self.dt = dt

    def step(self, rho: np.ndarray) -> np.ndarray:
        rho = self.u_dt @ rho @ self.u_dt.conj().T
        return rho * self.mask

    def run(self, rho0: np.ndarray, n_steps: int,
            sample_every: int = 1):
        """Yield (step_index, rho) at the requested sampling stride."""
        rho = rho0.copy()
        for k in range(1, n_steps + 1):
            rho = self.step(rho)
            if k % sample_every == 0:
                yield k, rho
