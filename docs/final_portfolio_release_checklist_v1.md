# Portfolio release check — 27 September 2026

Use this checklist just before including Product Data Copilot in an application. The current technical and product contract is in the [README](../README.md) and [requirements traceability](requirements_traceability.md).

## Already verified locally

- [x] App starts with fictional sample data and the normal Dashboard, Issues, Review Tasks, Management Export, and AI Suggestions views render in a browser.
- [x] Old demo-fixture loading control is absent from the application.
- [x] 188 automated tests pass in the tested Python 3.14.4 environment; syntax and dependency checks pass.
- [x] Both AI request paths run through the installed OpenAI SDK with a fake key and in-memory HTTP responses; no provider request is sent.
- [x] Import, product identity, issue/status gates, AI source/decision boundaries, and spreadsheet serialization have regression coverage.
- [x] Current README and case study describe the actual workflow and limitations.

## Required before sharing a GitHub link

- [x] Confirm the final code commit is on GitHub and the intended branch is current.
- [ ] Make the repository public as now requested by the owner, then verify the exact URL opens without signing in. Until then, do not paste it as a freely accessible application link.
- [ ] Check the application/CV wording and any portfolio or social posts against the current README. External publication links have not yet been provided for review.

## Manual acceptance

- [ ] Launch the app with fictional sample data, inspect each tab at a normal laptop width, and confirm labels and tables are readable.
- [ ] Download the management workbook and open it in Microsoft Excel. Confirm the intended sheets, source snapshot, readable layout, and text cells.

## Optional after release

- [ ] If a reviewer uses their own API key with suitable data, inspect one live V2 answer and the improved workbook in Microsoft Excel. Without V2 suggestions, the app does not offer this download. Do not treat a structurally valid response as factually proven.

No login, database, deployment, marketplace integration, automatic write-back, or compliance certification is promised for this local MVP. Old plan/fixture documents in `docs/` record development history and are not current manual test instructions.
