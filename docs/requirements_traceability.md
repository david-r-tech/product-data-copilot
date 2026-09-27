# Requirements and verification — 27 September 2026

This is the current decision and acceptance record for the **local** Product Data Copilot MVP. It separates implemented behavior from claims that require a human check. The sample data is fictional; the app is a review aid, not a publication or compliance authority.

| ID | User need / acceptance criterion | Implemented in | Verification |
| --- | --- | --- | --- |
| R1 | A user can load a product file without silently losing identifiers or mixing products. Invalid, empty, oversized, duplicate-SKU and missing-SKU inputs are rejected. | `data/product_input.py`, `app.py` | Automated CSV/XLSX boundary and UI tests; sample file in browser. |
| R2 | A user can see which product data problems exist and why they matter. | `rules/validators.py`, `app.py` | Validator tests and browser Issues view. Rules are heuristics, not a retailer specification. |
| R3 | A user can prioritize products without a critical/open issue being hidden by a high average score. | `scoring/scoring_helpers.py`, `review/review_helpers.py`, `app.py` | Scoring/review tests and browser Dashboard/Review Tasks views. |
| R4 | A change of input file or fresh AI response must not inherit decisions or suggestions from a previous context. | `review/session_state.py`, `app.py` | State transition and Streamlit AppTest regressions. State stays in the current session only. |
| R5 | AI content is optional, scoped to one product, traceable to available source fields, and requires human judgment. | `ai/source_validation.py`, `ai/suggestion_parser.py`, `app.py` | Parser/source-validation/AppTest tests. Factual correctness of a live response still requires manual review. |
| R6 | Reviewers can export without mutating the source file or executing spreadsheet formulas from source/AI text. | `export/serialization.py`, `export/export_helpers.py`, `app.py` | Workbook round-trip and CSV serialization tests. Visual layout in Microsoft Excel remains a manual check. |
| R7 | A reviewer can start the app locally without paid or hosted infrastructure. | `requirements.txt`, `start_app.bat`, `app.py` | Clean virtual environment, dependency check, app launch and sample-data browser walkthrough. |

## Decision rules

- Identity: SKU is the unique product key for this MVP. Ambiguous files are rejected instead of guessing row ownership.
- Readiness: component scores are numerical indicators. An open critical issue forces Critical; another open issue prevents Ready. The review status cannot manually bypass this.
- AI: v1 output is an unreviewed draft. V2 output is source-checked and reviewable. Only a human decision can put a V2 suggestion in the Approved Improvements export group. Neither path writes back to the product file.
- Export: source snapshots are included for comparison. Spreadsheet formulas and unsupported control characters in user-provided text are neutralized during serialization, leaving the in-memory source data unchanged.
- Privacy: the base workflow runs locally. Clicking an AI generation control sends the selected product context to OpenAI. A user must choose suitable data and verify any generated claims.

## Remaining acceptance checks and deliberate deferrals

1. **Before sharing the application:** the authenticated Git remote is reachable and the latest commit was pushed, but the repository page returned 404 in a signed-out browser on 27 September 2026. The owner chose to keep it private and grant access to named reviewers. Do not present its URL as a freely accessible link; an invited reviewer must accept access and sign in to GitHub.
2. **Manual product check:** open the running app with the fictional sample file, navigate every tab, download both workbooks, and inspect the files in Microsoft Excel. Automated tests verify their data and cell types, not Excel's visual presentation.
3. **Optional live AI check:** if an API key is available and the data may be sent to OpenAI, generate one V2 suggestion, inspect its sources and wording, approve only after factual review, regenerate, and verify that approval resets. The test suite uses controlled responses and does not establish live model quality.
4. **External publication check:** any CV, portfolio page, or social post linking this project must be checked against this README. Those links have not yet been supplied.

Database persistence, accounts, hosting, marketplace integrations, automatic bulk AI, automatic approval and write-back are outside the local MVP scope. They are not blockers for a code-and-product portfolio reference when described honestly.
