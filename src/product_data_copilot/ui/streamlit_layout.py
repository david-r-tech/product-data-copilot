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
