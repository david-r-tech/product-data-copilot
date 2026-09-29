"""Pure product scoring and readiness orchestration."""

import pandas as pd

from product_data_copilot.data.product_input import validate_product_identity
from product_data_copilot.review.review_helpers import derive_review_status
from product_data_copilot.rules.validators import (
    has_useful_attributes,
    is_blank,
    is_safety_relevant_category,
    is_suspicious_image_url,
    is_valid_ean,
    is_valid_price,
)
from product_data_copilot.scoring.scoring_helpers import (
    readiness_status_from_score,
    score_from_checks,
)


def _get_value(row, field_name):
    if field_name in row.index:
        return row[field_name]
    return ""


def get_review_status(product_issues, readiness_status):
    issue_types = product_issues["issue_type"].tolist()
    severities = product_issues["severity"].tolist()
    return derive_review_status(issue_types, severities, readiness_status)


def calculate_product_scores(row):
    sku = _get_value(row, "sku")
    product_name = _get_value(row, "product_name")
    category = _get_value(row, "category")
    description = _get_value(row, "description")
    brand = _get_value(row, "brand")
    ean = _get_value(row, "ean")
    image_url = _get_value(row, "image_url")
    warning_notes = _get_value(row, "warning_notes")
    translation_de = _get_value(row, "translation_de")
    translation_en = _get_value(row, "translation_en")
    manufacturer = _get_value(row, "manufacturer")
    price = _get_value(row, "price")
    attributes = _get_value(row, "attributes")

    data_quality_score = score_from_checks(
        [
            not is_blank(sku),
            not is_blank(product_name),
            not is_blank(description),
            not is_blank(brand),
            not is_blank(category),
            not is_blank(manufacturer),
            not is_blank(ean) and is_valid_ean(ean),
        ]
    )

    marketplace_readiness_score = score_from_checks(
        [
            not is_blank(product_name),
            not is_blank(description),
            not is_blank(brand),
            not is_blank(ean) and is_valid_ean(ean),
            not is_blank(image_url) and not is_suspicious_image_url(image_url),
            not is_blank(category),
            is_valid_price(price),
            has_useful_attributes(attributes),
        ]
    )

    translation_readiness_score = score_from_checks(
        [
            not is_blank(translation_de),
            not is_blank(translation_en),
        ]
    )

    if is_safety_relevant_category(category):
        compliance_readiness_score = 100 if not is_blank(warning_notes) else 0
    else:
        compliance_readiness_score = 100

    ai_content_readiness_score = score_from_checks(
        [
            not is_blank(product_name),
            not is_blank(description),
            not is_blank(brand),
            not is_blank(description) and len(str(description).strip()) >= 30,
            has_useful_attributes(attributes),
            sum(
                [
                    not is_blank(product_name),
                    not is_blank(description),
                    not is_blank(brand),
                    has_useful_attributes(attributes),
                ]
            )
            >= 3,
        ]
    )

    overall_readiness_score = round(
        (data_quality_score * 0.35)
        + (marketplace_readiness_score * 0.25)
        + (translation_readiness_score * 0.15)
        + (compliance_readiness_score * 0.15)
        + (ai_content_readiness_score * 0.10)
    )

    return {
        "data_quality_score": data_quality_score,
        "marketplace_readiness_score": marketplace_readiness_score,
        "translation_readiness_score": translation_readiness_score,
        "compliance_readiness_score": compliance_readiness_score,
        "ai_content_readiness_score": ai_content_readiness_score,
        "overall_readiness_score": overall_readiness_score,
    }


def calculate_readiness_scores(products, issues):
    validate_product_identity(products)
    scores = []

    for row_number, row in products.iterrows():
        sku = _get_value(row, "sku")

        if is_blank(sku):
            sku = f"Row {row_number + 1}"

        product_name = _get_value(row, "product_name")
        product_issues = issues[issues["sku"] == sku]
        product_scores = calculate_product_scores(row)
        readiness_status = readiness_status_from_score(
            product_scores["overall_readiness_score"], product_issues["severity"]
        )
        review_status = get_review_status(product_issues, readiness_status)

        scores.append(
            {
                "sku": sku,
                "product_name": product_name,
                "data_quality_score": product_scores["data_quality_score"],
                "marketplace_readiness_score": product_scores[
                    "marketplace_readiness_score"
                ],
                "translation_readiness_score": product_scores[
                    "translation_readiness_score"
                ],
                "compliance_readiness_score": product_scores[
                    "compliance_readiness_score"
                ],
                "ai_content_readiness_score": product_scores[
                    "ai_content_readiness_score"
                ],
                "overall_readiness_score": product_scores["overall_readiness_score"],
                "readiness_status": readiness_status,
                "review_status": review_status,
            }
        )

    return pd.DataFrame(scores)
