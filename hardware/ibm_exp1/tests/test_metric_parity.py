import numpy as np

from experiment import metric_from_pair_rdms
from ideg.migraph import (mutual_information_matrix, pair_rdm,
                          phi_distance_matrix)


def test_pair_rdm_metric_matches_paper_implementation():
    n_sites = 4
    rng = np.random.default_rng(23002)
    state = rng.normal(size=2**n_sites) + 1.0j * rng.normal(size=2**n_sites)
    state /= np.linalg.norm(state)
    rdms = {
        (i, j): pair_rdm(state, n_sites, i, j)
        for i in range(n_sites)
        for j in range(i + 1, n_sites)
    }
    mi, metric = metric_from_pair_rdms(rdms, n_sites)
    expected_mi = mutual_information_matrix(state, n_sites)
    expected_metric = phi_distance_matrix(expected_mi)
    assert np.allclose(mi, expected_mi, atol=1.0e-12)
    assert np.allclose(metric, expected_metric, atol=1.0e-12)

