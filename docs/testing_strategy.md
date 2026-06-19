# Product Data Copilot - Testing Strategy v1

## Purpose

This document explains why direct unit tests against the current `app.py` are not yet safe, and what should be extracted first to enable a clean pytest safety net.

The goal is to avoid brittle tests that import the full Streamlit app and accidentally execute UI code.

## Current Testability Problem

The current `app.py` is a working MVP but still behaves as a monolithic Streamlit script.

Importing `app.py` directly would execute top-level Streamlit code, including:

- `st.set_page_config(...)`
- `.env` loading
- sample data loading
- issue detection
- score calculation
- tab creation
- UI rendering
- session-state access

Because of this, direct imports such as:

```python
from app import is_valid_ean
```

are not a clean unit-testing strategy yet. They would import more than the function under test and may trigger Streamlit runtime behavior.

## Decision for This Block

Do not add brittle tests that import the full app.

Instead, document the first safe extraction targets and add pytest only when functions can be imported without executing the Streamlit UI.

## First Functions to Extract for Testing

These functions are the safest first candidates because they are small and mostly pure:

- `is_blank`
- `normalize_text`
- `is_valid_ean`
- `is_valid_price`
- `is_suspicious_image_url`
- `is_generic_product_name`
- `has_useful_attributes`
- `is_safety_relevant_category`
- `get_readiness_status`
- `score_from_checks`
- `get_task_priority`
- `get_task_type`

Recommended future location:

```text
src/product_data_copilot/rules/validators.py
src/product_data_copilot/scoring/scoring_service.py
src/product_data_copilot/review/review_service.py
```

## First Pytest Test Candidates

After extraction, add tests such as:

```text
tests/test_validators.py
tests/test_scoring.py
tests/test_review_mapping.py
```

Recommended initial assertions:

- valid EAN returns `True`
- invalid EAN returns `False`
- positive price returns `True`
- zero price returns `False`
- relative image path is suspicious
- generic product title is detected
- score 90 maps to `Ready`
- score 70 maps to `Needs Review`
- score 40 maps to `Critical`
- Critical severity maps to High priority
- Warning severity maps to Medium priority
- Info severity maps to Low priority

## Later Test Areas

After the first pure functions are extracted:

- rule engine issue output
- score calculation for sample products
- review task generation
- Excel export sheet names
- AI prompt safety language
- missing API key behavior

## Pytest Tooling Plan

Add `pytest` to `requirements.txt` only when the first real tests are added.

Recommended command after tests exist:

```bash
python -m pytest
```

## Non-Goals

This strategy does not add:

- test framework configuration
- new tests
- refactored code
- new source package
- app behavior changes
- UI changes

## Next Recommended Step

Extract only the smallest pure validation helpers into an import-safe module, then add `pytest` and the first validator tests.
