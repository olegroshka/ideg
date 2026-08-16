import numpy as np

from experiment import one_magnon_basis_index, paper_site_to_qiskit


def test_paper_site_to_qiskit_mapping_is_explicit_reflection():
    assert paper_site_to_qiskit(10) == tuple(range(9, -1, -1))


def test_one_magnon_indices_match_qiskit_little_endian_bits():
    mapping = paper_site_to_qiskit(10)
    for paper_site, qiskit_qubit in enumerate(mapping):
        paper_index = one_magnon_basis_index(paper_site, 10)
        qiskit_index = 1 << qiskit_qubit
        assert paper_index == qiskit_index
        state = np.zeros(2**10)
        state[paper_index] = 1.0
        assert np.argmax(state) == qiskit_index

