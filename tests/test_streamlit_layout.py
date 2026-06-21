import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_PATH))

from product_data_copilot.ui.streamlit_layout import (  # noqa: E402
    configure_page,
    render_app_intro,
    render_data_input_section,
    render_data_source_notice,
    render_sidebar_intro,
)


class FakeSidebar:
    def __init__(self):
        self.headers = []
        self.file_uploaders = []
        self.uploaded_file = None

    def header(self, text):
        self.headers.append(text)

    def file_uploader(self, label, type):
        self.file_uploaders.append({"label": label, "type": type})
        return self.uploaded_file


class FakeStreamlit:
    def __init__(self):
        self.page_config = None
        self.titles = []
        self.captions = []
        self.info_messages = []
        self.sidebar = FakeSidebar()

    def set_page_config(self, **kwargs):
        self.page_config = kwargs

    def title(self, text):
        self.titles.append(text)

    def caption(self, text):
        self.captions.append(text)

    def info(self, text):
        self.info_messages.append(text)


def test_streamlit_layout_module_imports_safely():
    assert callable(configure_page)
    assert callable(render_app_intro)
    assert callable(render_data_input_section)
    assert callable(render_data_source_notice)
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


def test_render_data_input_section_preserves_upload_widget():
    fake_st = FakeStreamlit()
    fake_st.sidebar.uploaded_file = object()

    uploaded_file = render_data_input_section(fake_st)

    assert uploaded_file is fake_st.sidebar.uploaded_file
    assert fake_st.sidebar.headers == ["Input"]
    assert fake_st.sidebar.file_uploaders == [
        {"label": "Upload a CSV or Excel file", "type": ["csv", "xlsx"]}
    ]


def test_render_data_source_notice_preserves_message():
    fake_st = FakeStreamlit()

    render_data_source_notice(fake_st, "Sample data")
    render_data_source_notice(fake_st, "Uploaded file")

    assert fake_st.info_messages == [
        "Using: Sample data",
        "Using: Uploaded file",
    ]
