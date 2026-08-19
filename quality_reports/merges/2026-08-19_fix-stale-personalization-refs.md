# Quality Report: Merge to Main -- 2026-08-19

## Summary
Removed all remaining internal references to infrastructure deleted in the
2026-04-16 personalization (Quarto/, guide/, master_supporting_docs/,
scripts/sync_to_docs.sh). 23 files across rules, skills, agents, settings,
and scripts; net -71 lines. Merged as PR #9.

## Files Modified
| File | Type | Quality Score |
|------|------|---|
| `.claude/rules/*` (8 rules incl. rewritten verification-protocol, single-source-of-truth) | Config | 95/100 |
| `.claude/skills/*` (11 skills incl. deep-audit repointing) | Config | 95/100 |
| `.claude/agents/verifier.md`, `.claude/agents/r-reviewer.md` | Config | 95/100 |
| `.claude/settings.json` (user-edited: removed sync_to_docs allowlist) | Config | 95/100 |
| `.claude/WORKFLOW_QUICK_REF.md` (placeholders filled from pinned values) | Config | 90/100 |
| `scripts/quality_score.py` (usage examples only) | Code | 95/100 |

## Verification
- [x] Compilation/execution succeeds — quality_score.py parses; settings.json valid JSON
- [ ] Tolerance checks PASS (not applicable — no analysis code)
- [ ] Tests pass (not applicable)
- [x] Quality gates >= 80 — re-grep for all six stale patterns clean; CLAUDE.md skills table matches disk 1:1

## Status
MERGED

## Notes
- Deliberate keeps (template genericity): score_quarto path in quality_score.py,
  .qmd guidance in reviewer agents, `Bash(quarto render *)` allowlist entry,
  and the .qmd rubric in quality-gates.md. Remove these too if Quarto support
  should be dropped from the public template entirely.
- WORKFLOW_QUICK_REF "Reporting" and "Replication" preferences had no pinned
  source; filled with sensible defaults — adjust if they don't match taste.
- settings.json was edited manually by the user (protect-files.sh blocks Claude).
