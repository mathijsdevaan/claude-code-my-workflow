---
name: sync-template
description: Pull template infrastructure improvements into an existing project created from the template. Runs the manifest-driven sync on a review branch, walks through the diff, and reconciles CLAUDE.md drift. Use when the user says "sync from the template", "update this project's setup", or "pull in template improvements".
argument-hint: "[optional: path-to-template]"
allowed-tools: ["Bash", "Read", "Grep", "Glob", "AskUserQuestion"]
---

# Sync From Template

Propagate template-owned infrastructure (rules, skills, agents, hooks,
scripts, templates, Preambles, docs) from the template repo into the current
project — safely, on a review branch, with a human-reviewed diff.

Run this FROM a project, never from the template. The ownership boundary
lives in the TEMPLATE's `scripts/template_sync_manifest.txt`; project
content (CLAUDE.md, MEMORY.md, README.md, Slides/, research/, data/,
quality_reports/, bibliography) is never touched.

## Steps

1. **Preflight.** Confirm a clean working tree (`git status`). If dirty,
   stop and ask the user to commit or stash first — the sync must land on a
   revertable baseline.

2. **Run the sync script** (pass `$ARGUMENTS` through if a template path
   was given):

   ```bash
   scripts/sync_from_template.sh
   ```

   It creates a `template-sync-YYYY-MM-DD` branch, applies the manifest,
   writes `.template-version`, and stages everything. If it errors (can't
   find the template, refuses to run), relay the message and stop.

3. **Review the staged diff** (`git diff --cached`, start from `--stat`).
   Summarize for the user what changed, and inspect three risk areas
   yourself before presenting:
   - **Deletions** anywhere, especially in `docs/` and `scripts/` — confirm
     each deleted file was removed upstream on purpose, not project content
     that strayed into a template-owned directory. If in doubt, ask.
   - **`.claude/settings.json`** — if the project had added its own
     permissions or hooks, re-apply them on top of the synced file.
   - **Skills** — `.claude/skills/` is overlaid, so project-local skills
     (from `/learn`) survive; but a skill deleted from the template lingers.
     Note any project-local skills so the user knows they were preserved.

4. **Report CLAUDE.md drift** (report only — never edit CLAUDE.md
   automatically). Diff the template's CLAUDE.md against the project's and
   list *structural* changes: new/removed rows in the Skills Quick
   Reference table, new sections, changed commands. Offer to apply the
   relevant ones to the project's CLAUDE.md, preserving all project-specific
   content (name, slide style, Current State).

5. **Commit** on the sync branch:

   ```bash
   git commit -m "Sync infrastructure from template (<short-hash>)"
   ```

   Use the template hash from `.template-version`. If the user wants
   anything excluded, `git restore --staged <path> && git checkout -- <path>`
   before committing.

6. **Land it per the project's workflow.** Solo projects merge to main and
   push; PR-based projects go through `/commit` (branch already exists —
   push it and open the PR from there). To abandon instead:
   `git checkout main && git branch -D <sync-branch>`.

7. **Verify.** After merging: hooks still load (no errors on next tool
   use), `git config core.hooksPath` is still `scripts/git-hooks`, and if
   the project compiles slides, one deck still compiles.

## Notes

- `.template-version` records which template commit the project last synced
  to — read it to tell the user how far behind the project was.
- Sync the template's own improvements FIRST (commit them in the template),
  then sync projects; the script warns when the template tree is dirty.
- This skill updates infrastructure only. Content conventions that changed
  in the template (e.g., new deck structure rules) apply to NEW work in the
  project; don't retrofit existing slides/analyses unless asked.
