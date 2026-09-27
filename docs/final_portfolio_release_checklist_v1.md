# Portfolio release check — 27 September 2026

Use this checklist just before including Product Data Copilot in an application. The current technical and product contract is in the [README](../README.md) and [requirements traceability](requirements_traceability.md).

## Already verified locally

- [x] App starts with fictional sample data and the normal Dashboard, Issues, Review Tasks, Management Export, and AI Suggestions views render in a browser.
- [x] Old demo-fixture loading control is absent from the application.
- [x] 186 automated tests pass in a fresh virtual environment; syntax and dependency checks pass.
- [x] Import, product identity, issue/status gates, AI source/decision boundaries, and spreadsheet serialization have regression coverage.
- [x] Current README and case study describe the actual workflow and limitations.

## Required before sharing a GitHub link

- [x] Confirm the final code commit is on GitHub and the intended branch is current.
- [ ] Make the repository public as now requested by the owner, then verify the exact URL opens without signing in. Until then, do not paste it as a freely accessible application link.
- [ ] Check the application/CV wording and any portfolio or social posts against the current README. External publication links have not yet been provided for review.

## Manual acceptance

- [ ] Launch the app with fictional sample data, inspect each tab at a normal laptop width, and confirm labels and tables are readable.
- [ ] Download the management and improved workbooks and open them in Microsoft Excel. Confirm the intended sheets, source snapshot, readable layout, and text cells. The improved workbook may contain no suggestions until a V2 response is generated.
- [ ] If an OpenAI key is available **and** fictional data may be sent, generate one V2 response. Check the proposed claim/translation and source fields yourself; approve a valid row, then regenerate and verify the approval clears. Do not treat a structurally valid response as factually proven.

No login, database, deployment, marketplace integration, automatic write-back, or compliance certification is promised for this local MVP. Old plan/fixture documents in `docs/` record development history and are not current manual test instructions.
