# Project status — 28 September 2026

Product Data Copilot is a working local Streamlit MVP with three tabs: **Daten prüfen**, **Texte erstellen & übersetzen**, and **Ergebnisse & Export**. It checks CSV/XLSX product data, presents one actionable correction list, and exports a management workbook. Technical scores and session-only audit decisions remain available as details. Its text workspace creates German HTML product copy and bullet points with a full English, French, or Spanish translation, or translates existing text. It works for one selected product or the entire loaded table. A person reviews generated texts per article; the compact two-sheet text workbook contains only explicitly approved texts and matching source rows. The uploaded source remains unchanged.

The data check also flags differing explicit material, colour, and surface values across dedicated columns and structured `attributes`, without claiming to understand arbitrary prose. The [Product-Owner artifacts](product_owner_artifacts.md) make the application claims reviewable and identify proposed measures as a concept, not observed impact.

The latest complete local run passed **189 automated tests** in Python 3.14.4, including approval and export checks. Full-file and single-product flows, translation inputs, safe HTML, dataset changes, workbook contents, and the OpenAI SDK boundary are covered. A live creation run directly in the app for fictional `APP-001` produced German/English copy and five bullets per language. A live translation-only call produced French text and two translated bullets. The approved-only gate was checked in the browser with fictional offline responses; its workbook contained only the approved SKU in both sheets. Microsoft Excel's visual rendering and broader model reliability remain unverified.

## Before using the repository as a job-application reference

1. Approve one generated text, reject another, and check that only the approved article appears in both sheets of the text workbook in Microsoft Excel. Check the audit workbook separately. Spot-check generated texts and translations against source facts.
2. Commit and push the accepted code. Make the repository public when ready, then verify that its exact URL opens without signing in.
3. Compare CV and portfolio descriptions with the [README](../README.md); external publication links have not yet been supplied.

Drafts last only for the Streamlit session. Each product starts one paid API request when explicitly generated, with at most one provider retry; up to 100 are processed per click. There are no accounts, database, hosted service, marketplace integrations, automatic approval, source write-back, or compliance guarantees.

The historical work record is in [commerce_readiness_ai_project_log.md](commerce_readiness_ai_project_log.md). Older plans and checklists are not current feature claims.
