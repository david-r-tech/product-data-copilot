"""Pure helpers describing the future Smart Suggestions AI contract."""

SMART_SUGGESTION_REQUIRED_KEYS = [
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


def smart_suggestion_json_contract():
    """Return the expected structured output contract for future prompts."""
    return {
        "root_key": "smart_suggestions",
        "item_type": "field_level_suggestion",
        "required_keys": SMART_SUGGESTION_REQUIRED_KEYS.copy(),
        "confidence_values": ["low", "medium", "high"],
        "risk_level_values": ["low", "medium", "high"],
        "approval_status_values": ["needs_review", "approved", "rejected"],
        "suggestion_status_values": [
            "draft",
            "review_required",
            "blocked_insufficient_source",
        ],
    }


def smart_suggestion_safety_rules():
    """Return strict safety rules for future field-level AI suggestions."""
    return "\n".join(
        [
            "Do not invent product facts.",
            (
                "Do not create unverifiable EANs, GTINs, prices, dimensions, "
                "certifications, materials, translations, or compliance claims."
            ),
            "Use only existing source fields from the provided product data.",
            (
                "If source data is missing, weak, unknown, or contradictory, "
                "leave proposed_value empty and mark the suggestion as review required."
            ),
            (
                "Every suggestion must include source_fields, reason, confidence, "
                "risk_level, approval_status, and suggestion_status."
            ),
            "Never claim legal compliance or that a product is safe.",
        ]
    )


def smart_suggestion_human_review_rules():
    """Return human-in-the-loop rules for future Smart Suggestions."""
    return "\n".join(
        [
            "All Smart Suggestions are draft recommendations.",
            "Human approval is required before use or export.",
            "Do not auto-apply suggestions to product data.",
            "Start suggestions as needs_review or review_required unless a human changes them.",
            "Rejected or draft suggestions must not be treated as approved product data.",
        ]
    )
