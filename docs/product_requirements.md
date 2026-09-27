# Product Data Copilot — MVP requirements

**Version:** local portfolio MVP, 27 September 2026. This document describes the current product contract. [Requirements traceability](requirements_traceability.md) links each requirement to implementation and verification evidence; the [README](../README.md) explains installation and use.

## Problem and decision

Product-data teams receive files from suppliers or internal systems before listings are published. They need to know which records require work, why, and what can be handed to the next reviewer. Spreadsheets alone provide rows but little prioritization or decision history. The MVP converts one local product file into a repeatable **upload → check → review → optional improvement → handoff** workflow.

The primary user is a product-data or e-commerce operations specialist. A manager consumes the summary workbook; a content or translation reviewer consumes issue tasks and proposed improvements. A reviewer retains responsibility for factual correctness and any publication decision.

## Scope and assumptions

- One user, one local Streamlit session, no database or hosted service.
- One CSV file or the first sheet of one XLSX file at a time. The SKU is a unique, non-empty product identifier. Invalid identity blocks analysis because incorrect issue or approval assignment is unacceptable.
- Up to 10 MB, 1,000 product rows and 100 columns. These bounds keep the local MVP responsive and limit untrusted workbook input.
- The base audit needs no external service. Optional AI generation sends the selected product and review context to OpenAI only on a user action.
- Rule results are generic quality signals. They are not retailer-specific validation or legal/compliance certification.

## Functional requirements

| ID | Requirement | Acceptance criterion |
| --- | --- | --- |
| R1 | Import bounded CSV/XLSX input without losing product identity. | CSV `000123` remains `000123`; empty files, missing required columns, missing/duplicate SKUs and files beyond stated limits produce a visible error and no analysis. |
| R2 | Detect actionable product-data issues. | Each detected issue names its SKU, field, issue type, severity, explanation and recommended action. Critical issues appear first in the Issues view and task list. |
| R3 | Explain readiness without hiding open findings. | Five component scores and a weighted overall score are visible. A critical issue forces Critical; another open issue prevents Ready even when the numeric score is high. |
| R4 | Scope decisions and drafts to the current evidence. | Loading a different file clears dataset-dependent manual and AI state. Regenerating V2 suggestions starts with no inherited approval. |
| R5 | Keep AI suggestions optional and reviewable. | With no API key, the core app works and generation is disabled clearly. V1 content is labeled an unreviewed draft. V2 proposals with mismatched SKU, target, old value or source are blocked; only a human decision can place a valid row in Approved Improvements. |
| R6 | Export auditable handoff artifacts without source mutation. | CSV and Excel downloads contain issues/tasks/scores or reviewed V2 groups as appropriate, include the loaded source snapshot, and never overwrite the input file. User-provided formula-like text does not become an executable spreadsheet formula. |
| R7 | Let a reviewer reproduce the workflow locally. | Dependencies install in an isolated environment; the app launches with fictional sample data, and all seven tabs work without paid API access. |

## Quality constraints

- **Privacy:** `.env` and app secrets remain outside Git. The interface explains when an AI click will send selected product context to OpenAI. No AI call is needed for audit or export.
- **Failure behavior:** malformed input shows an actionable error and does not leave stale approvals or a partial export behind. AI call failure does not expose raw provider error text to the user or retain previous V2 approvals.
- **Testability:** import, rules, scoring, review lifetime, AI provenance and serialization are import-safe helpers with automated regression tests. A real browser walkthrough and manual Excel check complement these tests.
- **Capacity:** the documented 1,000-row bound has been exercised with 9,000 generated issues in a local AppTest. This establishes a bounded MVP use case, not a production throughput guarantee.

## Deliberate exclusions

The MVP has no login, role system, shared review, persistence across sessions, marketplace presets/integrations, automatic bulk AI generation, automatic suggestion approval, source write-back, hosting, or compliance guarantee. These would need separate user evidence, requirements and acceptance tests; they are not implied by a readiness score.

## Release acceptance

The code reference is ready when the automated suite and dependency check pass, the fictional-data audit and management download work in the browser, the management workbook is visually inspected in Excel, public-facing text matches the actual product, and the GitHub link is accessible to the intended reviewers. The V2 improvement workbook is covered by offline tests; its visual Excel check is optional after a reviewer generates suggestions with their own key. Live AI quality must be tested separately before it is claimed as verified. The [release check](final_portfolio_release_checklist_v1.md) records the remaining manual steps.
