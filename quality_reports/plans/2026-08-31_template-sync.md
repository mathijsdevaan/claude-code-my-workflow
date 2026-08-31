# Plan: Template → Project Sync Tooling

**Date:** 2026-08-31
**Status:** COMPLETED (2026-08-31 — implemented as planned, no deviations;
12/12 end-to-end test assertions passed, see session log)
**Approved by:** user, in conversation ("Yes, build it — scripts/ is fully generic, docs/ is template-owned")

## Problem

Projects are bootstrapped by copying this template with a fresh `git init`
(`scripts/new_project.sh`), so they share no git ancestry with the template.
Template improvements made since a project was created cannot reach it via
`git pull`. We need a safe, repeatable way to propagate infrastructure
updates into existing projects without damaging project content.

## Approach

Manifest-driven file sync, run from inside a project, always on a review
branch. The template repo owns the manifest and the script, so the sync
mechanism itself improves with the template.

### Ownership boundary (from meta-governance + user decisions)

**Template-owned (synced):** `.claude/rules/`, `.claude/agents/`,
`.claude/hooks/`, `.claude/skills/` (overlay — see below), `scripts/`
(user: "fully generic"), `templates/`, `Preambles/`, `docs/` (user:
"template-owned"), `.claude/settings.json` (hook wiring must track
`hooks/`), `.claude/WORKFLOW_QUICK_REF.md`, `.gitignore`, `LICENSE`.

**Project-owned (never touched):** `CLAUDE.md` (diff-report only),
`MEMORY.md`, `README.md` (ASSUMED project-owned — not confirmed by user),
`Bibliography_base.bib`, `Slides/`, `Figures/`, `research/`, `data/`,
`references/`, `explorations/`, `quality_reports/`,
`.claude/settings.local.json`, `.claude/state/`.

**Overlay mode for `.claude/skills/`:** `/learn` writes project-local
skills into `.claude/skills/`; a plain mirror would delete them. Instead,
each skill directory that exists in the *template* is mirrored
individually; project-local skill directories are left alone. Consequence:
deleting a skill from the template does not delete it in projects (noted
in the skill's review step).

## Tasks

1. **`scripts/template_sync_manifest.txt`** — the manifest (mode + path
   per line). Verify: parsed by script in test run. Done: exists, documented.
2. **`scripts/sync_from_template.sh`** — refuses to run in the template or
   on a dirty tree; auto-locates the template (placeholder marker in
   CLAUDE.md) or takes a path argument; creates `template-sync-YYYY-MM-DD`
   branch; applies manifest via rsync (excluding `.DS_Store`,
   `__pycache__`, `*.pyc`, `.Rhistory`); writes `.template-version`
   (template HEAD hash + date); stages changes; prints diff summary and
   next steps. Verify: end-to-end test on a throwaway project in
   scratchpad. Done: test passes all cases (dirty-tree refusal,
   template-refusal, sync, overlay preservation, idempotence).
3. **`scripts/new_project.sh`** — also write `.template-version` at
   project creation so new projects know their baseline. Verify: test run
   in scratchpad. Done: new project contains correct hash.
4. **`.claude/skills/sync-template/SKILL.md`** — wraps the script: run,
   review staged diff (attention: deletions in `docs/`+`scripts/`,
   `.claude/settings.json` overwrites), CLAUDE.md structural diff report,
   commit/push per project's git workflow. Done: skill file exists.
5. **Docs** — CLAUDE.md skills table row; README section on updating
   existing projects + counts + Last Updated; `docs/architecture-decisions.md`
   entry (supersedes note in 2026-04-16 template-vs-project entry's
   "improvements don't auto-propagate"). Done: all three updated together.
6. **Session log** — `quality_reports/session_logs/2026-08-31_template-sync.md`.

## Verification

- Scripted end-to-end test in scratchpad: create fake project, add
  project-local skill + project content, run sync, assert (a) infra
  updated, (b) project content untouched, (c) local skill survives,
  (d) `.template-version` written, (e) branch created, (f) refusals fire.
- `bash -n` on both scripts.

## Not doing

- Re-establishing shared git history (`--allow-unrelated-histories`) — rejected in discussion.
- Auto-committing or auto-merging the sync — review stays human.
- Syncing CLAUDE.md/README.md content — report-only for CLAUDE.md.
