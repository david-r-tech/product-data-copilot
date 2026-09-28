import base64
import os
import sys
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
    normalize_text as source_text,
)
from product_data_copilot.rules.attribute_consistency import explicit_attribute_conflicts  # noqa: E402
from product_data_copilot.scoring.scoring_helpers import (  # noqa: E402
    readiness_status_from_score as get_readiness_status,
    score_from_checks,
)
from product_data_copilot.review.review_helpers import (  # noqa: E402
    ALLOWED_REVIEW_STATUSES as REVIEW_STATUS_OPTIONS,
    derive_review_status,
    issue_to_task_type,
    severity_to_task_priority as get_task_priority,
)
from product_data_copilot.export.export_helpers import (  # noqa: E402
    MANAGEMENT_EXPORT_FILENAME,
    MANAGEMENT_EXPORT_SHEETS,
)
from product_data_copilot.ui.streamlit_layout import (  # noqa: E402
    render_data_input_section,
    render_data_source_notice,
    render_dataset_summary,
)
from product_data_copilot.ui.content_workspace import render_content_workspace  # noqa: E402

from product_data_copilot.data.product_input import (  # noqa: E402
    ProductInputError,
    dataset_fingerprint,
    load_product_file,
    validate_product_identity,
)
from product_data_copilot.export.serialization import (  # noqa: E402
    ExportError,
    safe_csv_bytes,
    workbook_bytes,
)
from product_data_copilot.review.session_state import (  # noqa: E402
    bind_dataset,
)

APP_NAME = "Product Data Copilot"
APP_LOGO_PATH = Path(__file__).resolve().parent / "assets" / "product_data_copilot_logo.png"

SAMPLE_DATA_PATH = Path(__file__).resolve().parent / "data" / "sample_products.csv"


def get_image_data_uri(image_path):
    """Return a base64 data URI for a local PNG image."""
    if not image_path.exists():
        return ""

    encoded_image = base64.b64encode(image_path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{encoded_image}"


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


DISPLAY_COLUMN_LABELS = {
    "sku": "SKU",
    "product_name": "Product Name",
    "category": "Category",
    "description": "Description",
    "brand": "Brand",
    "manufacturer": "Manufacturer",
    "attributes": "Attributes",
    "ean": "EAN",
    "language": "Language",
    "price": "Price",
    "image_url": "Image URL",
    "warning_notes": "Warning Notes",
    "translation_de": "Translation DE",
    "translation_en": "Translation EN",
    "data_quality_score": "Data Quality",
    "marketplace_readiness_score": "Marketplace Readiness",
    "translation_readiness_score": "Translation Readiness",
    "compliance_readiness_score": "Compliance Readiness",
    "ai_content_readiness_score": "AI Content Readiness",
    "overall_readiness_score": "Overall Score",
    "readiness_status": "Readiness Status",
    "review_status": "Review Status",
    "issue_type": "Issue Type",
    "field_name": "Field",
    "severity": "Severity",
    "message": "Issue",
    "recommended_action": "Recommended Action",
    "task_type": "Task Type",
    "priority": "Priority",
    "products": "Products",
    "tasks": "Tasks",
    "metric": "Metric",
    "value": "Value",
    "target_field": "Field",
    "field": "Field",
    "current_value": "Current Value",
    "proposed_value": "Suggested Value",
    "suggested_value": "Suggested Value",
    "original_value": "Original Value",
    "approved_value": "Approved Value",
    "source_fields": "Source Fields",
    "reason": "Reason",
    "confidence": "Confidence",
    "risk_level": "Risk",
    "human_review_status": "Human Review Status",
    "suggestion_status": "Suggestion State",
    "approval_status": "Approval Status",
    "export_status": "Export Status",
    "suggestion_id": "Suggestion ID",
    "source": "Source",
}

TEXT_HEAVY_COLUMNS = {
    "Description",
    "Attributes",
    "Image URL",
    "Warning Notes",
    "Translation DE",
    "Translation EN",
    "Reason",
    "Source Fields",
    "Suggested Value",
    "Original Value",
    "Approved Value",
    "Current Value",
    "Value",
    "Source",
}
SMALL_COLUMNS = {
    "SKU",
    "Field",
    "EAN",
    "Price",
    "Language",
    "Severity",
    "Priority",
    "Risk",
    "Confidence",
    "Products",
    "Tasks",
    "Export Status",
}
SCORE_COLUMNS = {
    "Data Quality",
    "Marketplace Readiness",
    "Translation Readiness",
    "Compliance Readiness",
    "AI Content Readiness",
    "Overall Score",
}


def prepare_display_dataframe(dataframe, preferred_columns=None):
    """Return a display-only copy with business labels and prioritized columns."""
    display_dataframe = make_display_safe(dataframe)

    if preferred_columns:
        preferred_existing_columns = [
            column for column in preferred_columns if column in display_dataframe.columns
        ]
        remaining_columns = [
            column
            for column in display_dataframe.columns
            if column not in preferred_existing_columns
        ]
        display_dataframe = display_dataframe[
            preferred_existing_columns + remaining_columns
        ]

    return display_dataframe.rename(columns=DISPLAY_COLUMN_LABELS)


def get_display_column_config(display_dataframe):
    """Return Streamlit column config for readable, display-only tables."""
    column_config = {}

    for column_name in display_dataframe.columns:
        if column_name in SCORE_COLUMNS:
            column_config[column_name] = st.column_config.NumberColumn(
                column_name,
                format="%d",
                width="small",
            )
        elif column_name in TEXT_HEAVY_COLUMNS:
            column_config[column_name] = st.column_config.TextColumn(
                column_name,
                width="large",
            )
        elif column_name in SMALL_COLUMNS:
            column_config[column_name] = st.column_config.TextColumn(
                column_name,
                width="small",
            )
        else:
            column_config[column_name] = st.column_config.TextColumn(
                column_name,
                width="medium",
            )

    return column_config


def render_readable_dataframe(
    dataframe,
    preferred_columns=None,
    height=420,
    container=None,
):
    """Render a DataFrame with display-only labels, ordering, and hidden index."""
    streamlit_target = container or st
    display_dataframe = prepare_display_dataframe(dataframe, preferred_columns)
    streamlit_target.dataframe(
        display_dataframe,
        width="stretch",
        hide_index=True,
        height=height,
        column_config=get_display_column_config(display_dataframe),
    )


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


def add_attribute_consistency_checks(issues, row, sku):
    labels = {"material": "Material", "color": "Farbe", "surface": "Oberfläche"}
    for kind, first, second in explicit_attribute_conflicts(row):
        label = labels[kind]
        add_issue(
            issues,
            sku,
            f"Different {kind} values",
            kind,
            "Warning",
            f"{label} unterschiedlich angegeben: {first[0]} = {first[1]}; {second[0]} = {second[1]}.",
            f"{label}-Angaben in den genannten Spalten mit der Produktquelle abgleichen.",
        )


def find_product_issues(products):
    validate_product_identity(products)
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
        add_attribute_consistency_checks(issues, row, sku)
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


def prioritize_issues(issues):
    """Show critical work first while preserving order within each severity."""
    severity_order = {"Critical": 0, "Warning": 1, "Info": 2}
    return (
        issues.assign(_severity_order=issues["severity"].map(severity_order).fillna(3))
        .sort_values("_severity_order", kind="stable")
        .drop(columns="_severity_order")
        .reset_index(drop=True)
    )


def get_review_status(product_issues, readiness_status):
    issue_types = product_issues["issue_type"].tolist()
    severities = product_issues["severity"].tolist()
    return derive_review_status(issue_types, severities, readiness_status)


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
    validate_product_identity(products)
    scores = []

    for row_number, row in products.iterrows():
        sku = get_value(row, "sku")

        if is_blank(sku):
            sku = f"Row {row_number + 1}"

        product_name = get_value(row, "product_name")
        product_issues = issues[issues["sku"] == sku]
        product_scores = calculate_product_scores(row)
        readiness_status = get_readiness_status(
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


def apply_manual_review_overrides(readiness_scores):
    if "manual_review_status_overrides" not in st.session_state:
        st.session_state["manual_review_status_overrides"] = {}

    updated_scores = readiness_scores.copy()

    for sku, manual_status in st.session_state["manual_review_status_overrides"].items():
        product_mask = updated_scores["sku"] == sku
        if manual_status in {"OK", "Ready for Export"}:
            product_mask &= updated_scores["readiness_status"] == "Ready"
        updated_scores.loc[
            product_mask,
            "review_status",
        ] = manual_status

    return updated_scores


def get_task_type(issue):
    return issue_to_task_type(issue["issue_type"], issue["severity"])


def create_review_tasks(issues, readiness_scores):
    tasks = []
    product_details = readiness_scores.set_index("sku")[["product_name", "review_status"]].to_dict("index")

    for _, issue in issues.iterrows():
        product = product_details.get(issue["sku"], {})
        product_name = product.get("product_name", "")
        review_status = product.get("review_status", "Needs Review")

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
    return review_tasks[
        review_tasks["priority"].isin(selected_priorities)
        & review_tasks["task_type"].isin(selected_task_types)
        & review_tasks["review_status"].isin(selected_statuses)
    ].copy()


def get_product_option(row):
    sku = row["sku"]
    product_name = row["product_name"]
    score = row["overall_readiness_score"]

    if is_blank(product_name):
        product_name = "Unnamed product"

    return f"{sku} - {product_name} - Score {score}"


def request_content_draft(prompt):
    """One paid, JSON-constrained request for one product."""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), timeout=45.0, max_retries=1)
    response = client.responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        input=prompt,
        max_output_tokens=3000,
        text={"format": {"type": "json_object"}},
    )
    return response.output_text.strip()


def create_management_summary(
    data_source,
    products,
    issues,
    readiness_scores,
    review_tasks,
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
    ]

    return pd.DataFrame(summary_rows)


def create_excel_management_export(
    data_source, products, readiness_scores, issues, review_tasks,
):
    management_summary = create_management_summary(
        data_source, products, issues, readiness_scores, review_tasks,
    )
    return workbook_bytes(dict(zip(
        MANAGEMENT_EXPORT_SHEETS,
        [management_summary, readiness_scores, issues, review_tasks, products],
    )))


def run_app():
    """Run the Streamlit app."""
    load_dotenv(Path(__file__).resolve().parent / ".env")
    st.set_page_config(page_title=APP_NAME, layout="wide")
    st.markdown(
        '<style>div[data-testid="stMainBlockContainer"] { padding-top: 2rem; }</style>',
        unsafe_allow_html=True,
    )

    logo_data_uri = get_image_data_uri(APP_LOGO_PATH)
    if logo_data_uri:
        st.markdown(
            f"""
            <div style="max-width: 340px; margin: 0 0 0.75rem 0;">
                <img
                    src="{logo_data_uri}"
                    alt="{APP_NAME} logo"
                    style="width: 100%; height: auto; display: block;"
                />
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.title(APP_NAME)

    st.caption("Produktdaten prüfen, Textentwürfe erstellen und Ergebnisse sicher exportieren.")
    st.markdown("**Ablauf:** Datei hochladen → Daten prüfen → Texte erstellen oder übersetzen → Prüfen → Exportieren")
    st.caption("Die hochgeladene Datei bleibt unverändert; KI-Texte sind Entwürfe zur fachlichen Prüfung.")

    uploaded_file = render_data_input_section(st)
    st.sidebar.caption(
        "Nutze die fiktiven Beispieldaten oder lade eine eigene Datei hoch. Prüfung und Exporte beziehen sich auf die geladenen Daten."
    )
    with st.sidebar.expander("Anforderungen an die Datei"):
        st.caption(
            "Pflichtspalten: sku und product_name. Artikelnummern müssen eindeutig und gefüllt sein. "
            "UTF-8-CSV (Komma, Semikolon oder Tab) oder erstes Blatt einer XLSX-Datei. "
            "Grenze: 1.000 Artikel / 10 MB. SKU und EAN in Excel vor der Eingabe als Text formatieren."
        )
    try:
        if uploaded_file is not None:
            file_bytes = uploaded_file.getvalue()
            filename = uploaded_file.name
            data_source = "Uploaded file"
        else:
            file_bytes = SAMPLE_DATA_PATH.read_bytes()
            filename = SAMPLE_DATA_PATH.name
            data_source = "Sample data (fictional products)"
        products = load_product_file(file_bytes, filename)
    except (ProductInputError, OSError) as error:
        bind_dataset(st.session_state, None)
        st.error(str(error) if isinstance(error, ProductInputError) else "The sample file could not be loaded.")
        st.info("Correct the file and upload it again. No product decisions or exports were created.")
        return
    bind_dataset(st.session_state, dataset_fingerprint(file_bytes, data_source + ":" + filename))

    row_count, column_count = products.shape

    issues = prioritize_issues(find_product_issues(products))
    readiness_scores = calculate_readiness_scores(products, issues)
    readiness_scores = apply_manual_review_overrides(readiness_scores)
    review_tasks = create_review_tasks(issues, readiness_scores)

    critical_issues = len(issues[issues["severity"] == "Critical"])
    products_affected = issues["sku"].nunique()

    st.sidebar.header("Probleme filtern")
    selected_severities = st.sidebar.multiselect(
        "Schweregrad",
        ["Critical", "Warning", "Info"],
        default=["Critical", "Warning", "Info"],
        format_func=lambda value: {"Critical": "Kritisch", "Warning": "Warnung", "Info": "Info"}[value],
    )

    filtered_issues = issues[issues["severity"].isin(selected_severities)]

    render_data_source_notice(st, data_source)

    tabs = st.tabs(
        [
            "Daten prüfen",
            "Texte erstellen & übersetzen",
            "Ergebnisse & Export",
        ]
    )

    with tabs[0]:
        st.subheader("Daten prüfen")
        st.caption("Welche Artikel brauchen Aufmerksamkeit – und was muss konkret korrigiert werden?")

        metric_columns = st.columns(3)
        metric_columns[0].metric("Artikel geprüft", row_count)
        metric_columns[1].metric("Artikel mit Auffälligkeiten", products_affected)
        metric_columns[2].metric("Kritische Auffälligkeiten", critical_issues)
        if critical_issues > 0:
            st.warning(
                f"{critical_issues} kritische Auffälligkeiten: Prüfe zuerst die betroffenen Quelldaten."
            )
        elif products_affected > 0:
            st.info(
                f"{products_affected} Artikel haben Auffälligkeiten. Die Korrekturliste steht unten."
            )
        else:
            st.success("Die lokalen Regeln haben keine Auffälligkeiten gefunden.")


    with tabs[0]:
        st.markdown("#### Konkrete Korrekturen")
        st.caption(
            "Jede Zeile zeigt eine gefundene Auffälligkeit und den nächsten sinnvollen Prüfschritt. "
            "Korrigiere die Quelldatei und lade sie erneut hoch, um den Stand neu zu prüfen."
        )
        product_names = products.set_index("sku")["product_name"]
        actions = filtered_issues.copy()
        actions.insert(1, "Produkt", actions["sku"].map(product_names).fillna(""))
        product_labels = {
            f"{row['sku']} · {row['product_name']}": row["sku"]
            for _, row in products.iterrows()
        }
        selected_product = st.selectbox(
            "Artikel filtern", ["Alle Artikel", *product_labels], key="audit_product_filter"
        )
        if selected_product != "Alle Artikel":
            actions = actions[actions["sku"] == product_labels[selected_product]]
        severity_labels = {"Critical": "Kritisch", "Warning": "Warnung", "Info": "Info"}
        action_view = pd.DataFrame({
            "SKU": actions["sku"],
            "Produkt": actions["Produkt"],
            "Schweregrad": actions["severity"].map(severity_labels),
            "Feld": actions["field_name"],
            "Problem": actions["message"],
            "Nächster Schritt": actions["recommended_action"],
        })
        st.caption(f"{len(action_view)} von {len(issues)} Auffälligkeiten angezeigt")
        if action_view.empty:
            st.info("Für diese Auswahl wurden keine Auffälligkeiten gefunden.")
        else:
            st.dataframe(action_view, width="stretch", hide_index=True, height=430)
        st.download_button(
            "Korrekturliste als CSV herunterladen",
            safe_csv_bytes(action_view),
            "produktdaten_korrekturen.csv",
            "text/csv",
        )

    with tabs[0], st.expander("Originaldaten ansehen"):
        st.markdown("#### Hochgeladene Produktdaten")
        st.caption(
            "Referenz für die Prüfung. KI-Texte und Exporte ändern diese Daten nicht."
        )
        render_dataset_summary(st, row_count, column_count)
        render_readable_dataframe(
            products,
            preferred_columns=[
                "sku",
                "product_name",
                "category",
                "brand",
                "manufacturer",
                "price",
                "ean",
                "description",
                "attributes",
                "translation_de",
                "translation_en",
                "image_url",
                "warning_notes",
                "language",
            ],
            height=430,
        )

    with tabs[0], st.expander("Score-Details und Prüfmethode"):
        st.markdown("#### Technische Vollständigkeitsindikatoren")
        st.caption(
            "Diese Werte zählen überwiegend ausgefüllte Felder. Sie bewerten weder die Qualität erzeugter KI-Texte "
            "noch rechtliche Konformität oder die Freigabe eines Marktplatzes."
        )
        render_readable_dataframe(
            readiness_scores,
            preferred_columns=[
                "sku",
                "product_name",
                "review_status",
                "readiness_status",
                "overall_readiness_score",
                "data_quality_score",
                "marketplace_readiness_score",
                "translation_readiness_score",
                "compliance_readiness_score",
                "ai_content_readiness_score",
            ],
            height=430,
        )
        st.download_button(
            "Score-Details als CSV herunterladen",
            safe_csv_bytes(readiness_scores),
            "product_readiness_scores.csv",
            "text/csv",
        )
    with tabs[0], st.expander("Prüfentscheidung dokumentieren (nur diese Sitzung)"):
        st.caption(
            "Hier kannst du einen Artikel für die aktuelle Sitzung markieren. "
            "Offene Auffälligkeiten werden dadurch nicht behoben; korrigiere sie in der Quelldatei."
        )
        product_options = {
            f"{row['sku']} · {row['product_name']}": row["sku"]
            for _, row in readiness_scores.iterrows()
        }
        selected_review_product = st.selectbox(
            "Artikel auswählen", list(product_options), key="manual_review_product"
        )
        selected_review_sku = product_options[selected_review_product]
        selected_review_score = readiness_scores.loc[
            readiness_scores["sku"] == selected_review_sku
        ].iloc[0]
        current_manual_status = selected_review_score["review_status"]
        allowed_manual_statuses = [
            status for status in REVIEW_STATUS_OPTIONS
            if selected_review_score["readiness_status"] == "Ready"
            or status not in {"OK", "Ready for Export"}
        ]
        status_labels = {
            "OK": "OK",
            "Needs Review": "Prüfung nötig",
            "Missing Data": "Daten fehlen",
            "AI Suggestion Created": "KI-Entwurf vorhanden",
            "Translation Missing": "Übersetzung fehlt",
            "Compliance Check Required": "Fachprüfung nötig",
            "Ready for Export": "Keine offenen Regelverstöße",
            "Rejected": "Abgelehnt",
        }
        if st.session_state.get("manual_status_product") != selected_review_sku:
            st.session_state["manual_review_status"] = current_manual_status
            st.session_state["manual_status_product"] = selected_review_sku
        if st.session_state.get("manual_review_status") not in allowed_manual_statuses:
            st.session_state["manual_review_status"] = current_manual_status
        manual_status = st.selectbox(
            "Prüfstatus", allowed_manual_statuses,
            format_func=lambda value: status_labels.get(value, value),
            key="manual_review_status",
        )
        st.caption(f"Aktueller Status: {status_labels.get(current_manual_status, current_manual_status)}")
        if selected_review_score["readiness_status"] != "Ready":
            st.caption("Offene Auffälligkeiten verhindern den Status „Keine offenen Regelverstöße“.")
        action_columns = st.columns(2)
        if action_columns[0].button("Prüfstatus speichern", type="primary"):
            st.session_state["manual_review_status_overrides"][selected_review_sku] = manual_status
            st.rerun()
        if action_columns[1].button("Prüfstatus zurücksetzen"):
            st.session_state["manual_review_status_overrides"].pop(selected_review_sku, None)
            st.session_state.pop("manual_status_product", None)
            st.rerun()

    with tabs[2]:
        st.subheader("Ergebnisse & Export")
        st.caption(
            "Lade den Qualitätsbericht für die Abstimmung herunter. Er enthält die Prüfergebnisse, "
            "Korrekturaufgaben und eine Kopie der eingelesenen Quelldaten."
        )

        management_summary = create_management_summary(
            data_source,
            products,
            issues,
            readiness_scores,
            review_tasks,
        )

        st.markdown("#### Berichtsvorschau")
        st.caption("Die Vorschau zeigt die wichtigsten Ergebnisse; der Download enthält den vollständigen Bericht.")
        preview_labels = {
            "Data source": "Datenquelle",
            "Total products": "Geprüfte Artikel",
            "Products affected by issues": "Artikel mit Auffälligkeiten",
            "Critical issues": "Kritische Auffälligkeiten",
            "Total issues": "Auffälligkeiten insgesamt",
        }
        preview = management_summary[
            management_summary["metric"].isin(preview_labels)
        ].copy()
        preview["metric"] = preview["metric"].map(preview_labels)
        preview["value"] = preview["value"].replace({
            "Sample data (fictional products)": "Beispieldaten (fiktive Produkte)",
            "Uploaded file": "Hochgeladene Datei",
        })
        preview.columns = ["Kennzahl", "Wert"]
        st.dataframe(preview, width="stretch", hide_index=True, height=240)

        try:
            management_bytes = create_excel_management_export(
                data_source, products, readiness_scores, issues, review_tasks,
            )
        except ExportError as error:
            st.error(str(error))
        else:
            st.download_button(
                "Qualitätsbericht als Excel herunterladen", management_bytes, MANAGEMENT_EXPORT_FILENAME,
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", type="primary",
            )
        st.caption(
            "Die Scores sind technische Indikatoren, keine Freigabe für Marktplätze oder rechtliche Konformität. "
            "Originaltexte werden als Text exportiert; die hochgeladene Datei bleibt unverändert."
        )

    with tabs[1]:
        render_content_workspace(
            st, products, request_content_draft, workbook_bytes,
            has_key=bool(os.getenv("OPENAI_API_KEY")),
        )

if __name__ == "__main__":
    run_app()
