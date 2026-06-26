# Product Data Copilot - GitHub Repo Rename Manual Checklist v1

This checklist documents the manual owner steps for renaming the GitHub repository later.

Codex must not rename the GitHub repository, change the local remote URL, or rename local folders in this block.

Related docs:

- [README](../README.md)
- [Final Portfolio Release Checklist](final_portfolio_release_checklist_v1.md)

## 1. Rename Goal

Current GitHub repository:

```text
david-r-tech/commerce-readiness-ai
```

Recommended final GitHub repository:

```text
david-r-tech/product-data-copilot
```

## 2. Pre-Checks Before Rename

Before changing the repository name in GitHub, confirm:

- [ ] Working tree is clean:

```bash
git status
```

- [ ] Latest commit is pushed to GitHub.
- [ ] Current tests pass:

```bash
python -m pytest
```

- [ ] README uses `Product Data Copilot` as the visible product name.
- [ ] No urgent local changes are waiting to be committed.
- [ ] No important screenshots still need the old repository URL.

## 3. Manual GitHub Rename Steps

These steps are done manually by the project owner in GitHub:

1. Open the current GitHub repository:

```text
https://github.com/david-r-tech/commerce-readiness-ai
```

2. Open repository **Settings**.
3. Find the **Repository name** field.
4. Rename from:

```text
commerce-readiness-ai
```

to:

```text
product-data-copilot
```

5. Confirm the repository rename in GitHub.

## 4. After GitHub Rename

After GitHub confirms the rename:

- [ ] Open the new URL:

```text
https://github.com/david-r-tech/product-data-copilot
```

- [ ] Open the old URL and confirm GitHub redirects:

```text
https://github.com/david-r-tech/commerce-readiness-ai
```

- [ ] Check the local remote:

```bash
git remote -v
```

- [ ] If the local remote still points to the old URL, update it manually:

```bash
git remote set-url origin https://github.com/david-r-tech/product-data-copilot.git
```

- [ ] Confirm the updated remote:

```bash
git remote -v
```

- [ ] Fetch from GitHub:

```bash
git fetch origin
```

- [ ] Confirm the local repository is clean:

```bash
git status
```

## 5. External References To Update Manually

After the repository rename, update any public or personal references:

- [ ] CV / Bewerbung
- [ ] Portfolio page
- [ ] LinkedIn, if used
- [ ] Saved browser bookmarks
- [ ] GitHub profile pinned repository, if needed
- [ ] Screenshot checklist notes, if screenshots show the old URL
- [ ] Any shared links sent to reviewers or colleagues

## 6. What Not To Do

Do not:

- Rename the Python package path `src/product_data_copilot/`.
- Rewrite git history.
- Mass-edit old historical logs.
- Change source behavior.
- Rename the repository before checks are green.
- Rename local folders unless there is a separate, explicit owner decision.
- Change generated filenames unless a separate compatibility cleanup block approves it.

## 7. Risks

- Old links may rely on GitHub redirects.
- The local remote may still point to the old URL after the GitHub rename.
- Screenshots may show the old repository URL.
- README or portfolio links may need one final check.
- A local clone may need a manual remote update.
- External references such as CV or LinkedIn may become stale.

## 8. Acceptance Criteria

The manual rename is complete when:

- [ ] New repo URL works:

```text
https://github.com/david-r-tech/product-data-copilot
```

- [ ] Old repo URL redirects:

```text
https://github.com/david-r-tech/commerce-readiness-ai
```

- [ ] Local `git remote -v` points to the new repository URL.
- [ ] `git status` is clean.
- [ ] CV link uses the new URL.
- [ ] Portfolio or LinkedIn links use the new URL, if applicable.
- [ ] README and case study still render correctly.
- [ ] Final screenshots do not accidentally show stale repository naming unless intentionally documented.

## 9. Recommended Next Step

```text
Complete manual owner tasks from the Final Portfolio Release Checklist.
```

The repository rename itself remains an owner-only action.
