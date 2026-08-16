import numpy as np

from experiment import hardware_time_grid


def test_registered_25_point_time_grid_is_deterministic():
    indices, times = hardware_time_grid(25)
    assert len(indices) == len(times) == 25
    assert indices[0] == 0 and indices[-1] == 360
    assert times[0] == 20.0 and times[-1] == 200.0
    assert np.allclose(times, 20.0 + 0.5 * indices)

