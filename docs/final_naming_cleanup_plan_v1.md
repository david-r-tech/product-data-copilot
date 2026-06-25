# Product Data Copilot - Final Naming Cleanup Plan v1

This plan defines a careful naming cleanup path from the original working name to the final product name.

This is a planning document only. Do not rename the GitHub repository, local folder, package path, remote URL, or generated filenames until a later approved implementation block.

## 1. Final Product Name

Final visible product name:

```text
Product Data Copilot
```

This should be the primary visible name in:

- README
- Streamlit UI
- portfolio case study
- screenshot checklist
- current status docs
- future portfolio presentation

## 2. Final Recommended GitHub Repository Name

Recommended final GitHub repository name:

```text
product-data-copilot
```

Current repository name:

```text
commerce-readiness-ai
```

The repository should not be renamed automatically by Codex. This needs an explicit owner action in GitHub.

## 3. Old Names To Search For

Future cleanup blocks should search for:

- `Commerce Readiness AI`
- `Commerce Readiness`
- `commerce-readiness-ai`
- `commerce_readiness_ai`
- `commerce_readiness`
- old generated filenames such as `commerce_readiness_ai_management_export.xlsx`

Current read-only inspection found likely cleanup candidates in:

- visible Streamlit layout helper text
- `start_app.bat`
- README historical note and old management export filename
- older documentation titles such as demo script, testing notes, screenshot notes, and product requirements
- project log historical entries
- tests that intentionally lock older UI text
- export helper constant and tests for the management export filename
- Git remote URL pointing to `david-r-tech/commerce-readiness-ai`

## 4. What Should Be Changed Later

Future safe cleanup should consider:

- README visible links and text
- docs visible current-product references
- project status docs
- portfolio case study references
- screenshot checklist references
- Streamlit UI visible references if any remain
- `start_app.bat` startup message
- old generated file names only if safe and not disruptive
- test expectations only when corresponding visible UI or constants are intentionally changed
- GitHub repository description and topics later, manually

## 5. What Should Not Be Changed Automatically

Do not automatically change:

- Python package path `src/product_data_copilot/`
- stable helper module names
- tests unless a future block intentionally updates visible text or filenames
- git history
- old project log historical references unless they are presented as current branding
- local remote URL without human confirmation
- GitHub repository name without manual owner action
- local project folder name without manual owner confirmation

Historical references can remain if they are clearly framed as the former name.

## 6. Manual GitHub Rename Steps For The Project Owner

When the owner decides to rename the GitHub repository:

1. Open the GitHub repository.
2. Go to repository Settings.
3. Find Repository name.
4. Rename from:

```text
commerce-readiness-ai
```

to:

```text
product-data-copilot
```

5. Confirm GitHub redirects from old links.
6. Update the local remote URL if needed:

```bash
git remote set-url origin https://github.com/david-r-tech/product-data-copilot.git
```

7. Run:

```bash
git remote -v
git status
```

8. Update CV, LinkedIn, portfolio, and any shared links after the rename.

## 7. Risks

Naming cleanup risks:

- Broken GitHub or documentation links
- Stale README references
- Local remote URL mismatch after a GitHub rename
- Screenshots showing the old name
- Over-editing historical documentation
- Confusing old generated export filenames with current branding
- Test failures if visible UI text or export constants are renamed without updating tests
- Users with old cloned repository URLs needing to update remotes

## 8. Recommended Implementation Phases

### Phase 1: Naming Cleanup Plan

This document.

Scope:

- document target name
- document repository rename recommendation
- identify old-name search terms
- define safe and unsafe cleanup areas

### Phase 2: Safe Visible Text Cleanup

Recommended next block:

```text
Safe Naming Cleanup v1
```

Scope:

- update visible current-product text in docs/app where safe
- update `start_app.bat` message if allowed
- update old current-facing documentation titles if safe
- keep historical entries as historical
- update tests only if visible UI text is intentionally changed

### Phase 3: Optional Generated Filename Cleanup

Scope:

- decide whether to rename `commerce_readiness_ai_management_export.xlsx`
- update export constants and tests if approved
- document compatibility impact

This should be separate because filenames can affect existing documentation and user habits.

### Phase 4: Manual GitHub Repository Rename

Owner-only action.

Scope:

- rename GitHub repository to `product-data-copilot`
- update local remote URL after confirmation
- verify redirect behavior
- update public links

### Phase 5: Final Link Verification

Scope:

- verify README links
- verify case study links
- verify screenshot checklist references
- verify remote URL
- verify CV/LinkedIn/portfolio links

## 9. Acceptance Criteria

Future naming cleanup should pass if:

- Visible current product name is consistently `Product Data Copilot`.
- Old name remains only where historically necessary.
- The old repository name remains only before manual GitHub rename or as historical context.
- No code behavior changes are introduced.
- Tests still pass after future implementation blocks.
- README and portfolio docs do not look stale.
- No links are broken.

It should fail if:

- Current-facing UI still prominently shows `Commerce Readiness AI`.
- The Git remote is changed without owner confirmation.
- Git history or historical project log entries are over-edited.
- Tests fail because renamed UI text or filenames were not updated intentionally.
- Screenshots or public docs point to a stale product identity.

## 10. Recommended Next Block

```text
Safe Naming Cleanup v1
```

This next block should be implementation, but still conservative. It should update only safe visible text references and documentation references. It should not rename the repository or local folder.
