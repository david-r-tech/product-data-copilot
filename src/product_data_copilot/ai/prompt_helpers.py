"""Small, pure helpers for safe AI prompt preparation."""

from product_data_copilot.rules.validators import is_blank

UNKNOWN_FIELD_VALUES = {"", "-", "n/a", "na", "none", "null", "unknown"}

CONFIDENCE_LOW = "low"
CONFIDENCE_MEDIUM = "medium"
CONFIDENCE_HIGH = "high"
ALLOWED_CONFIDENCE_LABELS = [
    CONFIDENCE_LOW,
    CONFIDENCE_MEDIUM,
    CONFIDENCE_HIGH,
]

ACTION_STATUS_DRAFT = "draft"
ACTION_STATUS_NEEDS_REVIEW = "needs_review"
ACTION_STATUS_APPROVED = "approved"
ACTION_STATUS_REJECTED = "rejected"
ALLOWED_AI_ACTION_STATUSES = [
    ACTION_STATUS_DRAFT,
    ACTION_STATUS_NEEDS_REVIEW,
    ACTION_STATUS_APPROVED,
    ACTION_STATUS_REJECTED,
]

AI_SUGGESTION_SCHEMA_FIELDS = [
    "sku",
    "field_name",
    "original_value",
    "suggested_value",
    "source_fields",
    "confidence",
    "reason",
    "action_status",
]

DEFAULT_PRODUCT_CONTEXT_FIELDS = [
    "sku",
    "product_name",
    "category",
    "brand",
    "manufacturer",
    "description",
    "attributes",
    "ean",
    "image_url",
    "warning_notes",
    "translation_de",
    "translation_en",
]


def normalize_prompt_value(value):
    """Return a clean string value for prompt context."""
    if is_blank(value):
        return ""

    text = str(value).strip()
    if text.lower() in UNKNOWN_FIELD_VALUES:
        return ""

    return text


def should_include_prompt_field(value):
    """Return True when a field has useful source information."""
    return normalize_prompt_value(value) != ""


def build_product_context_snippet(product_data, fields=None):
    """Build a compact product context dictionary without empty fields."""
    if fields is None:
        fields = DEFAULT_PRODUCT_CONTEXT_FIELDS

    context = {}
    for field_name in fields:
        value = normalize_prompt_value(product_data.get(field_name, ""))
        if value:
            context[field_name] = value

    return context


def do_not_invent_facts_instruction():
    """Return the core anti-hallucination instruction for AI prompts."""
    return (
        "Do not invent facts, technical attributes, certifications, compliance "
        "claims, or unverifiable product details. Use only the provided source "
        "fields and clearly flag uncertainty."
    )


def human_review_instruction():
    """Return the human-in-the-loop safety instruction."""
    return (
        "All AI suggestions are draft recommendations. A human reviewer must "
        "approve, edit, or reject them before they are used or exported."
    )


def structured_suggestion_schema_description():
    """Return the expected structured suggestion schema description."""
    return {
        "fields": AI_SUGGESTION_SCHEMA_FIELDS.copy(),
        "required": AI_SUGGESTION_SCHEMA_FIELDS.copy(),
        "confidence_values": ALLOWED_CONFIDENCE_LABELS.copy(),
        "action_status_values": ALLOWED_AI_ACTION_STATUSES.copy(),
    }


def is_valid_confidence_label(confidence):
    """Return True when confidence is one of the allowed labels."""
    return normalize_prompt_value(confidence).lower() in ALLOWED_CONFIDENCE_LABELS


def normalize_confidence_label(confidence):
    """Return a valid confidence label, defaulting to low."""
    confidence = normalize_prompt_value(confidence).lower()
    if confidence in ALLOWED_CONFIDENCE_LABELS:
        return confidence
    return CONFIDENCE_LOW


def is_valid_ai_action_status(action_status):
    """Return True when the AI suggestion action status is allowed."""
    return normalize_prompt_value(action_status).lower() in ALLOWED_AI_ACTION_STATUSES


def normalize_ai_action_status(action_status):
    """Return a valid AI action status, defaulting to draft."""
    action_status = normalize_prompt_value(action_status).lower()
    if action_status in ALLOWED_AI_ACTION_STATUSES:
        return action_status
    return ACTION_STATUS_DRAFT


def build_safe_prompt_instructions():
    """Return the reusable safety instructions for AI suggestion prompts."""
    return "\n".join(
        [
            do_not_invent_facts_instruction(),
            human_review_instruction(),
            "Do not claim legal compliance or say that a product is legally safe.",
            "Provide a confidence value and a reason for every suggestion.",
        ]
    )
