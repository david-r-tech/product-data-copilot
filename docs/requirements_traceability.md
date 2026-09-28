# Requirements and verification — 28 September 2026

This records the current decisions for the **local** Product Data Copilot MVP. Sample data is fictional. The app is a review aid, not a publication or compliance authority.

| ID | Acceptance example | Decision / implementation | Evidence |
| --- | --- | --- | --- |
| R1 | CSV SKU `000123` remains `000123`; empty files or duplicate SKUs produce a visible error. | Validate input before analysis and retain imported cells as text in [product_input.py](../src/product_data_copilot/data/product_input.py). | [Import tests](../tests/test_product_input.py), [workflow tests](../tests/test_app_workflows.py). |
| R2 | An invalid EAN or missing description produces a field-specific issue. | Deterministic rules in [validators.py](../src/product_data_copilot/rules/validators.py); one correction list in **Daten prüfen** joins each finding with a recommended next step. | [Validator tests](../tests/test_validators.py) and browser data-check view. Rules are heuristics. |
| R3 | A high numerical score with a critical issue still reads Critical. | Gate readiness by open issues in [scoring_helpers.py](../src/product_data_copilot/scoring/scoring_helpers.py) and [app.py](../app.py). | [Scoring tests](../tests/test_scoring_helpers.py), [workflow tests](../tests/test_app_workflows.py). |
| R4 | Switching files clears earlier review decisions and generated text. | Bind session data to the loaded dataset in [session_state.py](../src/product_data_copilot/review/session_state.py). | [State tests](../tests/test_session_state.py), [workflow tests](../tests/test_app_workflows.py). |
| R5 | A user can create German text and bullets with a full selected-language translation for one product or the loaded list; translation-only mode accepts a chosen text column. | [Text helpers](../src/product_data_copilot/ai/content_generation.py) and [text UI](../src/product_data_copilot/ui/content_workspace.py). Requests are explicit and one per product. | [Content tests](../tests/test_content_generation.py), [workflow tests](../tests/test_app_workflows.py), [offline provider test](../tests/test_ai_provider_boundary.py). Factual truth needs human review. |
| R6 | A source value `=1+1` remains text in the downloaded workbook; the source file is unchanged. Unapproved text is absent. | Serialize cells safely in [serialization.py](../src/product_data_copilot/export/serialization.py). The approved-only text output has `Texte & Übersetzungen` and `Originaldaten`, each limited to approved SKUs. | [Serialization tests](../tests/test_export_serialization.py), [content workbook tests](../tests/test_content_generation.py). A fictional offline browser download contained only the approved SKU in both sheets; Microsoft Excel visual inspection remains. |
| R7 | The app starts with fictional data and no API key; three workflow tabs render. | Pinned dependencies, sample fallback and Windows launcher in [requirements.txt](../requirements.txt), [app.py](../app.py), and [start_app.bat](../start_app.bat). | Clean virtual environment, dependency check, workflow tests, and browser walkthrough. |
| R8 | After generating a full list, a person can select each draft and approve, reject or withdraw it; only approved articles can be downloaded as texts. | [Text UI](../src/product_data_copilot/ui/content_workspace.py) stores decisions beside drafts in the current session. [Approved-only export](../src/product_data_copilot/ai/content_generation.py) filters text and source rows by reviewed SKU. | [Workflow tests](../tests/test_app_workflows.py) cover article decisions after bulk generation; [content tests](../tests/test_content_generation.py) cover export exclusion. Human factual judgment remains manual. |
| R9 | A dedicated `material`, `color`/`farbe`, or `surface`/`oberfläche` value differs from an explicit value in `attributes`. | [Attribute comparison](../src/product_data_copilot/rules/attribute_consistency.py) adds a warning to the existing correction list with both values and sources. It does not infer facts from descriptions or declare which value is right. | [Attribute tests](../tests/test_attribute_consistency.py) cover mismatches and conservative non-matches; [workflow tests](../tests/test_app_workflows.py) confirm the warning appears in the UI. |

## Decision rules

- SKU is the unique key. Ambiguous files are rejected rather than guessed.
- Component scores prioritize review. Open issues can constrain a Ready label; manual status cannot bypass the gate.
- Creation uses populated product facts and requests a German HTML description, up to five supported bullets, and the complete selected-language translation. Translation-only mode changes existing text without adding new facts.
- AI runs only when clicked. One request is made per processed product. Completed results remain in the session; a click processes at most 100 products so large uploads can continue with another click. No output is automatically approved or published. Text approval is an explicit session-only decision per article and language.
- User-provided spreadsheet text is neutralized for formulas and control characters on export. The uploaded file is never overwritten.
- The base audit runs locally. AI processing sends the selected product context to OpenAI using the user's local key. Users must choose suitable data and review generated claims.
- The 1,000-row upload limit bounds this local MVP. Earlier worst-case measurements are observations, not performance guarantees for AI generation.

## Remaining acceptance checks

1. Approve one text, reject another, then open both workbooks in Microsoft Excel and verify that only approved texts and their matching source rows occur in the text workbook. The revised gate passed an offline browser check with fictional responses; a live-key review remains manual.
2. Spot-check several generated products before making broad quality claims. Live creation was checked in German/English for fictional `APP-001`, and live translation-only in French for a small fictional text; Spanish remains unverified.
3. The implementation is committed and pushed. Confirm that the repository remains private before publication; after publication, verify anonymous access to the intended URL.
4. Confirm that any external product description matches the current README and documented limitations.

Accounts, database persistence, hosting, marketplace integrations, automatic approval, and source write-back are outside the local MVP scope.
