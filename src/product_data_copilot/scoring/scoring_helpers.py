"""Small, pure scoring helpers for product readiness calculations."""

READINESS_READY = "Ready"
READINESS_NEEDS_REVIEW = "Needs Review"
READINESS_CRITICAL = "Critical"

SEVERITY_PENALTIES = {
    "Critical": 25,
    "Warning": 10,
    "Info": 3,
}


def clamp_score(score):
    """Clamp a numeric score into the 0-100 range and round it."""
    return max(0, min(100, round(score)))


def is_score_in_range(score):
    """Return True when score is numeric and inside the 0-100 range."""
    try:
        numeric_score = float(score)
    except (TypeError, ValueError):
        return False

    return 0 <= numeric_score <= 100


def readiness_status_from_score(score):
    """Return the readiness status label for a numeric score."""
    score = clamp_score(score)

    if score >= 85:
        return READINESS_READY
    if score >= 60:
        return READINESS_NEEDS_REVIEW
    return READINESS_CRITICAL


def score_from_checks(checks):
    """Return a percentage score based on truthy checks."""
    checks = list(checks)

    if len(checks) == 0:
        return 100

    return clamp_score((sum(bool(check) for check in checks) / len(checks)) * 100)


def weighted_average_score(weighted_scores):
    """Return a weighted average from (score, weight) pairs."""
    weighted_scores = list(weighted_scores)
    total_weight = sum(weight for _, weight in weighted_scores)

    if total_weight <= 0:
        return 0

    total = sum(clamp_score(score) * weight for score, weight in weighted_scores)
    return clamp_score(total / total_weight)


def penalty_for_severity(severity):
    """Return the point deduction for a severity label."""
    return SEVERITY_PENALTIES.get(severity, 0)


def score_after_issue_penalties(start_score, severities):
    """Apply severity penalties to a score and keep it in the valid range."""
    penalty_total = sum(penalty_for_severity(severity) for severity in severities)
    return clamp_score(start_score - penalty_total)

