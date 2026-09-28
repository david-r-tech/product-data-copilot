# Product Data Copilot — Product Case Study

## Problem and audience

Product-data teams receive incomplete supplier spreadsheets. They need to find gaps, prioritize corrections, and turn available facts into product copy without confusing a plausible AI draft with a verified fact. Product Data Copilot is a local Streamlit MVP for product-data and e-commerce teams.

## Workflow and product decisions

1. **Load:** Use fictional sample data or upload CSV/XLSX. Unique, non-empty SKUs identify each product; invalid files are rejected before analysis. The audit recognizes standard fields, while the text generator can also use populated supplier columns such as material, colour, and surface.
2. **Check:** Deterministic rules produce issues with field, severity, reason, and recommended action. Explicit material, colour, and surface values are compared across dedicated fields and structured `attributes`; discrepancies are flagged for a person to resolve. One correction list shows what needs attention first; technical scores are available in an expandable detail view. A critical issue forces Critical; any other open issue prevents a Ready label regardless of the number.
3. **Review:** Findings feed an optional session-only product status, a correction-list CSV, and a five-sheet management workbook. Source corrections require changing and re-uploading the original file.
4. **Create or translate:** A user chooses the whole table or one product, plus English, French, or Spanish. Creation requests German HTML product copy and up to five German bullets, then translates the complete output. Translation-only mode uses an existing text column and optional bullet column. Every processed product starts one paid request, with a visible progress/status list and retry for failures. The user starts the run explicitly.
5. **Review:** A person selects each generated article, compares German and translated text and bullets with the visible source facts, then approves, rejects, or withdraws the decision. Whole-table generation does not bulk-approve results.
6. **Hand off:** A two-sheet text workbook contains only approved texts and their matching source rows. Without an approval, no text workbook is offered. Decisions exist only in the current session; there is no automatic approval, publication, or source-file update.

## Requirements-engineering rationale

The central requirements and their evidence are in [requirements_traceability.md](requirements_traceability.md); the [Product-Owner artifacts](product_owner_artifacts.md) explain vision, priorities, stakeholders, and planned measures. Unambiguous SKU identity protects the link between source and output. The three-tab interface keeps concrete corrections ahead of abstract scores. Creation and translation are distinct user tasks, and a full-file option matches the supplier-spreadsheet workflow. The text workbook has only two sheets so a reviewer can find approved content and its source quickly.

AI output is a draft. Matching the response SKU, requesting JSON, restricting HTML, and warning about bullet-count gaps prevent some mechanical errors, but cannot establish that a product claim or translation is true. Human review remains necessary. Exports are generated in memory and written with spreadsheet-safe cell serialization.

## Implementation and evidence

`app.py` owns the Streamlit flow. Modules under `src/product_data_copilot/` handle loading, rules, scoring, text prompting/normalization, session state, and export serialization. The local run on 28 September 2026 passed **196 automated tests** in Python 3.14.4. Tests cover file identity and validation, readiness gates, generation for one product and an entire list, individual approval, approved-only export, translation inputs, HTML restrictions, and an offline OpenAI SDK request. During final acceptance, exactly one paid creation request for fictional `APP-001` returned German HTML and five German bullets plus English HTML and five English bullets. Every generated factual claim was manually compared with the source data, and no unsupported factual claim was found in this one controlled test. This single example does not prove reliability across products, languages, models, or future outputs. A whole-file live run, broader language quality, and visual inspection of both generated workbooks in Microsoft Excel remain outside this evidence.

## Deliberate limits

This MVP has no persistence across sessions, multi-user review, marketplace-specific rules, integration, automatic write-back, or compliance guarantee. The generic data checks are separate from the new text workflow; they do not verify semantic consistency of all supplier attributes. The next product decision should follow real-user feedback, not assumed enterprise requirements.

The [README](../README.md) contains setup, input format, and reviewer-facing usage instructions.
