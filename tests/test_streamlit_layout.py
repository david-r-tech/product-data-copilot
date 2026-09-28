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
    render_dataset_summary,
    render_issues_summary,
    render_no_data_quality_issues_notice,
    render_no_matching_issues_notice,
    render_no_matching_review_tasks_notice,
    render_no_review_tasks_notice,
    render_review_tasks_intro,
    render_review_tasks_summary,
    render_sidebar_intro,
)


class FakeSidebar:
    def __init__(self):
        self.headers = []
        self.file_uploaders = []
        self.uploaded_file = None

    def header(self, text):
        self.headers.append(text)

    def file_uploader(self, label, type, max_upload_size):
        self.file_uploaders.append({"label": label, "type": type, "max_upload_size": max_upload_size})
        return self.uploaded_file


class FakeStreamlit:
    def __init__(self):
        self.page_config = None
        self.titles = []
        self.captions = []
        self.info_messages = []
        self.success_messages = []
        self.sidebar = FakeSidebar()

    def set_page_config(self, **kwargs):
        self.page_config = kwargs

    def title(self, text):
        self.titles.append(text)

    def caption(self, text):
        self.captions.append(text)

    def info(self, text):
        self.info_messages.append(text)

    def success(self, text):
        self.success_messages.append(text)


def test_streamlit_layout_module_imports_safely():
    assert callable(configure_page)
    assert callable(render_app_intro)
    assert callable(render_data_input_section)
    assert callable(render_data_source_notice)
    assert callable(render_dataset_summary)
    assert callable(render_issues_summary)
    assert callable(render_no_data_quality_issues_notice)
    assert callable(render_no_matching_issues_notice)
    assert callable(render_no_matching_review_tasks_notice)
    assert callable(render_no_review_tasks_notice)
    assert callable(render_review_tasks_intro)
    assert callable(render_review_tasks_summary)
    assert callable(render_sidebar_intro)


def test_configure_page_sets_expected_streamlit_page_config():
    fake_st = FakeStreamlit()

    configure_page(fake_st)

    assert fake_st.page_config == {
        "page_title": "Product Data Copilot",
        "layout": "wide",
    }


def test_render_app_intro_preserves_title_and_caption():
    fake_st = FakeStreamlit()

    render_app_intro(fake_st)

    assert fake_st.titles == ["Product Data Copilot"]
    assert fake_st.captions == [
        "CSV-based product data quality checks for e-commerce readiness."
    ]


def test_render_sidebar_intro_preserves_input_header():
    fake_st = FakeStreamlit()

    render_sidebar_intro(fake_st)

    assert fake_st.sidebar.headers == ["Eingabe"]


def test_render_data_input_section_preserves_upload_widget():
    fake_st = FakeStreamlit()
    fake_st.sidebar.uploaded_file = object()

    uploaded_file = render_data_input_section(fake_st)

    assert uploaded_file is fake_st.sidebar.uploaded_file
    assert fake_st.sidebar.headers == ["Eingabe"]
    assert fake_st.sidebar.file_uploaders == [
        {"label": "CSV- oder Excel-Datei hochladen", "type": ["csv", "xlsx"], "max_upload_size": 10}
    ]


def test_render_data_source_notice_preserves_message():
    fake_st = FakeStreamlit()

    render_data_source_notice(fake_st, "Sample data")
    render_data_source_notice(fake_st, "Uploaded file")

    assert fake_st.info_messages == [
        "Datenquelle: Sample data",
        "Datenquelle: Hochgeladene Datei",
    ]


def test_render_dataset_summary_preserves_caption():
    fake_st = FakeStreamlit()

    render_dataset_summary(fake_st, 25, 14)

    assert fake_st.captions == ["Artikel: 25 | Spalten: 14"]


def test_render_issues_summary_preserves_caption():
    fake_st = FakeStreamlit()

    render_issues_summary(fake_st, 12, 5)

    assert fake_st.captions == ["Total issues: 12 | Displayed issues: 5"]


def test_issue_empty_state_notices_preserve_messages():
    fake_st = FakeStreamlit()

    render_no_matching_issues_notice(fake_st)
    render_no_data_quality_issues_notice(fake_st)

    assert fake_st.info_messages == ["No issues match the selected severity filter."]
    assert fake_st.success_messages == ["No data quality issues found."]


def test_render_review_tasks_intro_and_summary_preserve_captions():
    fake_st = FakeStreamlit()

    render_review_tasks_intro(fake_st)
    render_review_tasks_summary(fake_st, 20, 7)

    assert fake_st.captions == [
        "Review workflow overview, filters, manual status overrides, and task export.",
        "Total review tasks: 20 | Displayed tasks: 7",
    ]


def test_review_task_empty_state_notices_preserve_messages():
    fake_st = FakeStreamlit()

    render_no_matching_review_tasks_notice(fake_st)
    render_no_review_tasks_notice(fake_st)

    assert fake_st.info_messages == ["No review tasks match the selected filters."]
    assert fake_st.success_messages == ["No review tasks needed."]
