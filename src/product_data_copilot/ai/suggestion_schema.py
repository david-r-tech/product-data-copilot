"""Pure helpers for future field-level Smart Suggestions records."""

UNKNOWN_FIELD_VALUES = {"", "-", "n/a", "na", "none", "null", "unknown"}

CONFIDENCE_LOW = "low"
CONFIDENCE_MEDIUM = "medium"
CONFIDENCE_HIGH = "high"
ALLOWED_CONFIDENCE_LABELS = [
    CONFIDENCE_LOW,
    CONFIDENCE_MEDIUM,
    CONFIDENCE_HIGH,
]
DEFAULT_CONFIDENCE_LABEL = CONFIDENCE_LOW

RISK_LEVEL_LOW = "low"
RISK_LEVEL_MEDIUM = "medium"
RISK_LEVEL_HIGH = "high"
ALLOWED_RISK_LEVELS = [
    RISK_LEVEL_LOW,
    RISK_LEVEL_MEDIUM,
    RISK_LEVEL_HIGH,
]
DEFAULT_RISK_LEVEL = RISK_LEVEL_HIGH

APPROVAL_STATUS_NEEDS_REVIEW = "needs_review"
APPROVAL_STATUS_APPROVED = "approved"
APPROVAL_STATUS_REJECTED = "rejected"
ALLOWED_APPROVAL_STATUSES = [
    APPROVAL_STATUS_NEEDS_REVIEW,
    APPROVAL_STATUS_APPROVED,
    APPROVAL_STATUS_REJECTED,
]
DEFAULT_APPROVAL_STATUS = APPROVAL_STATUS_NEEDS_REVIEW

SUGGESTION_STATUS_DRAFT = "draft"
SUGGESTION_STATUS_REVIEW_REQUIRED = "review_required"
SUGGESTION_STATUS_BLOCKED = "blocked_insufficient_source"
ALLOWED_SUGGESTION_STATUSES = [
    SUGGESTION_STATUS_DRAFT,
    SUGGESTION_STATUS_REVIEW_REQUIRED,
    SUGGESTION_STATUS_BLOCKED,
]
DEFAULT_SUGGESTION_STATUS = SUGGESTION_STATUS_REVIEW_REQUIRED

REQUIRED_SUGGESTION_FIELDS = [
    "sku",
    "product_name",
    "target_field",
    "current_value",
    "proposed_value",
    "source_fields",
    "reason",
    "confidence",
    "risk_level",
    "requires_human_approval",
    "approval_status",
    "suggestion_status",
]

UNSUPPORTED_FACT_TARGET_FIELDS = [
    "ean",
    "gtin",
    "price",
    "dimension",
    "dimensions",
    "certification",
    "certifications",
    "material",
    "materials",
    "compliance",
    "compliance_claim",
    "compliance_claims",
    "legal_claim",
    "legal_claims",
    "safety_claim",
    "safety_claims",
]


def normalize_text(value):
    """Return a stripped text value, treating common placeholders as blank."""
    if value is None:
        return ""

    text = str(value).strip()
    if text.lower() in UNKNOWN_FIELD_VALUES:
        return ""

    return text


def normalize_confidence(value):
    """Return a valid confidence label, defaulting cautiously to low."""
    confidence = normalize_text(value).lower()
    if confidence in ALLOWED_CONFIDENCE_LABELS:
        return confidence
    return DEFAULT_CONFIDENCE_LABEL


def normalize_risk_level(value):
    """Return a valid risk level, defaulting cautiously to high."""
    risk_level = normalize_text(value).lower()
    if risk_level in ALLOWED_RISK_LEVELS:
        return risk_level
    return DEFAULT_RISK_LEVEL


def normalize_approval_status(value):
    """Return a valid approval status, defaulting to needs_review."""
    approval_status = normalize_text(value).lower()
    if approval_status in ALLOWED_APPROVAL_STATUSES:
        return approval_status
    return DEFAULT_APPROVAL_STATUS


def normalize_suggestion_status(value):
    """Return a valid suggestion status, defaulting to review_required."""
    suggestion_status = normalize_text(value).lower()
    if suggestion_status in ALLOWED_SUGGESTION_STATUSES:
        return suggestion_status
    return DEFAULT_SUGGESTION_STATUS


def normalize_source_fields(value):
    """Return a clean list of source field names."""
    if value is None:
        return []

    if isinstance(value, str):
        raw_fields = value.split(",")
    elif isinstance(value, (list, tuple, set)):
        raw_fields = list(value)
    else:
        return []

    source_fields = []
    for field_name in raw_fields:
        normalized_field = normalize_text(field_name)
        if normalized_field and normalized_field not in source_fields:
            source_fields.append(normalized_field)

    return source_fields


def is_unsupported_fact_target_field(target_field):
    """Return True when AI should not propose factual values for a field."""
    normalized_target_field = normalize_text(target_field).lower()
    return normalized_target_field in UNSUPPORTED_FACT_TARGET_FIELDS


def has_required_source_and_reason(record):
    """Return True when a suggestion has source fields and a reason."""
    return (
        len(normalize_source_fields(record.get("source_fields"))) > 0
        and normalize_text(record.get("reason")) != ""
    )


def normalize_suggestion_record(record):
    """Return a normalized suggestion record with stable required fields."""
    normalized = {}
    for field_name in REQUIRED_SUGGESTION_FIELDS:
        normalized[field_name] = record.get(field_name, "")

    normalized["sku"] = normalize_text(normalized["sku"])
    normalized["product_name"] = normalize_text(normalized["product_name"])
    normalized["target_field"] = normalize_text(normalized["target_field"])
    normalized["current_value"] = normalize_text(normalized["current_value"])
    normalized["proposed_value"] = normalize_text(normalized["proposed_value"])
    normalized["source_fields"] = normalize_source_fields(normalized["source_fields"])
    normalized["reason"] = normalize_text(normalized["reason"])
    normalized["confidence"] = normalize_confidence(normalized["confidence"])
    normalized["risk_level"] = normalize_risk_level(normalized["risk_level"])
    normalized["requires_human_approval"] = True
    normalized["approval_status"] = normalize_approval_status(
        normalized["approval_status"]
    )
    normalized["suggestion_status"] = normalize_suggestion_status(
        normalized["suggestion_status"]
    )

    return normalized


def validate_suggestion_record(record):
    """Return True when a suggestion has the minimum review-ready structure."""
    normalized = normalize_suggestion_record(record)
    required_text_fields = ["sku", "target_field", "reason"]

    for field_name in required_text_fields:
        if normalize_text(normalized.get(field_name)) == "":
            return False

    if not has_required_source_and_reason(normalized):
        return False

    if normalized["requires_human_approval"] is not True:
        return False

    return True


def create_review_required_suggestion(
    sku,
    product_name,
    target_field,
    current_value="",
    proposed_value="",
    source_fields=None,
    reason="",
    confidence=None,
    risk_level=None,
):
    """Create a conservative field-level suggestion that requires review."""
    return normalize_suggestion_record(
        {
            "sku": sku,
            "product_name": product_name,
            "target_field": target_field,
            "current_value": current_value,
            "proposed_value": proposed_value,
            "source_fields": source_fields or [],
            "reason": reason,
            "confidence": confidence,
            "risk_level": risk_level,
            "requires_human_approval": True,
            "approval_status": DEFAULT_APPROVAL_STATUS,
            "suggestion_status": DEFAULT_SUGGESTION_STATUS,
        }
    )
