"""Comparators and perturbation protocols (AR-009 spec §4, §5.2, frozen)."""

from __future__ import annotations

import numpy as np

from .evolve import DephasingEvolver, EigenEvolver
from .migraph import (delta_phi, mutual_information_matrix,
                      phi_distance_matrix, phi_series)
from .pauli import sz_diag


def diagonal_ensemble(evolver: EigenEvolver, psi0: np.ndarray) -> np.ndarray:
    """Stationary-state comparator (§4.1): rho_bar = sum p_n |n><n|."""
    p = np.abs(evolver.coeffs(psi0)) ** 2
    return (evolver.evecs * p[None, :]) @ evolver.evecs.conj().T


def dephase_to_diagonal(evolver: EigenEvolver, psi: np.ndarray) -> np.ndarray:
    """Switch-off operation (§4.2): kill all motion, keep populations."""
    return diagonal_ensemble(evolver, psi)


def quench_run(h: np.ndarray, evolver: EigenEvolver, psi0: np.ndarray,
               lam: float, site: int, n_sites: int, t_p: float,
               sample_times_post: np.ndarray) -> np.ndarray:
    """§5.2 protocol 1: evolve under H to t_p, then under H' = H + lam Z_site.

    Returns the post-t_p trajectory at t_p + sample_times_post."""
    psi_tp = evolver.state_at(psi0, t_p)
    h_pert = h + np.diag(lam * sz_diag(n_sites, site))
    ev_pert = EigenEvolver(h_pert)
    return ev_pert.states_at(psi_tp, sample_times_post)


def dephasing_run(h: np.ndarray, evolver: EigenEvolver, psi0: np.ndarray,
                  gamma: float, n_sites: int, t_p: float, t_end: float,
                  dt: float = 0.5, sample_every: int = 1):
    """§5.2 protocol 2: pure evolution to t_p, then dephasing channel on.

    Yields (t, rho) samples for t in (t_p, t_end]."""
    psi_tp = evolver.state_at(psi0, t_p)
    rho = np.outer(psi_tp, psi_tp.conj())
    deph = DephasingEvolver(h, n_sites, gamma, dt=dt)
    n_steps = int(round((t_end - t_p) / dt))
    for k, r in deph.run(rho, n_steps, sample_every=sample_every):
        yield t_p + k * dt, r


def subsystem_loss_series(states, n_sites: int, lost: tuple[int, int],
                          mixed: bool = False):
    """§5.2 protocol 3: Phi on the reduced (N-2)-site graph after tracing out
    `lost` (non-adjacent) sites. MI of surviving pairs is unchanged by the
    partial trace (it is computed from 2-site RDMs), so the effect is purely
    the removal of the lost sites' shortest-path mediation."""
    keep = [i for i in range(n_sites) if i not in lost]
    out = []
    for s in states:
        mi = mutual_information_matrix(s, n_sites, mixed=mixed)
        mi_red = mi[np.ix_(keep, keep)]
        out.append(phi_distance_matrix(mi_red))
    return np.array(out), keep


def restrict_reference(dbar_full_inputs, keep):
    """Reference geometry for protocol 3: recompute shortest paths on the
    surviving-site subgraph of the unperturbed mean MI (paths may not route
    through lost sites in the comparator either)."""
    mi_bar = dbar_full_inputs
    mi_red = mi_bar[np.ix_(keep, keep)]
    return phi_distance_matrix(mi_red)


def log_rho_effect(delta_pert_max: float, delta_unpert_max: float,
                   floor: float = 1e-3) -> float:
    """§5.2 primary effect measure: log drift ratio, both sides floored.

    The spec formula floors only the denominator; the numerator floor binds
    only when the perturbed drift is exactly zero (a stationary object under
    subsystem loss), where the spec formula is undefined (log 0). Recorded
    as an implementation clarification: such cases read log rho = 0, i.e.
    'no effect', which is the intended semantics."""
    return float(np.log(max(delta_pert_max, floor)
                        / max(delta_unpert_max, floor)))


def comparator_quench_stream(h: np.ndarray, rho_bar: np.ndarray, lam: float,
                             site: int, n_sites: int,
                             sample_times_post: np.ndarray):
    """§4.1 fair-perturbation, protocol 1 on the diagonal ensemble: rho_bar
    is stationary under H, so the quench H' = H + lam Z_site simply starts
    at t_p; yields (t_offset, rho) at the requested post-quench offsets."""
    h_pert = h + np.diag(lam * sz_diag(n_sites, site))
    ev = EigenEvolver(h_pert)
    yield from ev.rho_stream(rho_bar, sample_times_post)


def retention_r(delta_pert_max: float, delta_unpert_max: float) -> float:
    """§5.2 secondary (descriptive) retention measure."""
    return float(np.clip(1.0 - max(delta_pert_max - delta_unpert_max, 0.0),
                         0.0, 1.0))


def unperturbed_reference(evolver: EigenEvolver, psi0: np.ndarray,
                          n_sites: int, window: np.ndarray):
    """Unperturbed trajectory on `window`; returns (delta_series, dbar,
    mi_bar, max_delta) — the baseline every protocol compares against."""
    states = evolver.states_at(psi0, window)
    d_series = phi_series(states, n_sites)
    delta, dbar = delta_phi(d_series)
    mi_bar = np.mean([mutual_information_matrix(s, n_sites) for s in states],
                     axis=0)
    return d_series, delta, dbar, mi_bar
