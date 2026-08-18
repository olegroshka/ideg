"""AR-023a Amendment 2 compliance guards.

Two defects in this session had the same shape: an amendment item was
applied to one analysis path (S1) and silently not to the other (S2),
leaving code that still compiled, still ran, and still produced
plausible numbers while answering the retired question.

  * A2.1/A2.2 (endpoint floor) were missing from run_s2.py -> the first
    S2 condition reported floor 0.1338 and success 0/100.
  * A2.5(c) (readout-corrected leakage) was missing from the traffic
    light -> S2-G1 was judged on the simulator's exact survival, a
    quantity that does not exist on hardware.

Both were caught by eyeballing a shared number across the two paths.
These tests make that check automatic.  They are deliberately
structural: the real fix is a single shared implementation, and until
that refactor lands these guards keep the two paths honest.
"""

from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
RUNNERS = ("run_s1.py", "run_s2.py")


def source(name: str) -> str:
    return (SCRIPTS / name).read_text(encoding="utf-8")


@pytest.mark.parametrize("runner", RUNNERS)
def test_runner_uses_endpoint_floor(runner):
    """A2.1: both analysis paths build the floor on the endpoint."""
    text = source(runner)
    assert "endpoint_floor(" in text, (
        f"{runner} does not call sampling.endpoint_floor — the A2.1 "
        "endpoint-level floor is not in this path")
    assert "endpoint_from_stacks(" in text, (
        f"{runner} does not compute endpoint arms via "
        "sampling.endpoint_from_stacks")


@pytest.mark.parametrize("runner", RUNNERS)
def test_retired_matrix_norm_floor_is_not_in_the_decision_path(runner):
    """The retired full-matrix floor must not feed any clause or gate."""
    text = source(runner)
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#") or "import" in stripped:
            continue
        assert "floors_from_slots(" not in stripped, (
            f"{runner} still calls floors_from_slots in the decision "
            f"path: {stripped!r}")


@pytest.mark.parametrize("runner", RUNNERS)
def test_duplicate_arm_is_never_bootstrapped(runner):
    """A2.2: a systematic must not be resampled."""
    text = source(runner)
    assert "np.median(split_b)" in text, (
        f"{runner} must bootstrap the SPLIT arm (A2.2)")
    assert "np.median(duplicate" not in text.replace(" ", ""), (
        f"{runner} appears to take a bootstrap median of the duplicate "
        "arm; drift is a systematic and cannot be resampled (A2.2)")


def test_s2_leakage_gate_uses_corrected_counts():
    """A2.5(c): the traffic light is judged on corrected counts."""
    text = source("run_s2.py")
    assert "leakage_survival_corrected_min" in text, (
        "run_s2.py does not record the corrected leakage witness")
    assert "traffic_light_from_records" in text, (
        "the S2 traffic light is not derived from the per-experiment "
        "corrected records (A2.5c)")


def test_s2_projection_clause_uses_the_median_statistic():
    """A2.10: the 0.05 threshold belongs to the MEDIAN statistic."""
    text = source("run_s2.py")
    assert "proj_median < 0.05" in text, (
        "run_s2.py clause 5 must gate the median per-RDM correction")
    assert "proj_max < 0.05" not in text, (
        "run_s2.py still gates the maximum per-RDM correction (A2.10 "
        "reverted this to the median)")


def test_leakage_witness_row_is_excluded_from_reconstruction():
    """A2.5(b): the all-Z row must not enter the tomography estimator."""
    text = source("sampling.py")
    assert "reconstruction_basis_rows" in text
    for runner in RUNNERS:
        assert "reconstruction_basis_rows(" in source(runner), (
            f"{runner} builds aggregation weights without excluding the "
            "all-Z witness row (A2.5b)")
