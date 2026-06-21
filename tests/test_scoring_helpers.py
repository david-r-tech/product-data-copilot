import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_PATH))

from product_data_copilot.scoring.scoring_helpers import (  # noqa: E402
    READINESS_CRITICAL,
    READINESS_NEEDS_REVIEW,
    READINESS_READY,
    clamp_score,
    is_score_in_range,
    penalty_for_severity,
    readiness_status_from_score,
    score_after_issue_penalties,
    score_from_checks,
    weighted_average_score,
)


def test_clamp_score_keeps_scores_between_zero_and_one_hundred():
    assert clamp_score(-10) == 0
    assert clamp_score(0) == 0
    assert clamp_score(85.4) == 85
    assert clamp_score(101) == 100


def test_score_range_validation():
    assert is_score_in_range(0)
    assert is_score_in_range(100)
    assert is_score_in_range("75")
    assert not is_score_in_range(-1)
    assert not is_score_in_range(101)
    assert not is_score_in_range("not-a-score")


def test_readiness_status_from_score():
    assert readiness_status_from_score(100) == READINESS_READY
    assert readiness_status_from_score(85) == READINESS_READY
    assert readiness_status_from_score(84) == READINESS_NEEDS_REVIEW
    assert readiness_status_from_score(60) == READINESS_NEEDS_REVIEW
    assert readiness_status_from_score(59) == READINESS_CRITICAL


def test_score_from_checks_returns_percentage():
    assert score_from_checks([]) == 100
    assert score_from_checks([True, True, True]) == 100
    assert score_from_checks([True, False]) == 50
    assert score_from_checks([False, False, False]) == 0
    assert score_from_checks([True, False, False, False, False, False]) == 17
    assert score_from_checks([True, True, True, True, True, False]) == 83


def test_weighted_average_score():
    assert weighted_average_score([(100, 0.5), (50, 0.5)]) == 75
    assert weighted_average_score([(100, 0.35), (80, 0.25), (60, 0.40)]) == 79
    assert weighted_average_score([]) == 0
    assert weighted_average_score([(100, 0)]) == 0


def test_severity_penalties():
    assert penalty_for_severity("Critical") == 25
    assert penalty_for_severity("Warning") == 10
    assert penalty_for_severity("Info") == 3
    assert penalty_for_severity("Unknown") == 0


def test_score_after_issue_penalties():
    assert score_after_issue_penalties(100, ["Critical"]) == 75
    assert score_after_issue_penalties(100, ["Warning", "Info"]) == 87
    assert score_after_issue_penalties(20, ["Critical"]) == 0
    assert score_after_issue_penalties(100, []) == 100
