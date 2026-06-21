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

FORBIDDEN_UNSUPPORTED_FACT_CATEGORIES = [
    "EANs or GTINs",
    "prices",
    "dimensions",
    "certifications",
    "materials",
    "compliance claims",
    "legal or safety claims",
    "unsupported translations",
]

REVIEW_REQUIRED_SOURCE_CONDITIONS = [
    "source data is missing",
    "source data is weak",
    "source data is unknown",
    "source data is contradictory",
    "target field is price, EAN, GTIN, certification, legal, safety, or compliance",
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


def smart_suggestion_blocked_fact_categories():
    """Return fact categories that must not be invented by AI."""
    return FORBIDDEN_UNSUPPORTED_FACT_CATEGORIES.copy()


def smart_suggestion_review_required_conditions():
    """Return conditions that should force review-required suggestions."""
    return REVIEW_REQUIRED_SOURCE_CONDITIONS.copy()


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


def smart_suggestion_prompt_contract_block():
    """Return a deterministic future prompt contract block."""
    contract = smart_suggestion_json_contract()
    required_keys = ", ".join(contract["required_keys"])
    forbidden_categories = ", ".join(smart_suggestion_blocked_fact_categories())
    review_conditions = "; ".join(smart_suggestion_review_required_conditions())

    return "\n".join(
        [
            "Smart Suggestions v2 output contract:",
            "Return only valid JSON.",
            "The root object must contain a smart_suggestions array.",
            "Each array item must be one field-level suggestion.",
            f"Each suggestion must include these keys: {required_keys}.",
            (
                "Allowed confidence values are low, medium, and high. "
                "Allowed risk_level values are low, medium, and high."
            ),
            (
                "Allowed approval_status values are needs_review, approved, "
                "and rejected, but AI-generated suggestions must not set "
                "approval_status to approved."
            ),
            (
                "Allowed suggestion_status values are draft, review_required, "
                "and blocked_insufficient_source."
            ),
            smart_suggestion_safety_rules(),
            smart_suggestion_human_review_rules(),
            f"Never invent or infer these unsupported fact categories: {forbidden_categories}.",
            f"Mark the suggestion as review_required when: {review_conditions}.",
        ]
    )
