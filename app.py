import json
import os
import sys
from io import BytesIO
from pathlib import Path

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

SRC_PATH = Path(__file__).resolve().parent / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from product_data_copilot.rules.validators import (  # noqa: E402
    has_useful_attributes,
    is_blank,
    is_generic_product_name,
    is_safety_relevant_category,
    is_suspicious_image_url,
    is_valid_ean,
    is_valid_price,
)
from product_data_copilot.scoring.scoring_helpers import (  # noqa: E402
    readiness_status_from_score as get_readiness_status,
    score_from_checks,
)
from product_data_copilot.ui.streamlit_layout import (  # noqa: E402
    configure_page,
    render_app_intro,
    render_data_input_section,
    render_data_source_notice,
    render_dataset_summary,
    render_issues_summary,
    render_no_data_quality_issues_notice,
    render_no_matching_issues_notice,
    render_no_matching_review_tasks_notice,
    render_no_review_tasks_notice,
    render_review_tasks_intro,
    render_review_tasks_summary,
)

load_dotenv()

REVIEW_STATUS_OPTIONS = [
    "OK",
    "Needs Review",
    "Missing Data",
    "AI Suggestion Created",
    "Translation Missing",
    "Compliance Check Required",
    "Ready for Export",
    "Rejected",
]

AI_SUGGESTION_TYPES = [
    "Improved Product Title",
    "Product Description",
    "Bullet Points",
    "Missing Attribute Suggestions",
    "Translation DE to EN",
    "Translation EN to DE",
    "Compliance / Safety Review Note",
]


def get_value(row, field_name):
    if field_name in row.index:
        return row[field_name]
    return ""


def make_display_safe(dataframe):
    display_dataframe = dataframe.copy()

    for column in display_dataframe.columns:
        if display_dataframe[column].dtype == "object":
            display_dataframe[column] = display_dataframe[column].fillna("").astype(str)

    return display_dataframe


def add_issue(issues, sku, issue_type, field_name, severity, message, recommended_action):
    issues.append(
        {
            "sku": sku,
            "issue_type": issue_type,
            "field_name": field_name,
            "severity": severity,
            "message": message,
            "recommended_action": recommended_action,
        }
    )


def add_core_data_checks(issues, row, sku):
    product_name = get_value(row, "product_name")
    description = get_value(row, "description")
    brand = get_value(row, "brand")
    ean = get_value(row, "ean")
    category = get_value(row, "category")
    manufacturer = get_value(row, "manufacturer")

    if is_blank(product_name):
        add_issue(
            issues,
            sku,
            "Missing product_name",
            "product_name",
            "Critical",
            "Product name is missing.",
            "Add a clear product name.",
        )
    elif len(str(product_name).strip()) < 10:
        add_issue(
            issues,
            sku,
            "Short product_name",
            "product_name",
            "Warning",
            "Product name is shorter than 10 characters.",
            "Use a more descriptive product name.",
        )
    elif is_generic_product_name(product_name):
        add_issue(
            issues,
            sku,
            "Generic product_name",
            "product_name",
            "Warning",
            "Product name is too generic for marketplace use.",
            "Add product type, brand, or key attribute to the title.",
        )

    if is_blank(description):
        add_issue(
            issues,
            sku,
            "Missing description",
            "description",
            "Critical",
            "Product description is missing.",
            "Add a helpful product description.",
        )
    elif len(str(description).strip()) < 30:
        add_issue(
            issues,
            sku,
            "Short description",
            "description",
            "Warning",
            "Description is shorter than 30 characters.",
            "Add more detail about the product.",
        )

    if is_blank(brand):
        add_issue(
            issues,
            sku,
            "Missing brand",
            "brand",
            "Warning",
            "Brand is missing.",
            "Add the product brand.",
        )

    if is_blank(ean):
        add_issue(
            issues,
            sku,
            "Missing ean",
            "ean",
            "Critical",
            "EAN is missing.",
            "Add a valid product EAN.",
        )
    elif not is_valid_ean(ean):
        add_issue(
            issues,
            sku,
            "Invalid ean",
            "ean",
            "Critical",
            "EAN format looks invalid.",
            "Add a valid 8, 12, 13, or 14 digit EAN/GTIN.",
        )

    if is_blank(category):
        add_issue(
            issues,
            sku,
            "Missing category",
            "category",
            "Critical",
            "Product category is missing.",
            "Add a clear product category.",
        )

    if is_blank(manufacturer):
        add_issue(
            issues,
            sku,
            "Missing manufacturer",
            "manufacturer",
            "Warning",
            "Manufacturer is missing.",
            "Add manufacturer when available.",
        )


def add_marketplace_checks(issues, row, sku):
    price = get_value(row, "price")
    attributes = get_value(row, "attributes")

    if is_blank(price):
        add_issue(
            issues,
            sku,
            "Missing price",
            "price",
            "Warning",
            "Product price is missing.",
            "Add a product price before marketplace review.",
        )
    elif not is_valid_price(price):
        add_issue(
            issues,
            sku,
            "Invalid price",
            "price",
            "Warning",
            "Product price must be greater than 0.",
            "Check and correct the product price.",
        )

    if not has_useful_attributes(attributes):
        add_issue(
            issues,
            sku,
            "Missing attributes",
            "attributes",
            "Warning",
            "Product attributes are missing.",
            "Add key attributes such as color, size, material, capacity, or dimensions.",
        )


def add_content_quality_checks(issues, row, sku):
    product_name = get_value(row, "product_name")

    if not is_blank(product_name) and is_generic_product_name(product_name):
        existing_name_issues = [
            issue
            for issue in issues
            if issue["sku"] == sku and issue["field_name"] == "product_name"
        ]

        if len(existing_name_issues) == 0:
            add_issue(
                issues,
                sku,
                "Generic product_name",
                "product_name",
                "Warning",
                "Product name is too generic for marketplace use.",
                "Add product type, brand, or key attribute to the title.",
            )


def add_translation_checks(issues, row, sku):
    translation_de = get_value(row, "translation_de")
    translation_en = get_value(row, "translation_en")

    if is_blank(translation_de):
        add_issue(
            issues,
            sku,
            "Missing translation_de",
            "translation_de",
            "Warning",
            "German translation is missing.",
            "Add the German product translation.",
        )

    if is_blank(translation_en):
        add_issue(
            issues,
            sku,
            "Missing translation_en",
            "translation_en",
            "Warning",
            "English translation is missing.",
            "Add the English product translation.",
        )


def add_compliance_checks(issues, row, sku):
    category = get_value(row, "category")
    warning_notes = get_value(row, "warning_notes")

    if is_safety_relevant_category(category) and is_blank(warning_notes):
        add_issue(
            issues,
            sku,
            "Missing warning_notes",
            "warning_notes",
            "Warning",
            "Safety-relevant product is missing warning notes.",
            "Add safety or usage warning notes and review compliance needs.",
        )


def add_media_checks(issues, row, sku):
    image_url = get_value(row, "image_url")

    if is_blank(image_url):
        add_issue(
            issues,
            sku,
            "Missing image_url",
            "image_url",
            "Info",
            "Image URL is missing.",
            "Add a product image URL.",
        )
    elif is_suspicious_image_url(image_url):
        add_issue(
            issues,
            sku,
            "Image URL suspicious",
            "image_url",
            "Info",
            "Image URL looks incomplete or non-public.",
            "Add a complete public image URL.",
        )


def find_product_issues(products):
    issues = []

    for row_number, row in products.iterrows():
        sku = get_value(row, "sku")

        if is_blank(sku):
            sku = f"Row {row_number + 1}"

        add_core_data_checks(issues, row, sku)
        add_marketplace_checks(issues, row, sku)
        add_content_quality_checks(issues, row, sku)
        add_translation_checks(issues, row, sku)
        add_compliance_checks(issues, row, sku)
        add_media_checks(issues, row, sku)

    return pd.DataFrame(
        issues,
        columns=[
            "sku",
            "issue_type",
            "field_name",
            "severity",
            "message",
            "recommended_action",
        ],
    )


def get_review_status(product_issues, readiness_status):
    issue_types = product_issues["issue_type"].tolist()

    if "Critical" in product_issues["severity"].tolist():
        return "Missing Data"
    if "Missing warning_notes" in issue_types:
        return "Compliance Check Required"
    if "Missing translation_de" in issue_types or "Missing translation_en" in issue_types:
        return "Translation Missing"
    if readiness_status == "Ready":
        return "Ready for Export"
    return "Needs Review"


def calculate_product_scores(row):
    sku = get_value(row, "sku")
    product_name = get_value(row, "product_name")
    category = get_value(row, "category")
    description = get_value(row, "description")
    brand = get_value(row, "brand")
    ean = get_value(row, "ean")
    image_url = get_value(row, "image_url")
    warning_notes = get_value(row, "warning_notes")
    translation_de = get_value(row, "translation_de")
    translation_en = get_value(row, "translation_en")
    manufacturer = get_value(row, "manufacturer")
    price = get_value(row, "price")
    attributes = get_value(row, "attributes")

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
    scores = []

    for row_number, row in products.iterrows():
        sku = get_value(row, "sku")

        if is_blank(sku):
            sku = f"Row {row_number + 1}"

        product_name = get_value(row, "product_name")
        product_issues = issues[issues["sku"] == sku]
        product_scores = calculate_product_scores(row)
        readiness_status = get_readiness_status(
            product_scores["overall_readiness_score"]
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


def apply_manual_review_overrides(readiness_scores):
    if "manual_review_status_overrides" not in st.session_state:
        st.session_state["manual_review_status_overrides"] = {}

    updated_scores = readiness_scores.copy()

    for sku, manual_status in st.session_state["manual_review_status_overrides"].items():
        updated_scores.loc[
            updated_scores["sku"] == sku,
            "review_status",
        ] = manual_status

    return updated_scores


def get_task_type(issue):
    if issue["severity"] == "Critical":
        return "Data Completion"
    if issue["issue_type"] == "Missing manufacturer":
        return "Data Completion"
    if issue["issue_type"] in ["Missing price", "Invalid price"]:
        return "Commercial Review"
    if issue["issue_type"] == "Missing attributes":
        return "Attribute Enrichment"
    if issue["issue_type"] in ["Missing translation_de", "Missing translation_en"]:
        return "Translation"
    if issue["issue_type"] == "Missing warning_notes":
        return "Compliance Review"
    if issue["issue_type"] in [
        "Short product_name",
        "Short description",
        "Generic product_name",
    ]:
        return "Content Improvement"
    if issue["issue_type"] in ["Missing image_url", "Image URL suspicious"]:
        return "Media Improvement"
    return "General Review"


def get_task_priority(severity):
    if severity == "Critical":
        return "High"
    if severity == "Warning":
        return "Medium"
    return "Low"


def create_review_tasks(issues, readiness_scores):
    tasks = []

    for _, issue in issues.iterrows():
        product_score = readiness_scores[readiness_scores["sku"] == issue["sku"]]

        if len(product_score) > 0:
            product_name = product_score.iloc[0]["product_name"]
            review_status = product_score.iloc[0]["review_status"]
        else:
            product_name = ""
            review_status = "Needs Review"

        tasks.append(
            {
                "sku": issue["sku"],
                "product_name": product_name,
                "issue_type": issue["issue_type"],
                "field_name": issue["field_name"],
                "task_type": get_task_type(issue),
                "priority": get_task_priority(issue["severity"]),
                "recommended_action": issue["recommended_action"],
                "review_status": review_status,
            }
        )

    return pd.DataFrame(
        tasks,
        columns=[
            "sku",
            "product_name",
            "issue_type",
            "field_name",
            "task_type",
            "priority",
            "recommended_action",
            "review_status",
        ],
    )


def get_filter_options(dataframe, column_name):
    if len(dataframe) == 0 or column_name not in dataframe.columns:
        return []

    values = dataframe[column_name].dropna().astype(str).unique().tolist()
    return sorted(values)


def filter_review_tasks(review_tasks, selected_priorities, selected_task_types, selected_statuses):
    filtered_tasks = review_tasks.copy()

    if len(selected_priorities) > 0:
        filtered_tasks = filtered_tasks[filtered_tasks["priority"].isin(selected_priorities)]

    if len(selected_task_types) > 0:
        filtered_tasks = filtered_tasks[filtered_tasks["task_type"].isin(selected_task_types)]

    if len(selected_statuses) > 0:
        filtered_tasks = filtered_tasks[filtered_tasks["review_status"].isin(selected_statuses)]

    return filtered_tasks


def get_product_option(row):
    sku = row["sku"]
    product_name = row["product_name"]
    score = row["overall_readiness_score"]

    if is_blank(product_name):
        product_name = "Unnamed product"

    return f"{sku} - {product_name} - Score {score}"


def get_ai_product_context(product, product_score):
    return {
        "sku": product_score.get("sku", get_value(product, "sku")),
        "product_name": get_value(product, "product_name"),
        "category": get_value(product, "category"),
        "brand": get_value(product, "brand"),
        "manufacturer": get_value(product, "manufacturer"),
        "description": get_value(product, "description"),
        "attributes": get_value(product, "attributes"),
        "overall_readiness_score": product_score.get("overall_readiness_score", ""),
        "readiness_status": product_score.get("readiness_status", ""),
        "review_status": product_score.get("review_status", ""),
    }


def build_ai_prompt(product, product_issues, product_score, selected_suggestion_types):
    product_context = get_ai_product_context(product, product_score)
    issues_context = product_issues.to_dict(orient="records")
    scores_context = product_score.to_dict()

    return f"""
You are helping with an e-commerce product data audit.

Create human-review suggestions for exactly one product.
Only generate sections requested in the selected suggestion types.
If a selected section is not applicable, return a short note explaining why.
Do not invent technical attributes or unverifiable claims.
Flag uncertainty clearly.
Do not claim legal compliance.
Do not say the product is legally safe.
If the product is compliance-relevant or has missing warning notes, the review note must say that a human must check the warning and compliance information.
All suggestions are draft recommendations and require human review before use.

Return only valid JSON with these keys:
- improved_product_title
- improved_product_description
- bullet_points
- suggested_missing_attributes
- translation
- compliance_safety_review_note
- human_review_notes

Selected suggestion types:
{json.dumps(selected_suggestion_types, ensure_ascii=False, default=str)}

Product data:
{json.dumps(product_context, ensure_ascii=False, default=str)}

Current issues:
{json.dumps(issues_context, ensure_ascii=False, default=str)}

Current scores:
{json.dumps(scores_context, ensure_ascii=False, default=str)}
"""


def generate_ai_suggestions(product, product_issues, product_score, selected_suggestion_types):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    prompt = build_ai_prompt(product, product_issues, product_score, selected_suggestion_types)

    response = client.responses.create(
        model=model,
        input=prompt,
    )

    response_text = response.output_text.strip()

    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        return {
            "improved_product_title": "",
            "improved_product_description": "",
            "bullet_points": "",
            "suggested_missing_attributes": "",
            "translation": "",
            "compliance_safety_review_note": "",
            "human_review_notes": "AI response was not valid JSON. Please review manually.",
            "raw_response": response_text,
        }


def suggestions_to_dataframe(sku, suggestions):
    return pd.DataFrame(
        [
            {
                "sku": sku,
                "selected_suggestion_types": ", ".join(
                    suggestions.get("selected_suggestion_types", [])
                ),
                "improved_product_title": suggestions.get("improved_product_title", ""),
                "improved_product_description": suggestions.get(
                    "improved_product_description", ""
                ),
                "bullet_points": suggestions.get("bullet_points", ""),
                "suggested_missing_attributes": suggestions.get(
                    "suggested_missing_attributes", ""
                ),
                "translation": suggestions.get("translation", ""),
                "compliance_safety_review_note": suggestions.get(
                    "compliance_safety_review_note", ""
                ),
                "human_review_notes": suggestions.get("human_review_notes", ""),
            }
        ]
    )


def create_management_summary(
    data_source,
    products,
    issues,
    readiness_scores,
    review_tasks,
    ai_suggestions,
):
    ready_products = len(readiness_scores[readiness_scores["readiness_status"] == "Ready"])
    needs_review_products = len(
        readiness_scores[readiness_scores["readiness_status"] == "Needs Review"]
    )
    critical_products = len(
        readiness_scores[readiness_scores["readiness_status"] == "Critical"]
    )

    summary_rows = [
        {"metric": "Data source", "value": data_source},
        {"metric": "Total products", "value": len(products)},
        {"metric": "Total issues", "value": len(issues)},
        {
            "metric": "Critical issues",
            "value": len(issues[issues["severity"] == "Critical"]),
        },
        {
            "metric": "Warning issues",
            "value": len(issues[issues["severity"] == "Warning"]),
        },
        {"metric": "Info issues", "value": len(issues[issues["severity"] == "Info"])},
        {"metric": "Products affected by issues", "value": issues["sku"].nunique()},
        {
            "metric": "Average overall readiness score",
            "value": round(readiness_scores["overall_readiness_score"].mean()),
        },
        {"metric": "Ready products", "value": ready_products},
        {"metric": "Needs Review products", "value": needs_review_products},
        {"metric": "Critical products", "value": critical_products},
        {"metric": "Total review tasks", "value": len(review_tasks)},
        {
            "metric": "High priority tasks",
            "value": len(review_tasks[review_tasks["priority"] == "High"]),
        },
        {
            "metric": "Medium priority tasks",
            "value": len(review_tasks[review_tasks["priority"] == "Medium"]),
        },
        {
            "metric": "Low priority tasks",
            "value": len(review_tasks[review_tasks["priority"] == "Low"]),
        },
        {
            "metric": "AI suggestions included",
            "value": "Yes" if len(ai_suggestions) > 0 else "No",
        },
    ]

    return pd.DataFrame(summary_rows)


def get_ai_suggestions_export_dataframe():
    columns = [
        "sku",
        "selected_suggestion_types",
        "improved_product_title",
        "improved_product_description",
        "bullet_points",
        "suggested_missing_attributes",
        "translation",
        "compliance_safety_review_note",
        "human_review_notes",
    ]

    if "ai_suggestions" not in st.session_state:
        return pd.DataFrame(columns=columns)

    sku = st.session_state.get("ai_suggestions_sku", "")
    suggestions = st.session_state["ai_suggestions"]
    return suggestions_to_dataframe(sku, suggestions)


def create_excel_management_export(
    data_source,
    products,
    readiness_scores,
    issues,
    review_tasks,
    ai_suggestions,
):
    output = BytesIO()
    management_summary = create_management_summary(
        data_source,
        products,
        issues,
        readiness_scores,
        review_tasks,
        ai_suggestions,
    )

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        management_summary.to_excel(
            writer, sheet_name="Management Summary", index=False
        )
        readiness_scores.to_excel(writer, sheet_name="Product Scores", index=False)
        issues.to_excel(writer, sheet_name="Issues", index=False)
        review_tasks.to_excel(writer, sheet_name="Review Tasks", index=False)
        ai_suggestions.to_excel(writer, sheet_name="AI Suggestions", index=False)
        products.to_excel(writer, sheet_name="Source Products", index=False)

    output.seek(0)
    return output.getvalue()


def run_app():
    """Run the Streamlit app."""
    configure_page(st)
    render_app_intro(st)

    uploaded_file = render_data_input_section(st)

    if uploaded_file is not None:
        if uploaded_file.name.endswith(".xlsx"):
            products = pd.read_excel(uploaded_file)
        else:
            products = pd.read_csv(uploaded_file)
        data_source = "Uploaded file"
    else:
        products = pd.read_csv("data/sample_products.csv")
        data_source = "Sample data"

    row_count, column_count = products.shape

    issues = find_product_issues(products)
    readiness_scores = calculate_readiness_scores(products, issues)
    readiness_scores = apply_manual_review_overrides(readiness_scores)
    review_tasks = create_review_tasks(issues, readiness_scores)

    critical_issues = len(issues[issues["severity"] == "Critical"])
    warning_issues = len(issues[issues["severity"] == "Warning"])
    info_issues = len(issues[issues["severity"] == "Info"])
    products_affected = issues["sku"].nunique()

    st.sidebar.header("Issue Filter")
    selected_severities = st.sidebar.multiselect(
        "Filter by severity",
        ["Critical", "Warning", "Info"],
        default=["Critical", "Warning", "Info"],
    )

    filtered_issues = issues[issues["severity"].isin(selected_severities)]

    render_data_source_notice(st, data_source)

    tabs = st.tabs(
        [
            "Dashboard",
            "Product Data",
            "Scores",
            "Issues",
            "Review Tasks",
            "Management Export",
            "AI Suggestions",
        ]
    )

    with tabs[0]:
        st.subheader("Dashboard")

        metric_columns = st.columns(3)
        metric_columns[0].metric("Total products", row_count)
        metric_columns[1].metric("Total issues", len(issues))
        metric_columns[2].metric("Products affected", products_affected)

        severity_columns = st.columns(3)
        severity_columns[0].metric("Critical issues", critical_issues)
        severity_columns[1].metric("Warning issues", warning_issues)
        severity_columns[2].metric("Info issues", info_issues)

        average_score = round(readiness_scores["overall_readiness_score"].mean())
        average_score_columns = st.columns(3)
        average_score_columns[0].metric("Average overall score", average_score)
        average_score_columns[1].metric(
            "Average data quality",
            round(readiness_scores["data_quality_score"].mean()),
        )
        average_score_columns[2].metric(
            "Average marketplace readiness",
            round(readiness_scores["marketplace_readiness_score"].mean()),
        )

    with tabs[1]:
        st.subheader("Product Data")
        render_dataset_summary(st, row_count, column_count)
        st.dataframe(make_display_safe(products), width="stretch")

    with tabs[2]:
        st.subheader("Product Readiness Scores")
        st.dataframe(make_display_safe(readiness_scores), width="stretch")
        st.download_button(
            "Download Product Readiness Scores",
            readiness_scores.to_csv(index=False),
            "product_readiness_scores.csv",
            "text/csv",
        )

    with tabs[3]:
        st.subheader("Data Quality Issues")
        render_issues_summary(st, len(issues), len(filtered_issues))

        if len(filtered_issues) > 0:
            st.dataframe(make_display_safe(filtered_issues), width="stretch")
        elif len(issues) > 0:
            render_no_matching_issues_notice(st)
        else:
            render_no_data_quality_issues_notice(st)

        st.download_button(
            "Download Data Quality Issues",
            issues.to_csv(index=False),
            "data_quality_issues.csv",
            "text/csv",
        )

    with tabs[4]:
        st.subheader("Review Tasks")
        render_review_tasks_intro(st)

        st.write("Product Review Overview")
        high_priority_tasks = len(review_tasks[review_tasks["priority"] == "High"])
        medium_priority_tasks = len(review_tasks[review_tasks["priority"] == "Medium"])
        low_priority_tasks = len(review_tasks[review_tasks["priority"] == "Low"])
        ready_for_export_products = len(
            readiness_scores[readiness_scores["review_status"] == "Ready for Export"]
        )
        not_ready_for_export_products = len(readiness_scores) - ready_for_export_products

        overview_columns = st.columns(3)
        overview_columns[0].metric("Total review tasks", len(review_tasks))
        overview_columns[1].metric("High priority tasks", high_priority_tasks)
        overview_columns[2].metric("Medium priority tasks", medium_priority_tasks)

        readiness_columns = st.columns(3)
        readiness_columns[0].metric("Low priority tasks", low_priority_tasks)
        readiness_columns[1].metric("Ready for Export", ready_for_export_products)
        readiness_columns[2].metric("Not Ready for Export", not_ready_for_export_products)

        status_counts = (
            readiness_scores["review_status"]
            .value_counts()
            .rename_axis("review_status")
            .reset_index(name="products")
        )
        priority_counts = (
            review_tasks["priority"]
            .value_counts()
            .rename_axis("priority")
            .reset_index(name="tasks")
        )
        task_type_counts = (
            review_tasks["task_type"]
            .value_counts()
            .head(5)
            .rename_axis("task_type")
            .reset_index(name="tasks")
        )

        summary_columns = st.columns(3)
        summary_columns[0].write("Products by review status")
        summary_columns[0].dataframe(make_display_safe(status_counts), width="stretch")
        summary_columns[1].write("Tasks by priority")
        summary_columns[1].dataframe(make_display_safe(priority_counts), width="stretch")
        summary_columns[2].write("Top task types")
        summary_columns[2].dataframe(make_display_safe(task_type_counts), width="stretch")

        st.write("Manual Review Status Override")
        product_options = {
            get_product_option(row): row["sku"] for _, row in readiness_scores.iterrows()
        }
        selected_review_product = st.selectbox(
            "Select SKU",
            list(product_options.keys()),
            key="manual_review_product",
        )
        selected_review_sku = product_options[selected_review_product]
        current_manual_status = st.session_state["manual_review_status_overrides"].get(
            selected_review_sku,
            "Needs Review",
        )
        manual_status = st.selectbox(
            "Manual review status",
            REVIEW_STATUS_OPTIONS,
            index=REVIEW_STATUS_OPTIONS.index(current_manual_status),
            key="manual_review_status",
        )

        action_columns = st.columns(2)
        if action_columns[0].button("Save Manual Review Status"):
            st.session_state["manual_review_status_overrides"][
                selected_review_sku
            ] = manual_status
            st.rerun()

        if action_columns[1].button("Clear Manual Review Status"):
            st.session_state["manual_review_status_overrides"].pop(selected_review_sku, None)
            st.rerun()

        st.write("Task Filters")
        filter_columns = st.columns(3)
        priority_options = get_filter_options(review_tasks, "priority")
        task_type_options = get_filter_options(review_tasks, "task_type")
        review_status_options = get_filter_options(review_tasks, "review_status")

        selected_priorities = filter_columns[0].multiselect(
            "Priority",
            priority_options,
            default=priority_options,
        )
        selected_task_types = filter_columns[1].multiselect(
            "Task type",
            task_type_options,
            default=task_type_options,
        )
        selected_review_statuses = filter_columns[2].multiselect(
            "Review status",
            review_status_options,
            default=review_status_options,
        )

        filtered_review_tasks = filter_review_tasks(
            review_tasks,
            selected_priorities,
            selected_task_types,
            selected_review_statuses,
        )

        render_review_tasks_summary(st, len(review_tasks), len(filtered_review_tasks))

        if len(filtered_review_tasks) > 0:
            st.dataframe(make_display_safe(filtered_review_tasks), width="stretch")
        elif len(review_tasks) > 0:
            render_no_matching_review_tasks_notice(st)
        else:
            render_no_review_tasks_notice(st)

        st.download_button(
            "Download Review Tasks",
            filtered_review_tasks.to_csv(index=False),
            "review_tasks.csv",
            "text/csv",
        )

    with tabs[5]:
        st.subheader("Management Export")
        st.caption(
            "Download one Excel workbook with summary metrics, scores, issues, review tasks, AI suggestions, and source products."
        )

        ai_suggestions_export = get_ai_suggestions_export_dataframe()
        management_summary = create_management_summary(
            data_source,
            products,
            issues,
            readiness_scores,
            review_tasks,
            ai_suggestions_export,
        )

        st.write("Management Summary Preview")
        st.dataframe(make_display_safe(management_summary), width="stretch")

        st.download_button(
            "Download Excel Management Export",
            create_excel_management_export(
                data_source,
                products,
                readiness_scores,
                issues,
                review_tasks,
                ai_suggestions_export,
            ),
            "commerce_readiness_ai_management_export.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    with tabs[6]:
        st.subheader("AI Suggestions")
        st.caption(
            "Generate structured suggestions for one selected product. Suggestions are not applied automatically."
        )
        st.warning(
            "AI suggestions are draft recommendations and must be reviewed by a human before use."
        )
        st.write(
            "By default, the product with the lowest readiness score is selected to focus AI support on the most critical item."
        )

        product_options = {
            get_product_option(row): row_number
            for row_number, row in readiness_scores.iterrows()
        }
        default_product_index = 0

        if len(readiness_scores) > 0 and "overall_readiness_score" in readiness_scores.columns:
            lowest_score_row = readiness_scores["overall_readiness_score"].idxmin()
            default_product_index = list(readiness_scores.index).index(lowest_score_row)

        selected_product_label = st.selectbox(
            "Select a product",
            list(product_options.keys()),
            index=default_product_index,
        )
        selected_row_number = product_options[selected_product_label]
        selected_product = products.iloc[selected_row_number]
        selected_score = readiness_scores.iloc[selected_row_number]
        selected_sku = selected_score["sku"]
        selected_issues = issues[issues["sku"] == selected_sku]
        selected_product_context = get_ai_product_context(selected_product, selected_score)

        selected_suggestion_types = st.multiselect(
            "Select suggestion types",
            AI_SUGGESTION_TYPES,
            default=[
                "Improved Product Title",
                "Product Description",
                "Bullet Points",
                "Missing Attribute Suggestions",
            ],
        )

        st.write("Selected product context")
        st.dataframe(make_display_safe(pd.DataFrame([selected_product_context])), width="stretch")

        st.write("Current issues for this product")
        if len(selected_issues) > 0:
            st.dataframe(make_display_safe(selected_issues), width="stretch")
        else:
            st.success("No issues found for this product.")

        if not os.getenv("OPENAI_API_KEY"):
            st.info(
                "AI generation requires an API key. AI suggestions are disabled because OPENAI_API_KEY is missing."
            )
            with st.expander("Prompt preview"):
                st.text(
                    build_ai_prompt(
                        selected_product,
                        selected_issues,
                        selected_score,
                        selected_suggestion_types,
                    )
                )
        elif len(selected_suggestion_types) == 0:
            st.info("Select at least one suggestion type to generate AI suggestions.")
        elif st.button(
            "Generate AI Suggestions",
        ):
            with st.spinner("Generating AI suggestions..."):
                try:
                    suggestions = generate_ai_suggestions(
                        selected_product,
                        selected_issues,
                        selected_score,
                        selected_suggestion_types,
                    )
                    suggestions["selected_suggestion_types"] = selected_suggestion_types
                    st.session_state["ai_suggestions"] = suggestions
                    st.session_state["ai_suggestions_sku"] = selected_sku
                except Exception as error:
                    st.error(
                        "AI suggestion generation failed. Please check your API key, network connection, or model availability."
                    )
                    with st.expander("Technical details"):
                        st.write(str(error))

        if (
            "ai_suggestions" in st.session_state
            and st.session_state.get("ai_suggestions_sku") == selected_sku
        ):
            suggestions = st.session_state["ai_suggestions"]
            bulletpoints = suggestions.get("bullet_points", "")

            if isinstance(bulletpoints, list):
                bulletpoints_text = "\n".join([f"- {item}" for item in bulletpoints])
            else:
                bulletpoints_text = str(bulletpoints)

            st.markdown("### Improved Product Title")
            st.write(suggestions.get("improved_product_title", ""))

            st.markdown("### Improved Product Description")
            st.write(suggestions.get("improved_product_description", ""))

            st.markdown("### Bullet Points")
            st.write(bulletpoints_text)

            st.markdown("### Suggested Missing Attributes")
            st.write(suggestions.get("suggested_missing_attributes", ""))

            st.markdown("### Translation")
            st.write(suggestions.get("translation", ""))

            st.markdown("### Compliance / Safety Review Note")
            st.write(suggestions.get("compliance_safety_review_note", ""))

            st.markdown("### Human Review Notes")
            st.write(suggestions.get("human_review_notes", ""))

            if suggestions.get("raw_response"):
                st.markdown("### Raw AI response")
                st.text(suggestions["raw_response"])

            st.download_button(
                "Download AI Suggestions",
                suggestions_to_dataframe(selected_sku, suggestions).to_csv(index=False),
                "ai_suggestions.csv",
                "text/csv",
            )


run_app()
