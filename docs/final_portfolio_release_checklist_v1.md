# Portfolio release check — 28 September 2026

Use this checklist before including Product Data Copilot in an application. The current contract is in the [README](../README.md) and [requirements traceability](requirements_traceability.md).

## Verified locally

- [x] App starts with fictional sample data; three workflow tabs are available.
- [x] Old demo-fixture and Quick Drafts controls are absent from the current UI.
- [x] 196 automated tests passed on 28 September 2026 in Python 3.14.4, including generation, individual approval after whole-list creation, approved-only export, translation input, workbook safety, and an offline OpenAI SDK request.
- [x] Exactly one paid creation request during final acceptance used fictional `APP-001` and returned German HTML with five German bullets plus English HTML with five English bullets. Every generated factual claim was manually compared with the source data, and no unsupported factual claim was found in this one controlled test. This does not prove reliability across products, languages, models, or future outputs.
- [x] A live translation-only call returned French text and two translated source bullets.
- [x] A live creation request completed in the browser UI before the approval gate. Its earlier text workbook contained exactly two sheets, 25 product rows, five German and five English bullets for `APP-001`, and no formula cells.
- [x] The README and case study describe the current text workflow and limitations.

## Manual acceptance before sharing

- [ ] Inspect all three tabs at a normal laptop width. Filter the correction list, create one text, translate one existing text, and check every AI claim against the source.
- [ ] Manually perform approve → reject → withdraw/reset → final approve in the live app. Confirm that pending and rejected drafts are excluded from the approved-text download.
- [ ] Open the approved-only two-sheet text workbook and five-sheet management workbook in Microsoft Excel; confirm readable content and unchanged source values.
- [x] Rename the existing GitHub repository to `product-data-copilot`, update the local `origin` URL, and confirm the application link points to this same repository. The existing Git history is retained; the repository remains private.
- [x] Commit and push the current implementation; verify the intended GitHub branch. The repository remains private and publication has not happened.
- [ ] Confirm the repository still shows PRIVATE before publication.
- [ ] Make the repository public when ready and verify its URL opens without signing in.
- [ ] Compare application/CV, portfolio, and social descriptions with the README. External links have not yet been supplied.

A whole-file live run and multiple-language quality review are useful before claiming broad output reliability, but are not required to demonstrate the local workflow honestly. AI drafts require human review. The MVP does not promise deployment, marketplace integration, automatic publication, or compliance certification.
