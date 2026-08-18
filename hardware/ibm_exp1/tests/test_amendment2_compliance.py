"""AR-023a Amendment 2 compliance guards (unified-implementation era).

Four defects in this programme had one shape: an amendment item applied
to one analysis path and silently not the other, leaving code that ran
cleanly and returned plausible numbers while answering a retired
question:

  * A2.1/A2.2 endpoint floor missing from S2  -> floor 0.1338, 0/100
  * A2.5(c) corrected leakage missing         -> S2-G1 judged on a
    quantity that does not exist on hardware
  * A2.10 median statistic                    -> 1.9% margin
  * A2.3 retired half still gating S2-G3      -> spurious FAIL

`scripts/analysis.py` now holds the single implementation, so the class
of defect is structurally removed.  These guards enforce that: the
amendment items live in the shared module, and the runners DELEGATE
rather than reimplementing.
"""

from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
RUNNERS = ("run_s1.py", "run_s2.py")
SHARED = "analysis.py"


def source(name: str) -> str:
    return (SCRIPTS / name).read_text(encoding="utf-8")


# ---------------------------------------------- single implementation

@pytest.mark.parametrize("runner", RUNNERS)
def test_runner_delegates_to_the_shared_implementation(runner):
    """Neither runner may carry its own copy of the analysis."""
    text = source(runner)
    assert "analysis.evaluate_experiment(" in text, (
        f"{runner} does not delegate to analysis.evaluate_experiment")


@pytest.mark.parametrize("runner", RUNNERS)
def test_runner_does_not_reimplement_the_floor(runner):
    """The floor must be built once, in the shared module."""
    text = source(runner)
    assert "endpoint_floor(" not in text, (
        f"{runner} builds a floor locally; the shared implementation "
        "in analysis.py is the only one permitted")
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#") or "import" in stripped:
            continue
        assert "floors_from_slots(" not in stripped, (
            f"{runner} still calls the retired matrix-norm floor: "
            f"{stripped!r}")


# ------------------------------------------- amendment items, shared

def test_shared_module_uses_the_endpoint_floor():
    """A2.1: floor = max(split, duplicate), both on the endpoint."""
    text = source(SHARED)
    assert "endpoint_floor(" in text
    assert "endpoint_from_stacks(" in text
    assert "eps_ctrl" in text, "duplicate arm (control substitution) absent"


def test_duplicate_arm_is_never_bootstrapped():
    """A2.2: a systematic cannot be resampled."""
    text = source(SHARED)
    assert "np.median(split_b)" in text, "split arm must be bootstrapped"
    assert "np.median(duplicate" not in text.replace(" ", ""), (
        "duplicate arm appears to be bootstrap-averaged; drift is a "
        "systematic (A2.2)")


def test_projection_clause_uses_the_median_statistic():
    """A2.10: the 0.05 threshold belongs to the MEDIAN statistic."""
    text = source(SHARED)
    assert "proj_median < 0.05" in text
    assert "proj_max < 0.05" not in text, (
        "clause 5 gates the maximum; A2.10 reverted this to the median")


def test_leakage_is_gated_on_corrected_counts():
    """A2.5(c): corrected witness gates; raw is reported alongside."""
    text = source(SHARED)
    assert "surv_corr.min() >= 0.70" in text.replace("float(", "").replace(
        ")", ")"), "clause 3 must use the corrected witness"
    assert "leakage_survival_raw_min" in text, (
        "the raw witness must still be recorded for contrast")
    assert "project=True" in text, (
        "corrected counts must be projected to the closest probability "
        "distribution before the excitation count (A2.5c)")


def test_ideal_case_is_the_degenerate_noisy_case():
    """S1 must not be a special-cased branch: identity M3 instead."""
    text = source(SHARED)
    assert "_identity_inverses" in text, (
        "the ideal backend should reduce to identity M3 rather than a "
        "separate code path")
    assert "cal_probs is None" in text


def test_s2_g3_endpoint_shift_half_is_retired():
    """A2.3: S2-G3 keeps only its per-RDM half; shift is not a gate."""
    text = source("run_s2.py")
    assert "g3_pass = (op is not None and g3_median < 0.05)" in text
    assert "retired_form" in text, (
        "the retired endpoint-shift form must still be reported")


def test_leakage_witness_row_is_excluded_from_reconstruction():
    """A2.5(b): the all-Z row must not enter the tomography estimator."""
    assert "reconstruction_basis_rows" in source("sampling.py")
    for runner in RUNNERS:
        assert "reconstruction_basis_rows(" in source(runner), (
            f"{runner} builds aggregation weights without excluding the "
            "all-Z witness row (A2.5b)")
