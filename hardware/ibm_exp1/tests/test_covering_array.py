from collections import Counter
from itertools import product

from experiment import AXES, covering_array_rows, validate_covering_array


def test_registered_covering_array_has_exact_strength_two_multiplicity():
    rows = covering_array_rows()
    validate_covering_array(rows)
    assert len(rows) == 27
    expected = Counter(a + b for a, b in product(AXES, repeat=2))
    expected = Counter({key: 3 for key in expected})
    for i in range(10):
        for j in range(i + 1, 10):
            assert Counter(row[i] + row[j] for row in rows) == expected



def test_all_z_leakage_witness_row_is_present_and_excluded():
    """AR-023a A2.5: witness row exists, reconstruction still 27 rows."""
    from experiment import (ALL_Z_ROW, RECONSTRUCTION_ROWS,
                            covering_array_rows, leakage_row_index,
                            tomography_rows)

    base = covering_array_rows()
    assert ALL_Z_ROW not in base, "no covering-array row measures all Z"
    assert max(row.count("Z") for row in base) == 6

    rows = tomography_rows(True)
    assert len(rows) == 28
    assert rows[:RECONSTRUCTION_ROWS] == base
    assert rows[leakage_row_index(rows)] == ALL_Z_ROW


def test_leakage_witness_recovers_one_excitation_probability():
    """The all-Z row makes the AR-023 §5 quantity computable."""
    import numpy as np
    from sampling import survival_from_allz, N_OUT

    counts = np.zeros(N_OUT)
    counts[1 << 3] = 700.0          # one excitation
    counts[(1 << 3) | (1 << 5)] = 68.0   # two excitations
    assert abs(float(survival_from_allz(counts)) - 700.0 / 768.0) < 1e-12


def test_endpoint_floor_takes_conservative_max():
    """A2.1: floor = max(split, duplicate), both endpoint-level."""
    from sampling import endpoint_floor

    out = endpoint_floor(0.230, 0.210, 0.228, 0.226)
    assert abs(out["split"] - 0.020) < 1e-12
    assert abs(out["duplicate"] - 0.002) < 1e-12
    assert abs(out["floor"] - 0.020) < 1e-12
