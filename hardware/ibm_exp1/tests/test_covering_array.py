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

