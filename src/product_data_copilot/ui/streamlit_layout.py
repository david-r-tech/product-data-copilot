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
