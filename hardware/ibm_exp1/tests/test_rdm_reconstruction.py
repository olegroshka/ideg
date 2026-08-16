from itertools import product

import numpy as np

from experiment import PAULI, hermitize_and_project, reconstruct_pair_rdm


def _expectations(rho):
    return {
        (a, b): float(np.trace(rho @ np.kron(PAULI[a], PAULI[b])).real)
        for a, b in product(PAULI, repeat=2)
    }


def test_bell_pair_rdm_reconstructs_from_pauli_expectations():
    bell = np.array([1.0, 0.0, 0.0, 1.0], dtype=complex) / np.sqrt(2.0)
    exact = np.outer(bell, bell.conj())
    reconstructed = reconstruct_pair_rdm(_expectations(exact))
    assert np.allclose(reconstructed, exact, atol=1.0e-12)


def test_psd_projection_reports_negative_raw_eigenvalue():
    invalid = np.diag([0.6, 0.4, 0.1, -0.1]).astype(complex)
    projected, diagnostics = hermitize_and_project(invalid)
    assert diagnostics["min_eigenvalue_raw"] == -0.1
    assert diagnostics["projection_fro"] > 0.0
    assert np.isclose(np.trace(projected), 1.0)
    assert np.min(np.linalg.eigvalsh(projected)) >= -1.0e-14

