"""Tests for the confirmatory-phase additions: vectorized/Floquet witnesses,
degeneracy-correct Xi, density-matrix streams, battery, slope bootstrap."""

import numpy as np
import pytest

from ideg.battery import run_battery
from ideg.evolve import (EigenEvolver, FloquetDephasingEvolver,
                         floquet_states)
from ideg.models import floquet_dtc, mixed_field_ising
from ideg.protocols import (comparator_quench_stream, diagonal_ensemble,
                            log_rho_effect)
from ideg.states import haar_product_state
from ideg.stats import slope_block_bootstrap
from ideg.witnesses import (bohr_measure_pr, bohr_measure_pr_floquet,
                            floquet_eigenbasis, otoc, otoc_series,
                            xi_offdiagonal_pure, xi_offdiagonal_pure_floquet,
                            xi_offdiagonal_rho)

RNG = np.random.default_rng(777)


def test_bohr_pr_two_line_value():
    """Equal superposition of two nondegenerate eigenstates: half the weight
    at w = 0, half at the gap -> PR = 2 exactly."""
    h = np.diag([0.0, 1.3, 2.9, 4.1])  # "2-qubit" diagonal H, no degeneracy
    ev = EigenEvolver(h)
    psi = np.zeros(4, dtype=complex)
    psi[0] = psi[1] = 1.0 / np.sqrt(2.0)
    assert bohr_measure_pr(ev, psi) == pytest.approx(2.0, abs=1e-9)


def test_xi_degenerate_level_is_stationary():
    """Superposition INSIDE a degenerate level does not move under H ->
    Xi must be 0 (the spec's defining property of W4)."""
    h = np.diag([0.0, 1.0, 1.0, 2.0])
    ev = EigenEvolver(h)
    inside = np.array([0.0, 1.0, 1.0, 0.0], dtype=complex) / np.sqrt(2.0)
    across = np.array([1.0, 1.0, 0.0, 0.0], dtype=complex) / np.sqrt(2.0)
    assert xi_offdiagonal_pure(ev, inside) == pytest.approx(0.0, abs=1e-12)
    assert xi_offdiagonal_pure(ev, across) == pytest.approx(0.5, abs=1e-12)
    # rho version agrees with the pure version on pure states
    for psi in (inside, across):
        rho = np.outer(psi, psi.conj())
        assert xi_offdiagonal_rho(ev, rho) == pytest.approx(
            xi_offdiagonal_pure(ev, psi), abs=1e-12)
    # and the state inside the degenerate level really is stationary
    u = ev.unitary_at(3.7)
    assert np.abs(np.abs(inside.conj() @ (u @ inside)) - 1.0) < 1e-12


def test_otoc_series_matches_direct_matrix_computation():
    n = 5
    h = mixed_field_ising(n)
    ev = EigenEvolver(h)
    psi = haar_product_state(n, RNG)
    times = np.array([0.0, 2.5, 7.0])
    c = otoc(ev, psi, n, site_w=4, site_v=2, times=times)
    # direct dense check: C = 1/2 || [W(t), V] psi ||^2
    from ideg.pauli import sz_diag
    w = np.diag(sz_diag(n, 4))
    v = np.diag(sz_diag(n, 2))
    for k, t in enumerate(times):
        u = ev.unitary_at(t)
        wt = u.conj().T @ w @ u
        comm = wt @ v - v @ wt
        assert c[k] == pytest.approx(
            0.5 * float(np.linalg.norm(comm @ psi) ** 2), abs=1e-9)
    # multi-site batch agrees with single-site calls
    both = otoc_series(ev, psi, n, 2, [3, 4], times)
    assert np.allclose(both[1], c, atol=1e-10)


def test_floquet_eigenbasis_reconstruction_and_w1():
    n = 5
    u_f, _ = floquet_dtc(n, eps=0.05, rng=np.random.default_rng(3))
    theta, z = floquet_eigenbasis(u_f)
    assert np.allclose(z @ np.diag(np.exp(-1.0j * theta)) @ z.conj().T,
                       u_f, atol=1e-10)
    # a Floquet eigenstate is silent: PR = 1, Xi = 0
    psi = z[:, 7].copy()
    assert bohr_measure_pr_floquet(theta, z, psi) == pytest.approx(1.0,
                                                                  abs=1e-9)
    assert xi_offdiagonal_pure_floquet(theta, z, psi) == pytest.approx(
        0.0, abs=1e-9)


def test_rho_stream_matches_pure_evolution():
    n = 4
    h = mixed_field_ising(n)
    ev = EigenEvolver(h)
    psi = haar_product_state(n, RNG)
    rho0 = np.outer(psi, psi.conj())
    for t, rho_t in ev.rho_stream(rho0, np.array([1.5, 6.0])):
        psi_t = ev.state_at(psi, t)
        assert np.allclose(rho_t, np.outer(psi_t, psi_t.conj()), atol=1e-10)


def test_comparator_quench_lambda_zero_stationary():
    n = 4
    h = mixed_field_ising(n)
    ev = EigenEvolver(h)
    rho_bar = diagonal_ensemble(ev, haar_product_state(n, RNG))
    for _, rho_t in comparator_quench_stream(h, rho_bar, 0.0, 1, n,
                                             np.array([2.0, 9.0])):
        assert np.allclose(rho_t, rho_bar, atol=1e-10)


def test_floquet_dephasing_trace_and_hermiticity():
    n = 4
    u_f, _ = floquet_dtc(n, eps=0.05, rng=np.random.default_rng(9))
    psi = haar_product_state(n, RNG)
    rho = np.outer(psi, psi.conj())
    for _, rho in FloquetDephasingEvolver(u_f, n, gamma=0.05).run(rho, 30):
        pass
    assert np.trace(rho).real == pytest.approx(1.0, abs=1e-8)
    assert np.allclose(rho, rho.conj().T, atol=1e-10)


def test_log_rho_numerator_floor():
    assert log_rho_effect(0.0, 0.0) == pytest.approx(0.0)
    assert log_rho_effect(0.5, 0.1) == pytest.approx(np.log(5.0))


def test_slope_block_bootstrap_recovers_trend():
    t = np.arange(0.0, 100.0, 0.5)
    y = 0.02 * t + 0.3 * np.sin(t)
    slope, lo, hi = slope_block_bootstrap(t, y, rng=np.random.default_rng(2))
    assert lo <= 0.02 <= hi
    assert slope == pytest.approx(0.02, abs=5e-3)


def test_battery_chaotic_chain_passes():
    n = 5
    h = mixed_field_ising(n)
    psi = haar_product_state(n, RNG)
    times = np.linspace(20.0, 60.0, 5)
    rep = run_battery(h, psi, n, times, np.random.default_rng(42))
    assert rep["all_must_pass"], rep
    # state-only transform: Phi is provably invariant under strictly local
    # basis changes (single-site entropies are), W3 is not
    assert rep["state_only_local_basis"]["phi_max_dev"] < 1e-10
    assert rep["state_only_local_basis"]["w3_max_dev"] > 1e-3
