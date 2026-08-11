"""Unit tests for src/ideg — exact small-N physics checks."""

import numpy as np
import pytest

from ideg.evolve import DephasingEvolver, EigenEvolver, floquet_states
from ideg.migraph import (I0, delta_phi, floyd_warshall,
                          mutual_information_matrix, pair_rdm,
                          pair_rdm_mixed, phi_distance_matrix, phi_series)
from ideg.models import (ferro_ising_weak_tf, floquet_dtc, mixed_field_ising,
                         tfim, xx_chain, xxz_disordered)
from ideg.pauli import (hamming_matrix, reflection_sector_basis, sz_diag,
                        sz_sector_indices)
from ideg.protocols import diagonal_ensemble, quench_run
from ideg.states import (all_up, ground_state, haar_product_state,
                         magnon_superposition, neel)
from ideg.stats import auc, bootstrap_ci_mean, r_statistic
from ideg.witnesses import (bohr_measure_pr, otoc, recurrence_distance,
                            subharmonic_peak, xi_offdiagonal_pure,
                            xi_offdiagonal_rho)

RNG = np.random.default_rng(12345)


def test_bell_pair_mutual_information():
    n = 4
    psi = np.zeros(2**n, dtype=complex)
    # Bell pair on sites (0, 1), up-up background on (2, 3):
    # (|00> + |11>)/sqrt(2) x |00>
    psi[0b0000] = 1 / np.sqrt(2)
    psi[0b1100] = 1 / np.sqrt(2)
    mi = mutual_information_matrix(psi, n)
    assert mi[0, 1] == pytest.approx(I0, rel=1e-10)   # maximal for a pair
    assert mi[2, 3] == pytest.approx(0.0, abs=1e-10)  # product background
    assert mi[0, 2] == pytest.approx(0.0, abs=1e-10)


def test_product_state_zero_mi_and_max_distance():
    n = 5
    psi = haar_product_state(n, RNG)
    mi = mutual_information_matrix(psi, n)
    assert np.max(np.abs(mi - np.diag(np.diag(mi)))) < 1e-8
    d = phi_distance_matrix(mi)
    # every pair at the cap distance (w_max), no shortcut can beat it
    assert d[0, 1] == pytest.approx(-np.log(1e-6))


def test_pair_rdm_mixed_matches_pure():
    n = 4
    psi = haar_product_state(n, RNG)
    h = mixed_field_ising(n)
    ev = EigenEvolver(h)
    psi_t = ev.state_at(psi, 3.7)
    rho = np.outer(psi_t, psi_t.conj())
    for (i, j) in [(0, 1), (1, 3), (0, 3)]:
        r_pure = pair_rdm(psi_t, n, i, j)
        r_mixed = pair_rdm_mixed(rho, n, i, j)
        assert np.allclose(r_pure, r_mixed, atol=1e-12)


def test_floyd_warshall_shortcuts():
    w = np.array([[0.0, 1.0, 10.0],
                  [1.0, 0.0, 1.0],
                  [10.0, 1.0, 0.0]])
    d = floyd_warshall(w)
    assert d[0, 2] == pytest.approx(2.0)  # via the middle node


def test_eigenstate_null_comparator_silent():
    """Spec §4.4: class (i) must silence every witness while Phi is frozen."""
    n = 6
    h = tfim(n, g=1.5)
    ev = EigenEvolver(h)
    psi0 = ground_state(h)
    times = np.linspace(0.0, 50.0, 26)
    states = ev.states_at(psi0, times)

    assert bohr_measure_pr(ev, psi0) == pytest.approx(1.0, abs=1e-9)
    assert xi_offdiagonal_pure(ev, psi0) == pytest.approx(0.0, abs=1e-9)
    assert np.max(recurrence_distance(states)) < 1e-9
    delta, _ = delta_phi(phi_series(states, n))
    assert np.max(delta) < 1e-9


def test_unitarity_and_norm_drift():
    n = 6
    h = mixed_field_ising(n)
    ev = EigenEvolver(h)
    psi = haar_product_state(n, RNG)
    psi_t = ev.state_at(psi, 100.0)
    assert abs(np.linalg.norm(psi_t) - 1.0) < 1e-10


def test_magnon_superposition_energies():
    n = 6
    psi, energies = magnon_superposition(n, RNG)
    h = xx_chain(n)
    # psi should be an exact superposition of eigenstates with the returned
    # energies: H psi restricted to the span must reproduce them
    hpsi = h @ psi
    # project: <psi|H|psi> = mean of energies (equal weights)
    assert (psi.conj() @ hpsi).real == pytest.approx(np.mean(energies),
                                                    abs=1e-9)
    # variance check: <H^2> - <H>^2 matches the mode-energy variance
    var = (hpsi.conj() @ hpsi).real - ((psi.conj() @ hpsi).real) ** 2
    assert var == pytest.approx(np.var(energies), abs=1e-9)


def test_otoc_zero_at_t0_distant_sites():
    n = 6
    h = mixed_field_ising(n)
    ev = EigenEvolver(h)
    psi = haar_product_state(n, RNG)
    c = otoc(ev, psi, n, site_w=0, site_v=4, times=np.array([0.0]))
    assert c[0] == pytest.approx(0.0, abs=1e-10)


def test_otoc_grows_in_chaotic_chain():
    n = 6
    h = mixed_field_ising(n)
    ev = EigenEvolver(h)
    psi = neel(n)
    c = otoc(ev, psi, n, site_w=0, site_v=3, times=np.array([0.0, 6.0]))
    assert c[1] > 0.05


def test_diagonal_ensemble_stationary_and_xi_zero():
    n = 5
    h = mixed_field_ising(n)
    ev = EigenEvolver(h)
    psi = haar_product_state(n, RNG)
    rho_bar = diagonal_ensemble(ev, psi)
    assert np.trace(rho_bar).real == pytest.approx(1.0, abs=1e-10)
    assert xi_offdiagonal_rho(ev, rho_bar) == pytest.approx(0.0, abs=1e-10)
    # stationarity: U rho U^dag = rho
    u = ev.unitary_at(2.3)
    assert np.allclose(u @ rho_bar @ u.conj().T, rho_bar, atol=1e-10)
    # and the dynamical pure state has Xi > 0
    assert xi_offdiagonal_pure(ev, psi) > 0.1


def test_dephasing_preserves_trace_kills_coherence():
    n = 4
    h = mixed_field_ising(n)
    psi = haar_product_state(n, RNG)
    rho = np.outer(psi, psi.conj())
    deph = DephasingEvolver(h, n, gamma=0.5, dt=0.5)
    for _, rho in deph.run(rho, 40):
        pass
    assert np.trace(rho).real == pytest.approx(1.0, abs=1e-8)
    assert np.allclose(rho, rho.conj().T, atol=1e-10)
    ev = EigenEvolver(h)
    # strong dephasing for a long time: energy-basis coherence far below the
    # initial pure-state value 1 - sum p^2
    xi0 = xi_offdiagonal_pure(ev, psi)
    assert xi_offdiagonal_rho(ev, rho) < 0.2 * xi0


def test_floquet_perfect_flip_subharmonic():
    n = 6
    u_f, _ = floquet_dtc(n, eps=0.0, rng=np.random.default_rng(7))
    psi0 = all_up(n)
    traj = floquet_states(u_f, psi0, n_periods=64)[1:]  # drop t=0
    zdiags = np.array([sz_diag(n, i) for i in range(n)])  # (n, dim)
    mags = np.array([[float(np.sum(z * np.abs(s) ** 2)) for z in zdiags]
                     for s in traj])  # (M, n)
    assert subharmonic_peak(mags) > 0.9


def test_floquet_no_interactions_fragile_to_eps():
    """Fine-tuned comparator r1: with J=0 the subharmonic peak degrades
    with eps (no DTC rigidity)."""
    n = 6
    rng = np.random.default_rng(11)
    u0, _ = floquet_dtc(n, eps=0.0, rng=rng, interactions=False)
    u1, _ = floquet_dtc(n, eps=0.15, rng=rng, interactions=False)
    psi0 = all_up(n)
    zdiags = np.array([sz_diag(n, i) for i in range(n)])

    def peak(u):
        traj = floquet_states(u, psi0, n_periods=64)[1:]
        mags = np.array([[float(np.sum(z * np.abs(s) ** 2)) for z in zdiags]
                         for s in traj])
        return subharmonic_peak(mags)

    assert peak(u0) > 0.9
    assert peak(u1) < peak(u0) - 0.1


def test_quench_run_continuity():
    n = 5
    h = mixed_field_ising(n)
    ev = EigenEvolver(h)
    psi = haar_product_state(n, RNG)
    post = quench_run(h, ev, psi, lam=0.0, site=2, n_sites=n, t_p=10.0,
                      sample_times_post=np.array([0.0, 5.0]))
    # lam = 0 quench must exactly continue the unperturbed evolution
    assert np.allclose(post[0], ev.state_at(psi, 10.0), atol=1e-10)
    assert np.allclose(post[1], ev.state_at(psi, 15.0), atol=1e-10)


def test_r_statistic_references():
    rng = np.random.default_rng(3)
    # Poisson: iid uniform levels
    poisson = np.sort(rng.uniform(0, 1000, size=4000))
    assert abs(r_statistic(poisson) - 0.386) < 0.02
    # GOE: eigenvalues of a random symmetric matrix (central bulk)
    m = rng.normal(size=(1200, 1200))
    goe = np.linalg.eigvalsh((m + m.T) / 2.0)
    goe = goe[300:-300]
    assert abs(r_statistic(goe) - 0.531) < 0.02


def test_auc_and_bootstrap():
    assert auc(np.array([1, 2, 3]), np.array([10, 11, 12])) == 1.0
    assert auc(np.array([1, 2, 3, 4]), np.array([1, 2, 3, 4])) == 0.5
    mean, lo, hi = bootstrap_ci_mean(np.arange(20.0),
                                     rng=np.random.default_rng(1))
    assert lo < mean < hi


def test_sector_utilities():
    n = 6
    b = reflection_sector_basis(n, even=True)
    # even + odd dims must total 2^n
    b_odd = reflection_sector_basis(n, even=False)
    assert b.shape[1] + b_odd.shape[1] == 2**n
    assert np.allclose(b.T @ b, np.eye(b.shape[1]), atol=1e-12)
    idx = sz_sector_indices(n, n // 2)
    assert len(idx) == 20  # C(6, 3)
    assert np.all(hamming_matrix(3) == np.array([[0, 1, 1, 2, 1, 2, 2, 3],
                                                 [1, 0, 2, 1, 2, 1, 3, 2],
                                                 [1, 2, 0, 1, 2, 3, 1, 2],
                                                 [2, 1, 1, 0, 3, 2, 2, 1],
                                                 [1, 2, 2, 3, 0, 1, 1, 2],
                                                 [2, 1, 3, 2, 1, 0, 2, 1],
                                                 [2, 3, 1, 2, 1, 2, 0, 1],
                                                 [3, 2, 2, 1, 2, 1, 1, 0]]))


def test_metastable_doublet_slow_dynamics():
    """T-A(iv): |all-up> overlaps the quasi-degenerate doublet almost
    entirely; Bohr measure is dominated by the tiny splitting line."""
    n = 6
    h = ferro_ising_weak_tf(n, g=0.05)
    ev = EigenEvolver(h)
    p = np.abs(ev.coeffs(all_up(n))) ** 2
    assert p[0] + p[1] > 0.99          # doublet support
    split = ev.evals[1] - ev.evals[0]
    gap = ev.evals[2] - ev.evals[1]
    assert split < 1e-3 * gap          # exponentially small splitting


def test_xxz_disordered_shape_and_sector():
    n = 6
    h = xxz_disordered(n, np.random.default_rng(5))
    assert h.shape == (64, 64)
    # conserves total Sz: no matrix elements between different sectors
    idx0 = sz_sector_indices(n, 3)
    idx1 = sz_sector_indices(n, 2)
    assert np.max(np.abs(h[np.ix_(idx0, idx1)])) < 1e-12
