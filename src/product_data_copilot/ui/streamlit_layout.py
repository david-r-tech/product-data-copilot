"""Small Streamlit layout helpers.

The helpers accept the Streamlit module as an argument so they remain import-safe
and easy to test without launching Streamlit.
"""


def configure_page(st):
    """Configure the Streamlit page."""
    st.set_page_config(page_title="Commerce Readiness AI", layout="wide")


def render_app_intro(st):
    """Render the app title and short intro caption."""
    st.title("Commerce Readiness AI")
    st.caption("CSV-based product data quality checks for e-commerce readiness.")


def render_sidebar_intro(st):
    """Render the sidebar input section header."""
    st.sidebar.header("Input")


def render_data_input_section(st):
    """Render the sidebar data upload input and return the uploaded file."""
    render_sidebar_intro(st)
    return st.sidebar.file_uploader(
        "Upload a CSV or Excel file", type=["csv", "xlsx"]
    )


def render_data_source_notice(st, data_source):
    """Render the currently used data source notice."""
    st.info(f"Using: {data_source}")


def render_dataset_summary(st, row_count, column_count):
    """Render the product data row and column summary."""
    st.caption(f"Rows: {row_count} | Columns: {column_count}")


def render_issues_summary(st, total_issues, displayed_issues):
    """Render the total and displayed issue count summary."""
    st.caption(f"Total issues: {total_issues} | Displayed issues: {displayed_issues}")


def render_no_matching_issues_notice(st):
    """Render the message shown when issue filters hide all issues."""
    st.info("No issues match the selected severity filter.")


def render_no_data_quality_issues_notice(st):
    """Render the success message shown when no issues exist."""
    st.success("No data quality issues found.")


def render_review_tasks_intro(st):
    """Render the Review Tasks tab intro caption."""
    st.caption("Review workflow overview, filters, manual status overrides, and task export.")


def render_review_tasks_summary(st, total_tasks, displayed_tasks):
    """Render the total and displayed review task count summary."""
    st.caption(f"Total review tasks: {total_tasks} | Displayed tasks: {displayed_tasks}")


def render_no_matching_review_tasks_notice(st):
    """Render the message shown when review task filters hide all tasks."""
    st.info("No review tasks match the selected filters.")


def render_no_review_tasks_notice(st):
    """Render the success message shown when no review tasks exist."""
    st.success("No review tasks needed.")
