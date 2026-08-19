# Plan: Fix Hook Design Bugs (Deep-Audit 2026-08-19 Deferred Items)

**Date:** 2026-08-19
**Status:** COMPLETED (no deviations; issue #4 report-only as planned)
**Branch:** claude/admiring-edison-156f84

## Context

The 2026-08-19 deep-audit confirmed four design-level bugs in `.claude/hooks/`
that were deferred from mechanical fixing. All four were re-verified today
against the current files — all still exist.

## Verified issues and fixes

### 1. context-monitor.py — state cache keyed by project, never by session
- **Files:** `.claude/hooks/context-monitor.py`
- **Action:** Read `session_id` from hook input JSON (confirmed present in the
  common hook input per current docs). Key the cache file per session:
  `context-monitor-cache-{session_id}.json`. Prune stale per-session cache
  files (>7 days) best-effort. `tool_calls`, `shown_learn`, `shown_warn_*`
  now start fresh each session.
- **Verify:** Pipe sample JSON twice with session A (counter increments),
  then once with session B (counter restarts at 1). Pre-seed cache near a
  threshold and confirm the reminder fires once, then is suppressed within
  the same session only.
- **Done:** Fresh session ⇒ fresh estimate and warnings; no cross-session bleed.

### 2. log-reminder.py — per-project state shared across concurrent sessions
- **Files:** `.claude/hooks/log-reminder.py`
- **Action:** Incorporate `session_id` from hook input into the state
  filename: `log-reminder-state-{session_id}.json`.
- **Verify:** Pipe Stop-hook JSON with two session_ids; confirm two separate
  state files and independent counters. Confirm block JSON still emitted at
  THRESHOLD with stale log.
- **Done:** Concurrent sessions no longer share counter/mtime/reminded state.

### 3. PostToolUse reminders printed to stdout never reach Claude
- **Files:** `.claude/hooks/context-monitor.py`, `.claude/hooks/verify-reminder.py`
- **Action:** Replace plain `print()` with JSON on stdout:
  `{"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": "..."}}`
  (schema confirmed against current Claude Code hooks docs; additionalContext
  max 10,000 chars). Strip ANSI color codes — the text is injected into
  Claude's context, not rendered in a terminal.
- **Verify:** Pipe sample PostToolUse JSON; confirm stdout parses as JSON
  with the correct hookEventName and non-empty additionalContext.
- **Done:** /learn and verification reminders are injected into Claude's context.

### 4. settings.json PostToolUse matcher "Bash|Task" misses current subagent tool
- **Files:** `.claude/settings.json` (line ~96) — WRITE-PROTECTED by protect-files.sh
- **Action:** NOT edited (protection respected; user approval required).
  Recommended manual edit: change matcher `"Bash|Task"` to `"Bash|Task|Agent"`.
- **Verify:** n/a (user applies manually)
- **Done:** Reported in PR description and final summary with exact edit.

## Order
1. Save plan + session log (this step)
2. Fix #1 and #3 in context-monitor.py (one rewrite)
3. Fix #2 in log-reminder.py
4. Fix #3 in verify-reminder.py
5. Test all three hooks by piping sample JSON with isolated CLAUDE_PROJECT_DIR
6. Commit via branch + PR per .claude/skills/commit; report #4 for manual action
