# Requirements and verification — 27 September 2026

This is the current decision and acceptance record for the **local** Product Data Copilot MVP. It separates implemented behavior from claims that require a human check. The sample data is fictional; the app is a review aid, not a publication or compliance authority.

| ID | Acceptance example | Decision / implementation | Evidence |
| --- | --- | --- | --- |
| R1 | CSV SKU `000123` remains `000123`; an empty file or duplicate SKU produces a visible error and no analysis. | Validate input before analysis and retain all imported cells as text in [product_input.py](../src/product_data_copilot/data/product_input.py). | [Import tests](../tests/test_product_input.py), [app workflow tests](../tests/test_app_workflows.py). |
| R2 | An invalid EAN or missing description creates a field-specific issue with severity and recommended action. | Deterministic rules in [validators.py](../src/product_data_copilot/rules/validators.py); critical issues appear first in the UI and export. | [Validator tests](../tests/test_validators.py), browser Issues view and screenshot. Rules are heuristics, not a retailer specification. |
| R3 | A product with a numeric score above 85 and a critical issue still reads Critical and cannot be marked Ready for Export. | Gate numeric indicators by open issues in [scoring_helpers.py](../src/product_data_copilot/scoring/scoring_helpers.py) and [app.py](../app.py). | [Scoring tests](../tests/test_scoring_helpers.py), [app workflow tests](../tests/test_app_workflows.py). |
| R4 | File A → file B with the same SKU clears previous review decisions; generating a fresh V2 answer resets approvals. | Bind decisions to input and response lifetime in [session_state.py](../src/product_data_copilot/review/session_state.py). | [State tests](../tests/test_session_state.py), [app workflow tests](../tests/test_app_workflows.py). |
| R5 | A V2 proposal with a different SKU, nonexistent source field or wrong current value cannot be approved. | Check model output against the selected source product in [source_validation.py](../src/product_data_copilot/ai/source_validation.py). | [Source-validation tests](../tests/test_source_validation.py), controlled V2 app tests. Factual truth still needs human review. |
| R6 | A source value `=1+1` remains text in the downloaded workbook; the original file is unchanged. | Serialize source and suggestion text safely in [serialization.py](../src/product_data_copilot/export/serialization.py). | [Serialization tests](../tests/test_export_serialization.py); an actual management download contained 25 source rows and zero formula cells. Excel visual layout remains a manual check. |
| R7 | The app starts locally with fictional sample data and no API key; all seven tabs render. | Pinned dependencies, sample fallback and Windows launcher in [requirements.txt](../requirements.txt), [app.py](../app.py) and [start_app.bat](../start_app.bat). | Clean virtual environment, dependency check, app workflow test and browser walkthrough. |

## Decision rules

- Identity: SKU is the unique product key for this MVP. Ambiguous files are rejected instead of guessing row ownership.
- Readiness: component scores are numerical indicators. An open critical issue forces Critical; another open issue prevents Ready. The review status cannot manually bypass this.
- AI: v1 output is an unreviewed draft. V2 output is source-checked and reviewable. Only a human decision can put a V2 suggestion in the Approved Improvements export group. Neither path writes back to the product file.
- Export: source snapshots are included for comparison. Spreadsheet formulas and unsupported control characters in user-provided text are neutralized during serialization, leaving the in-memory source data unchanged.
- Privacy: the base workflow runs locally. Clicking an AI generation control sends the selected product context to OpenAI. A user must choose suitable data and verify any generated claims.
- Capacity: the 1,000-row upload limit is a deliberate bound. A worst-case local AppTest with 1,000 fictional products and 9,000 issues rendered all seven tabs without errors in about 12 seconds on the development machine; this is an observation, not a performance guarantee.

## Remaining acceptance checks and deliberate deferrals

1. **Before sharing the application:** the authenticated Git remote is reachable and the latest code was pushed, but the repository page returned 404 in a signed-out browser on 27 September 2026. The owner now intends to make it public. Change the GitHub visibility setting and verify anonymous access before presenting its URL as a freely accessible link.
2. **Manual product check:** open the running app with the fictional sample file, navigate every tab, download both workbooks, and inspect the files in Microsoft Excel. Automated tests verify their data and cell types, not Excel's visual presentation.
3. **Optional live AI check:** if an API key is available and the data may be sent to OpenAI, generate one V2 suggestion, inspect its sources and wording, approve only after factual review, regenerate, and verify that approval resets. The test suite uses controlled responses and does not establish live model quality.
4. **External publication check:** any CV, portfolio page, or social post linking this project must be checked against this README. Those links have not yet been supplied.

Database persistence, accounts, hosting, marketplace integrations, automatic bulk AI, automatic approval and write-back are outside the local MVP scope. They are not blockers for a code-and-product portfolio reference when described honestly.
