# Session Log: 2026-08-31 -- Template → Project Sync Tooling

**Status:** COMPLETED

## Objective

Build a safe, repeatable way to propagate template infrastructure
improvements into existing projects (which have no git ancestry with the
template). Approach approved in conversation; plan at
`quality_reports/plans/2026-08-31_template-sync.md`.

## Changes Made

| File | Change | Reason |
|------|--------|--------|
| `scripts/template_sync_manifest.txt` | NEW — declares template-owned paths + sync modes | Single source of truth for the ownership boundary |
| `scripts/sync_from_template.sh` | NEW — manifest-driven sync on a review branch | The mechanism; refuses dirty trees and the template repo |
| `scripts/new_project.sh` | Writes `.template-version` at creation | New projects know their template baseline |
| `.claude/skills/sync-template/SKILL.md` | NEW — wraps script with diff review + CLAUDE.md drift report | Human-reviewed landing of each sync |
| `CLAUDE.md` | `/sync-template` row in Skills Quick Reference | Table stays in sync with skills on disk |
| `README.md` | "Updating an existing project" section; 25→26 skills; date | README+guide updated together |
| `docs/architecture-decisions.md` | New ADR entry (amends 2026-04-16 separation entry) | Infrastructure decisions live here |

## Design Decisions

Recorded in `docs/architecture-decisions.md` (2026-08-31 entry): manifest
sync over shared-git-history; overlay mode for `.claude/skills/`; sync
always staged on a branch, never auto-committed; `.claude/settings.json`
synced (hook wiring must track hooks/) with review-carefully flag.

User rulings this session: `scripts/` fully generic; `docs/`
template-owned. ASSUMED (flagged to user): `README.md` project-owned.

## Verification Results

| Check | Result | Status |
|-------|--------|--------|
| `bash -n` both scripts | clean | PASS |
| End-to-end in scratchpad (fake template + project) | sync picked up exactly the 5 seeded template changes | PASS |
| Project-local skill (`/learn`-style) survives overlay | preserved | PASS |
| Project content (Slides, customized CLAUDE.md, MEMORY.md) untouched | untouched | PASS |
| Upstream-deleted template file removed in project | removed | PASS |
| `.template-version` written by both scripts, correct hash | correct | PASS |
| Idempotence (second run: "nothing to sync", branch `-2` suffix) | correct | PASS |
| Refusals: dirty tree; running inside template | both refuse | PASS |

12/12 assertions passed.

## Learnings & Corrections

- [LEARN:workflow] Template→project sync needs an overlay mode wherever
  projects legitimately add files inside a template-owned directory
  (`/learn` skills in `.claude/skills/`); a plain mirror silently deletes
  project work.

## Open Questions / Blockers

- ~~README.md ownership is ASSUMED project-owned~~ — RESOLVED 2026-09-01:
  user confirmed project-owned (never synced). No manifest change needed.

## Next Steps

- [x] Run `/sync-template` in one real project as a live shakedown —
      done 2026-08-31 (`ai_mental_health`, synced to 345bb82, verified).

## Incremental Work Log (post-session)

**2026-09-01:** Postdoc question ("why not user-level ~/.claude skills?")
answered and recorded as an ADR in `docs/architecture-decisions.md`
(per-project vendored infrastructure over user-level shared skills).
README.md ownership ruling confirmed by user: project-owned.
