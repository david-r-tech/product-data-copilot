"""Validate AI suggestions against trusted source identity and field values."""

from product_data_copilot.ai.suggestion_schema import normalize_suggestion_record, normalize_text
from product_data_copilot.rules.validators import normalize_text as source_text

EDITABLE_TEXT_FIELDS = (
    "product_name", "description", "attributes", "translation_de", "translation_en",
)
SOURCE_FIELDS = {
    "sku", "product_name", "category", "description", "brand", "manufacturer",
    "attributes", "ean", "language", "price", "image_url", "warning_notes",
    "translation_de", "translation_en",
}


def validate_suggestions_against_product(suggestions, product):
    """Fail closed on mismatched identity, fabricated evidence or unusable edits.

    This validates provenance and structure, not factual equivalence of natural
    language. A human must still check every proposed claim and translation.
    """
    results = []
    for suggestion in suggestions:
        record = normalize_suggestion_record(suggestion)
        errors = []
        target = record["target_field"]
        if record["sku"] != source_text(product.get("sku")):
            errors.append("SKU does not match the selected product")
        if target not in EDITABLE_TEXT_FIELDS:
            errors.append("target field is not an editable text field")
        elif record["current_value"] != source_text(product.get(target)):
            errors.append("current value does not match the loaded source")
        sources = record["source_fields"]
        if not sources or any(
            field not in SOURCE_FIELDS or not normalize_text(product.get(field))
            for field in sources
        ):
            errors.append("source fields must exist and contain usable product data")
        if not record["reason"]:
            errors.append("a reason is required")
        if not record["proposed_value"]:
            errors.append("no proposed value; this is a review task, not an improvement")
        elif record["proposed_value"] == record["current_value"]:
            errors.append("the suggestion does not change the source value")
        record["approval_status"] = "needs_review"
        if errors:
            record["suggestion_status"] = "blocked_insufficient_source"
            record["risk_level"] = "high"
            record["reason"] = (record["reason"] + "\nBlocked: " + "; ".join(errors) + ".").strip()
        # Product label comes from the loaded file, never the model.
        record["product_name"] = normalize_text(product.get("product_name"))
        results.append(record)
    return results
