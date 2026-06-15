# Commerce Readiness AI - Product Requirements

## 1. Purpose

Commerce Readiness AI is a local Streamlit MVP that helps e-commerce teams review product data before marketplace or shop publication.

The purpose of this document is to capture the current product requirements in a clear, testable format. It is written for portfolio review, future development planning, and requirements-engineering traceability.

## 2. Business Goal

The MVP should demonstrate how a product-data audit workflow can turn a CSV/XLSX product file into:

- A product data preview
- Detected data quality issues
- Explainable readiness scores
- Review tasks for operational follow-up
- Optional human-reviewed AI draft suggestions
- CSV and Excel exports for business users

## 3. Target Users

- Product Data Managers
- Marketplace Managers
- E-commerce Operations Teams
- Category Managers
- Content and Translation Teams

## 4. User Problems

Users need to answer these questions quickly:

- Which products have missing or weak product data?
- Which issues are critical before marketplace review?
- Which products need translation or compliance review?
- Which product listings are closest to being ready?
- What tasks should a team work on next?
- What summary can be shared with management or stakeholders?

## 5. MVP Scope

The current MVP includes:

- Local Streamlit app
- Sample product dataset
- CSV and Excel upload
- Product data preview
- Rule-based product data checks
- Dashboard metrics
- Multiple readiness scores
- Product review statuses
- Review task workflow
- Manual review status override in session state
- CSV exports
- Excel Management Export
- Optional AI Suggestions for one selected product
- Documentation for demo, testing, screenshots, and portfolio use

## 6. Functional Requirements

| ID | Requirement | Current Status | Verification |
| --- | --- | --- | --- |
| FR-001 | The app shall load the built-in sample product dataset when no file is uploaded. | Implemented | Start app without upload and confirm "Using: Sample data". |
| FR-002 | The app shall support CSV upload. | Implemented | Upload a CSV file and confirm product data changes. |
| FR-003 | The app shall support XLSX upload. | Implemented | Upload an Excel file and confirm product data changes. |
| FR-004 | The app shall display product data in a table. | Implemented | Open Product Data tab. |
| FR-005 | The app shall detect product data quality issues. | Implemented | Open Issues tab and review issue rows. |
| FR-006 | The app shall classify issues by severity. | Implemented | Check Critical, Warning, and Info values in Issues. |
| FR-007 | The app shall calculate multiple readiness scores per product. | Implemented | Open Scores tab and check score columns. |
| FR-008 | The app shall create review tasks from detected issues. | Implemented | Open Review Tasks tab. |
| FR-009 | The app shall allow filtering review tasks. | Implemented | Use priority, task type, and review status filters. |
| FR-010 | The app shall support manual review status overrides in the current session. | Implemented | Apply override and confirm status changes. |
| FR-011 | The app shall export scores, issues, and tasks as CSV. | Implemented | Use CSV download buttons. |
| FR-012 | The app shall create a Management Excel Export. | Implemented | Download workbook from Management Export tab. |
| FR-013 | The app shall support optional AI suggestions when an API key is configured. | Implemented | Generate one suggestion with local API key. |
| FR-014 | The app shall not crash when no OpenAI API key is configured. | Implemented | Open AI Suggestions without `.env` key. |
| FR-015 | The app shall not automatically write AI suggestions back to product data. | Implemented | Confirm suggestions are displayed/exported only. |

## 7. Non-Functional Requirements

| ID | Requirement | Current Status | Verification |
| --- | --- | --- | --- |
| NFR-001 | The app should run locally with a simple command. | Implemented | `python -m streamlit run app.py` |
| NFR-002 | The project should be understandable for GitHub and portfolio reviewers. | Implemented | Review README and docs. |
| NFR-003 | The app should work without secrets committed to the repository. | Implemented | Check `.env` is ignored and `.env.example` uses placeholders. |
| NFR-004 | The app should remain usable without OpenAI access. | Implemented | Open AI Suggestions without API key. |
| NFR-005 | The app should keep generated exports out of Git. | Implemented | Check `.gitignore`. |
| NFR-006 | The code should stay beginner-friendly and avoid unnecessary architecture. | Implemented | App remains in a simple Streamlit MVP structure. |

## 8. Business Rules

- Products with missing core data should receive issues and lower readiness scores.
- Safety-relevant categories should require warning-note review.
- AI Suggestions are draft recommendations only.
- Human review is required before using generated AI content.
- Manual review overrides are session-only in the current MVP.
- Management exports should include all main audit outputs in one workbook.

## 9. Out of Scope

The current MVP does not include:

- Production deployment
- Login or user accounts
- Multi-user roles
- Database persistence
- Marketplace-specific rule presets
- Shopware, Shopify, Plentymarkets, or marketplace API integrations
- Variant parent-child logic
- Bulk AI generation
- Automatic acceptance of AI suggestions
- Automatic write-back to product source data
- Legal compliance guarantees

## 10. Acceptance Criteria

The MVP is considered GitHub/portfolio-ready when:

- The app starts locally.
- Sample data loads without upload.
- CSV and XLSX upload work.
- Dashboard, Product Data, Scores, Issues, Review Tasks, Management Export, and AI Suggestions tabs render.
- Product data issues are detected from the sample dataset.
- Readiness scores are visible and explainable.
- Review tasks can be filtered.
- Manual review status override works in the session.
- CSV downloads work.
- Management Excel Export downloads successfully.
- AI Suggestions tab works without an API key by showing the fallback message.
- No secrets are stored in the repository.
- README and supporting docs explain setup, usage, scope, limits, and demo flow.

## 11. Risks and Limitations

- Manual review overrides are not persisted after the Streamlit session ends.
- Rule-based checks are useful but not marketplace-certified validations.
- AI Suggestions depend on local API-key configuration and model availability.
- AI Suggestions are not legal or compliance advice.
- The app is designed for demo-sized datasets, not large production catalogs.
- The project is a local MVP, not a deployed SaaS product.

## 12. Next Recommended Requirement Block

Portfolio Case Study v1 Finalization:

- Add final screenshots
- Add concise project narrative
- Connect requirements, implementation decisions, and business value
- Prepare the project for sharing in applications or interviews
