# Project status — 27 September 2026

Product Data Copilot is a working local Streamlit MVP. It loads fictional sample data or validated CSV/XLSX product files, calculates issues and readiness, creates review tasks, supports optional human-reviewed AI suggestions, and exports management/improvement workbooks without modifying source data. The application no longer contains the old demo-fixture loader.

The latest local automated run passed **188 tests** in the tested Python 3.14.4 environment, including offline request/response checks through the installed OpenAI SDK with a fake key. The normal sample-data flow rendered in a browser. The exact code and decisions are documented in [requirements_traceability.md](requirements_traceability.md) and the public-facing workflow in the [README](../README.md).

## Before using the repository as a job-application reference

1. Finish a manual visual check of the management workbook in Microsoft Excel. A live AI call is not required for this release candidate; the reviewer may later use their own key. Live model output and factual quality remain unverified.
2. The owner now intends to publish the repository for job applications. The latest code has been pushed, but the page returned 404 in a signed-out browser before the visibility change. Verify anonymous access before adding the URL to an application.
3. Check any CV, portfolio, or social description against the current README. Links to those publications have not yet been supplied.

## Intentional limits

Review decisions last only for the Streamlit session. There are no accounts, database, hosted service, external commerce integrations, bulk AI generation, automatic approval or source write-back. Readiness scores and AI suggestions are aids to human judgment, not retailer acceptance or compliance guarantees.

The historical work record remains in [commerce_readiness_ai_project_log.md](commerce_readiness_ai_project_log.md). Older plans and demo checklists describe earlier development stages; they are not current feature claims.
