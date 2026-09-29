"""Management-report construction and workbook orchestration."""

import pandas as pd

from product_data_copilot.export.export_helpers import MANAGEMENT_EXPORT_SHEETS
from product_data_copilot.export.serialization import workbook_bytes


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


def prepare_management_workbook_sheets(
    data_source, products, readiness_scores, issues, review_tasks,
):
    management_summary = create_management_summary(
        data_source, products, issues, readiness_scores, review_tasks,
    )
    return dict(zip(
        MANAGEMENT_EXPORT_SHEETS,
        [management_summary, readiness_scores, issues, review_tasks, products],
    ))


def create_excel_management_export(
    data_source, products, readiness_scores, issues, review_tasks,
):
    return workbook_bytes(prepare_management_workbook_sheets(
        data_source, products, readiness_scores, issues, review_tasks,
    ))
