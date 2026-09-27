"""Small, pure helpers for review workflow decisions."""

REVIEW_STATUS_OK = "OK"
REVIEW_STATUS_NEEDS_REVIEW = "Needs Review"
REVIEW_STATUS_MISSING_DATA = "Missing Data"
REVIEW_STATUS_AI_SUGGESTION_CREATED = "AI Suggestion Created"
REVIEW_STATUS_TRANSLATION_MISSING = "Translation Missing"
REVIEW_STATUS_COMPLIANCE_CHECK_REQUIRED = "Compliance Check Required"
REVIEW_STATUS_READY_FOR_EXPORT = "Ready for Export"
REVIEW_STATUS_REJECTED = "Rejected"

ALLOWED_REVIEW_STATUSES = [
    REVIEW_STATUS_OK,
    REVIEW_STATUS_NEEDS_REVIEW,
    REVIEW_STATUS_MISSING_DATA,
    REVIEW_STATUS_AI_SUGGESTION_CREATED,
    REVIEW_STATUS_TRANSLATION_MISSING,
    REVIEW_STATUS_COMPLIANCE_CHECK_REQUIRED,
    REVIEW_STATUS_READY_FOR_EXPORT,
    REVIEW_STATUS_REJECTED,
]

TASK_PRIORITY_HIGH = "High"
TASK_PRIORITY_MEDIUM = "Medium"
TASK_PRIORITY_LOW = "Low"

TASK_TYPE_DATA_COMPLETION = "Data Completion"
TASK_TYPE_COMMERCIAL_REVIEW = "Commercial Review"
TASK_TYPE_ATTRIBUTE_ENRICHMENT = "Attribute Enrichment"
TASK_TYPE_TRANSLATION = "Translation"
TASK_TYPE_COMPLIANCE_REVIEW = "Compliance Review"
TASK_TYPE_CONTENT_IMPROVEMENT = "Content Improvement"
TASK_TYPE_MEDIA_IMPROVEMENT = "Media Improvement"
TASK_TYPE_GENERAL_REVIEW = "General Review"


def severity_to_task_priority(severity):
    """Map an issue severity to a review task priority."""
    if severity == "Critical":
        return TASK_PRIORITY_HIGH
    if severity == "Warning":
        return TASK_PRIORITY_MEDIUM
    return TASK_PRIORITY_LOW


def issue_to_task_type(issue_type, severity=None):
    """Map an issue type and optional severity to a review task type."""
    if severity == "Critical":
        return TASK_TYPE_DATA_COMPLETION
    if issue_type == "Missing manufacturer":
        return TASK_TYPE_DATA_COMPLETION
    if issue_type in ["Missing price", "Invalid price"]:
        return TASK_TYPE_COMMERCIAL_REVIEW
    if issue_type == "Missing attributes":
        return TASK_TYPE_ATTRIBUTE_ENRICHMENT
    if issue_type in ["Missing translation_de", "Missing translation_en"]:
        return TASK_TYPE_TRANSLATION
    if issue_type == "Missing warning_notes":
        return TASK_TYPE_COMPLIANCE_REVIEW
    if issue_type in [
        "Short product_name",
        "Short description",
        "Generic product_name",
    ]:
        return TASK_TYPE_CONTENT_IMPROVEMENT
    if issue_type in ["Missing image_url", "Image URL suspicious"]:
        return TASK_TYPE_MEDIA_IMPROVEMENT
    return TASK_TYPE_GENERAL_REVIEW


def normalize_review_status(status):
    """Return a known review status or the default Needs Review status."""
    if status in ALLOWED_REVIEW_STATUSES:
        return status
    return REVIEW_STATUS_NEEDS_REVIEW


def is_allowed_review_status(status):
    """Return True when a review status is one of the allowed labels."""
    return status in ALLOWED_REVIEW_STATUSES


def is_ready_for_export(review_status):
    """Return True when the effective review status is ready for export."""
    return normalize_review_status(review_status) == REVIEW_STATUS_READY_FOR_EXPORT


def needs_review(review_status):
    """Return True when a product still needs review work."""
    return not is_ready_for_export(review_status)


def derive_review_status(issue_types, severities, readiness_status):
    """Derive the product review status from issues and readiness status."""
    issue_types = list(issue_types)
    severities = list(severities)

    if "Critical" in severities:
        return REVIEW_STATUS_MISSING_DATA
    if "Missing warning_notes" in issue_types:
        return REVIEW_STATUS_COMPLIANCE_CHECK_REQUIRED
    if "Missing translation_de" in issue_types or "Missing translation_en" in issue_types:
        return REVIEW_STATUS_TRANSLATION_MISSING
    if readiness_status == "Ready" and not issue_types and not severities:
        return REVIEW_STATUS_READY_FOR_EXPORT
    return REVIEW_STATUS_NEEDS_REVIEW
