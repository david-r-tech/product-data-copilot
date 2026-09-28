# Product Data Copilot — MVP requirements

**Version:** local portfolio MVP, 28 September 2026. This is the current product contract. [Requirements traceability](requirements_traceability.md) links requirements to implementation and evidence; the [README](../README.md) explains installation and use.

## Problem and users

Product-data teams receive incomplete supplier spreadsheets. They need to find data gaps, prioritize correction work, and prepare fact-based product copy and translations for human review. A product-data or e-commerce specialist operates the app; a manager reads the audit export; a content reviewer checks generated drafts. Publication and factual responsibility remain with people.

The local workflow is **upload → check data → create or translate text → review → export**.

## Scope and assumptions

- One user and one local Streamlit session; no database, hosted service, or automatic publication.
- One UTF-8 CSV or the first worksheet of one XLSX file at a time. `sku` and `product_name` are required; the SKU must be unique and non-empty.
- Up to 10 MB, 1,000 product rows, and 100 columns. Additional populated supplier columns can inform text generation even if the audit does not assign them a specific rule.
- The base audit and management export run locally without an API key. Text generation sends relevant product facts or selected source text to OpenAI only after a user clicks the button.
- Rules are generic quality signals, not retailer-specific validation or legal/compliance certification.

## Functional requirements

| ID | Requirement | Acceptance criterion |
| --- | --- | --- |
| R1 | Import bounded CSV/XLSX without losing product identity. | CSV SKU `000123` remains `000123`; missing/duplicate SKUs, missing required columns, empty or oversized files show an error and stop analysis. |
| R2 | Detect actionable data-quality issues. | Each finding identifies SKU, field, type, severity, explanation, and recommended action; critical issues appear first. |
| R3 | Explain findings without hiding open issues. | The main view shows affected products and an actionable correction list; component scores remain in expandable technical details. A critical issue forces Critical; another open issue prevents Ready. |
| R4 | Scope state to the loaded file. | Switching to another file clears review decisions and generated text, including when the SKU is reused. |
| R5 | Create or translate product text for one product or the loaded table. | With a key, creation requests a German HTML description and up to five fact-based German bullets, then the complete text and bullet translation in English, French, or Spanish. Translation-only mode uses a chosen existing text column and optional bullet column. Without a key, audit and export still work and the text tab explains what is needed. |
| R6 | Export without modifying the source. | The management workbook has five audit sheets. The text workbook has only `Texte & Übersetzungen` and `Originaldaten`; both sheets contain only articles whose generated texts a person approved. No text workbook is available without an approval. Downloaded source cells remain unchanged and formula-like text is inert. |
| R7 | Reproduce the workflow locally. | Dependencies install in an isolated environment, fictional sample data loads automatically, and the three workflow tabs render without paid API access. |
| R8 | Review generated texts individually, including after whole-list generation. | Each draft is shown with its source fields, German and translated text, bullets and local review notes. A reviewer can approve, reject or withdraw a decision per article; pending and rejected texts never enter the text workbook. |
| R9 | Surface explicit supplier-attribute discrepancies for review. | When dedicated material, colour, or surface columns differ from explicitly named values in `attributes`, one warning per affected attribute shows both values and their source columns. Missing values and free-form prose are not guessed. |

## Quality constraints

- **Human review:** AI output is a draft. Responses must match the requested SKU and parse as JSON; HTML is restricted to safe tags. These checks do not prove claims or translations true. Only an explicit human decision enables a text for export.
- **Cost and control:** A user explicitly starts generation. One product is processed per logical generation request; up to 100 products run per click and later clicks continue unfinished rows. Provider retries may occur once. Completed drafts remain in the current session to avoid repeat generation.
- **Failure behavior:** Bad input shows an actionable error. Failed product generation remains visible and can be retried without discarding other completed rows. Provider details and credentials are not exposed in the interface.
- **Security and privacy:** `.env` and keys remain outside Git. User-provided data is sent to OpenAI only on a generation click. Spreadsheet output neutralizes formula-like text.
- **Testability:** Import, rules, scoring, session state, prompting, response normalization, and export serialization have automated tests. Browser and Microsoft Excel checks complement them.
- **Capacity:** The 1,000-row file limit is a bound for this local MVP, not a throughput guarantee for AI generation.

## Deliberate exclusions and acceptance

There are no accounts, shared review, persistence across sessions, marketplace presets or integrations, automatic approval, source write-back, hosting, or compliance guarantees. The explicit-attribute comparison is a conservative rule; semantic consistency of arbitrary free-form supplier text remains a separate future product decision.

The code reference is ready to share after automated checks pass, the final UI and both downloads are inspected, public-facing documentation matches the app, and the intended GitHub URL is accessible to reviewers. A live in-app creation and a separate translation-only call have passed for small fictional examples; whole-file factual quality is not established. The [release check](final_portfolio_release_checklist_v1.md) records the remaining manual steps.
