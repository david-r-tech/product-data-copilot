import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_PATH))

from product_data_copilot.ui.streamlit_layout import (  # noqa: E402
    configure_page,
    render_app_intro,
    render_sidebar_intro,
)


class FakeSidebar:
    def __init__(self):
        self.headers = []

    def header(self, text):
        self.headers.append(text)


class FakeStreamlit:
    def __init__(self):
        self.page_config = None
        self.titles = []
        self.captions = []
        self.sidebar = FakeSidebar()

    def set_page_config(self, **kwargs):
        self.page_config = kwargs

    def title(self, text):
        self.titles.append(text)

    def caption(self, text):
        self.captions.append(text)


def test_streamlit_layout_module_imports_safely():
    assert callable(configure_page)
    assert callable(render_app_intro)
    assert callable(render_sidebar_intro)


def test_configure_page_sets_expected_streamlit_page_config():
    fake_st = FakeStreamlit()

    configure_page(fake_st)

    assert fake_st.page_config == {
        "page_title": "Commerce Readiness AI",
        "layout": "wide",
    }


def test_render_app_intro_preserves_title_and_caption():
    fake_st = FakeStreamlit()

    render_app_intro(fake_st)

    assert fake_st.titles == ["Commerce Readiness AI"]
    assert fake_st.captions == [
        "CSV-based product data quality checks for e-commerce readiness."
    ]


def test_render_sidebar_intro_preserves_input_header():
    fake_st = FakeStreamlit()

    render_sidebar_intro(fake_st)

    assert fake_st.sidebar.headers == ["Input"]
