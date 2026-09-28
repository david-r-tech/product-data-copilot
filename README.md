# Product Data Copilot

Product Data Copilot is a local Streamlit application for reviewing e-commerce product data before publication. It turns a CSV or XLSX file into a concrete correction list, optional AI text drafts, and safe handoff exports. The intended users are product-data and e-commerce operations teams.

Repository: [david-r-tech/product-data-copilot](https://github.com/david-r-tech/product-data-copilot). It remains private until the final review and publication.

The product question is: **Which product records need attention, why, and what can a reviewer safely hand off next?** The app supports that decision; it does not publish listings or certify compliance.

## Try the workflow

1. Install Python and create an isolated environment: `python -m venv .venv`. The verified environment used Python **3.14.4** on Windows.
2. Install dependencies: `.venv\Scripts\python.exe -m pip install -r requirements.txt` on Windows, or `.venv/bin/python -m pip install -r requirements.txt` on macOS/Linux.
3. Start the app: `.venv\Scripts\python.exe -m streamlit run app.py` on Windows, or `.venv/bin/python -m streamlit run app.py` on macOS/Linux. On Windows, `start_app.bat` also uses `.venv` when available.
4. The app opens with 25 fictional sample products. Use the three tabs **Daten prüfen**, **Texte erstellen & übersetzen**, and **Ergebnisse & Export**, or upload your own file.
5. Download the management workbook or CSV tables. For product copy, copy `.env.example` to `.env`, add your own `OPENAI_API_KEY`, and restart the app. In **Texte erstellen & übersetzen**, choose creation or translation, the full file or one product, and a target language. The start button states how many products will incur an AI request. Then select each generated article, compare the draft with its source fields, and approve or reject it. Download the two-sheet text workbook once at least one article is approved.

The sample file at [data/sample_products.csv](data/sample_products.csv) is fictional and deliberately contains quality gaps. No API key is needed for the core audit and export workflow.

## Input contract

- UTF-8 CSV with comma, semicolon, or tab delimiter, or the first worksheet of an XLSX file. File extension is case-insensitive.
- Required columns: `sku` and `product_name`. Other supported audit fields include `category`, `description`, `brand`, `manufacturer`, `attributes`, `ean`, `language`, `price`, `image_url`, `warning_notes`, `translation_de`, and `translation_en`. The text generator can also use additional populated supplier columns such as material, colour, or surface.
- Every SKU must be non-empty and unique. The app rejects ambiguous files before it assigns issues, review decisions, or generated texts to products.
- Limits for this local MVP: 10 MB, 1,000 products, and 100 columns. Invalid and empty files show a recoverable error.
- Identifiers are read as text, so leading zeros in CSV are preserved. In Excel, format SKU and EAN cells as text **before** entering them; zeros already removed by Excel cannot be recovered.

## What the results mean

Checks identify missing or weak titles/descriptions, missing fields and translations, invalid prices or EAN/GTIN checksums, suspicious image URLs, and missing warning notes for selected safety-relevant categories. Explicit material, colour, or surface values in dedicated columns are also compared with matching `attributes` entries such as `material: cotton; color: blue`; differing values become review warnings with both sources shown. This comparison does not understand contradictions in free-form descriptions or establish which value is correct. **Daten prüfen** shows the affected SKU, field, severity, problem, and recommended next step in one filterable correction list. Source data, score details, and session-only review decisions are available in expandable sections.

The five component scores cover data quality, marketplace-related field completeness, translation-field presence, selected warning-note presence, and content-field completeness. Overall readiness combines them with weights of 35%, 25%, 15%, 15%, and 10%. They remain available as technical details and in the audit workbook, but the main view prioritizes concrete findings. Scores are **not** a measure of generated text quality, marketplace acceptance, or legal compliance. A critical issue forces the status to Critical; another open issue prevents a Ready label even when the numeric score is high. Manual review statuses cannot override those gates or fix source data.

## AI and review boundary

The default audit runs locally. AI calls occur only when the user clicks a generation button and has configured `OPENAI_API_KEY` in an ignored `.env` file (see [.env.example](.env.example)). Product facts or the selected source-text columns are sent to OpenAI. The generator starts one logical request per product; the provider client may retry once after a retryable failure. A click processes up to 100 products and can be repeated for larger files without regenerating completed rows in the current session. `OPENAI_MODEL` can override the configured model. No API key is included in this repository; a reviewer can use their own key.

**Create product copy** uses populated product fields to request a German HTML description and up to five fact-based German bullet points, then complete translations of both into the selected language. **Translate existing copy** uses a selected text column and, optionally, a bullet-point column; it does not add new product facts. The response must be valid JSON for the matching SKU, and HTML is restricted to a small set of safe tags. The prompt discourages unsupported benefits and imprecise product-type translations, but this cannot guarantee factual correctness. A missing fact may result in shorter copy or fewer bullets. Failed products can be retried. Only local format checks produce review notes; the AI cannot certify its own accuracy. Generated texts begin unapproved. A person must compare each text and translation with the source and explicitly approve it for the text export. An approval is session-only, scoped to that source file and language; a new result replaces the earlier decision.

## Exports and data handling

The management workbook in **Ergebnisse & Export** contains five audit sheets and is separate from AI text approval. The text workbook in **Texte erstellen & übersetzen** contains only **Texte & Übersetzungen** and **Originaldaten**. Both sheets include only the approved articles; pending, rejected, failed, and ungenerated text does not enter this workbook. The download appears only after at least one approval. User-provided text is serialized so spreadsheet software does not evaluate it as a formula; recognizable prices in the text workbook's source snapshot are restored as numeric Excel cells, while identifiers remain text. Exports are generated in memory and downloaded locally; the app does not write back to an uploaded product file. Drafts and review state are session-only.

## Engineering notes

`app.py` owns the Streamlit flow. Import-safe modules under `src/product_data_copilot/` implement input validation, rules, scoring, review state, text generation and normalization, and export serialization. The app is deliberately a local MVP; it has no accounts, database, deployment, marketplace integration, automatic approval, or automatic publication.

Run the automated suite with `python -m pytest`. The latest local verification on 28 September 2026 passed **196 automated tests** in the tested Python 3.14.4 environment. Tests cover full-file and single-product generation, individual approval after whole-file generation, approved-only export, translation input, safe HTML and workbook output, plus an offline request through the installed OpenAI SDK. During final acceptance, exactly one paid creation request for fictional `APP-001` returned German HTML and five German bullets plus English HTML and five English bullets. Every generated factual claim was manually compared with the displayed source data, and no unsupported factual claim was found in this one controlled test. This single example does not prove reliability across products, languages, models, or future outputs. The approved-only text workbook and the management workbook still need visual inspection in Microsoft Excel. See the [MVP requirements](docs/product_requirements.md), [requirements and verification](docs/requirements_traceability.md), and [case study](docs/portfolio_case_study.md) for the product decisions and evidence.

The [Product-Owner artifacts](docs/product_owner_artifacts.md) document the vision, Product Goal, assumed stakeholder roles, roadmap, MoSCoW backlog, user story, Definition of Done, and a measurement concept without claiming measured outcomes. The current implementation is committed and pushed, while the repository remains private pending the owner's final manual acceptance. Until its visibility is changed and anonymous access is verified, the GitHub URL is not a working public reference. The repository has no license file. Automated checks are defined in [GitHub Actions](.github/workflows/checks.yml).
