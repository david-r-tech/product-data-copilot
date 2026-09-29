"""Pure review-task and manual-status orchestration."""

import pandas as pd

from product_data_copilot.review.review_helpers import (
    ALLOWED_REVIEW_STATUSES,
    REVIEW_STATUS_NEEDS_REVIEW,
    REVIEW_STATUS_OK,
    REVIEW_STATUS_READY_FOR_EXPORT,
    issue_to_task_type,
    severity_to_task_priority,
)


PROTECTED_READY_STATUSES = {REVIEW_STATUS_OK, REVIEW_STATUS_READY_FOR_EXPORT}


def allowed_manual_review_statuses(readiness_status):
    """Return manual statuses allowed by the product's technical readiness."""
    return [
        status
        for status in ALLOWED_REVIEW_STATUSES
        if readiness_status == "Ready" or status not in PROTECTED_READY_STATUSES
    ]


def apply_manual_review_overrides(readiness_scores, overrides):
    """Apply session-provided overrides without bypassing readiness gates."""
    updated_scores = readiness_scores.copy()

    for sku, manual_status in overrides.items():
        product_mask = updated_scores["sku"] == sku
        if manual_status in PROTECTED_READY_STATUSES:
            product_mask &= updated_scores["readiness_status"] == "Ready"
        updated_scores.loc[product_mask, "review_status"] = manual_status

    return updated_scores


def get_task_type(issue):
    return issue_to_task_type(issue["issue_type"], issue["severity"])


def create_review_tasks(issues, readiness_scores):
    tasks = []
    product_details = readiness_scores.set_index("sku")[["product_name", "review_status"]].to_dict("index")

    for _, issue in issues.iterrows():
        product = product_details.get(issue["sku"], {})
        product_name = product.get("product_name", "")
        review_status = product.get("review_status", REVIEW_STATUS_NEEDS_REVIEW)

        tasks.append(
            {
                "sku": issue["sku"],
                "product_name": product_name,
                "issue_type": issue["issue_type"],
                "field_name": issue["field_name"],
                "task_type": get_task_type(issue),
                "priority": severity_to_task_priority(issue["severity"]),
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
