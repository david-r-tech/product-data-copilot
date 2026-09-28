# Project status — 28 September 2026

Product Data Copilot is a working local Streamlit MVP with three tabs: **Daten prüfen**, **Texte erstellen & übersetzen**, and **Ergebnisse & Export**. It checks CSV/XLSX product data, presents one actionable correction list, and exports a management workbook. Technical scores and session-only audit decisions remain available as details. Its text workspace creates German HTML product copy and bullet points with a full English, French, or Spanish translation, or translates existing text. It works for one selected product or the entire loaded table. A person reviews generated texts per article; the compact two-sheet text workbook contains only explicitly approved texts and matching source rows. The uploaded source remains unchanged.

The data check also flags differing explicit material, colour, and surface values across dedicated columns and structured `attributes`, without claiming to understand arbitrary prose. The [Product-Owner artifacts](product_owner_artifacts.md) make the application claims reviewable and identify proposed measures as a concept, not observed impact.

The latest complete local run passed **196 automated tests** on 28 September 2026 in Python 3.14.4, including approval and export checks. Full-file and single-product flows, translation inputs, safe HTML, dataset changes, workbook contents, and the OpenAI SDK boundary are covered. During final acceptance, exactly one paid creation request for fictional `APP-001` returned German HTML and five German bullets plus English HTML and five English bullets. Every generated factual claim was manually compared with the source data, and no unsupported factual claim was found in this one controlled test. This single example does not prove reliability across products, languages, models, or future outputs. The approved-only gate was checked with fictional offline responses; its workbook contained only the approved SKU in both sheets. Microsoft Excel's visual rendering remains unverified.

## Before using the repository as a job-application reference

1. Open the approved-only text workbook and the management workbook in Microsoft Excel and inspect their visual layout. In the live app, manually perform approve → reject → withdraw/reset → final approve.
2. The implementation is committed and pushed. Confirm that the repository still shows PRIVATE before publication. After publication, verify that its exact URL opens anonymously without signing in.
3. Compare CV and portfolio descriptions with the [README](../README.md); external publication links have not yet been supplied.

Drafts last only for the Streamlit session. Each product starts one paid API request when explicitly generated, with at most one provider retry; up to 100 are processed per click. There are no accounts, database, hosted service, marketplace integrations, automatic approval, source write-back, or compliance guarantees.

The historical work record is in [commerce_readiness_ai_project_log.md](commerce_readiness_ai_project_log.md). Older plans and checklists are not current feature claims.
