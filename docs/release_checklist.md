# Release checklist — 29 September 2026

Use this checklist to verify Product Data Copilot before sharing it. The current contract is in the [README](../README.md) and [requirements traceability](requirements_traceability.md).

## Verified locally

- [x] App starts with fictional sample data; three workflow tabs are available.
- [x] 231 automated tests passed on 29 September 2026 in Python 3.14.4, including extracted-module boundaries, generation, individual approval after whole-list creation, approved-only export, translation input, workbook safety, malformed responses, and offline OpenAI SDK success and failure paths.
- [x] GitHub Actions verifies dependency consistency, compilation of `app.py` and `src`, and pytest on Windows and Ubuntu with Python 3.14.
- [x] Exactly one paid creation request during final acceptance used fictional `APP-001` and returned German HTML with five German bullets plus English HTML with five English bullets. Every generated factual claim was manually compared with the source data, and no unsupported factual claim was found in this one controlled test. This does not prove reliability across products, languages, models, or future outputs.
- [x] A live translation-only call returned French text and two translated source bullets.
- [x] The README and case study describe the current text workflow and limitations.
- [x] Repository renamed to `product-data-copilot`, current implementation committed and pushed.
- [x] Repository is public at `https://github.com/david-r-tech/product-data-copilot`.

## Remaining manual acceptance

- [ ] Inspect all three tabs at a normal laptop width. Filter the correction list, create one text, translate one existing text, and check every AI claim against the source.
- [ ] Manually perform approve → reject → approve in the live app and use previous/next navigation between generated articles. Confirm that pending and rejected drafts are excluded from the approved-text download.
- [ ] Open the approved-only two-sheet text workbook and five-sheet management workbook in Microsoft Excel; confirm readable content and unchanged source values.
- [ ] Confirm that any external product description matches the README and its documented limitations.

A whole-file live run and multiple-language quality review are useful before claiming broad output reliability, but are not required to demonstrate the local workflow honestly. AI drafts require human review. The MVP does not promise deployment, marketplace integration, automatic publication, or compliance certification.
