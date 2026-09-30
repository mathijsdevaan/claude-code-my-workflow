#!/usr/bin/env python3
"""
Session Log Reminder Hook for Claude Code

A Stop hook that tracks how many responses have passed since the *current*
session log was last updated. After a threshold, it blocks Claude from
stopping and reminds it to update (or create) that log.

"Current" means a log for today, per the naming convention
quality_reports/session_logs/YYYY-MM-DD_description.md. A log from an
earlier day is a finished record of different work, so the reminder never
points Claude at one — it asks for a new log instead. (Naming a stale log
caused Claude to append unrelated progress to a completed record.)

State is keyed by both project and session_id (from the hook input JSON),
so two concurrent sessions in the same project cannot suppress or
double-fire each other's reminders.

Adapted from: https://gist.github.com/michaelewens/9a1bc5a97f3f9bbb79453e5b682df462

Usage (in .claude/settings.json):
    "Stop": [{ "hooks": [{ "type": "command", "command": "python3 \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/log-reminder.py" }] }]
"""

from __future__ import annotations

import json
import sys
import hashlib
from pathlib import Path
from datetime import datetime, timedelta

THRESHOLD = 15


def get_state_dir() -> Path:
    """Get state directory under ~/.claude/sessions/ keyed by project."""
    import os
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "")
    if not project_dir:
        state_dir = Path.home() / ".claude" / "sessions" / "default"
    else:
        project_hash = hashlib.md5(project_dir.encode()).hexdigest()[:8]
        state_dir = Path.home() / ".claude" / "sessions" / project_hash
    state_dir.mkdir(parents=True, exist_ok=True)
    return state_dir


def get_project_dir():
    """Get project directory and session id from stdin JSON."""
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        hook_input = {}

    # If stop_hook_active, Claude is already continuing from a previous
    # Stop hook block — let it stop this time to avoid infinite loops.
    if hook_input.get("stop_hook_active", False):
        sys.exit(0)

    session_id = str(hook_input.get("session_id") or "default")
    return hook_input.get("cwd", ""), session_id, hook_input


def get_state_path(session_id: str) -> Path:
    """Return the state file path for the current project and session."""
    return get_state_dir() / f"log-reminder-state-{session_id}.json"


def load_state(state_path: Path) -> dict:
    """Load persisted state, or return defaults."""
    defaults = {"counter": 0, "last_mtime": 0.0, "reminded": False}
    try:
        stored = json.loads(state_path.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return defaults
    if not isinstance(stored, dict):
        return defaults
    # Tolerate state written by an older version of this hook.
    return {k: stored.get(k, v) for k, v in defaults.items()}


def save_state(state_path: Path, state: dict):
    """Persist state to disk."""
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps(state))


def find_current_log(project_dir: str, today: str, yesterday: str) -> tuple[Path | None, float]:
    """Find the session log belonging to the CURRENT session, or None.

    A log qualifies if its filename is dated today. As a concession to
    sessions that run past midnight, a log dated yesterday also qualifies
    if it was modified today — that means this session is still writing to
    it. Logs from any earlier day are finished records of other work and
    are deliberately ignored.
    """
    log_dir = Path(project_dir) / "quality_reports" / "session_logs"
    if not log_dir.is_dir():
        return None, 0.0

    candidates = list(log_dir.glob(f"{today}_*.md"))

    if not candidates:
        for stale in log_dir.glob(f"{yesterday}_*.md"):
            try:
                mtime = stale.stat().st_mtime
            except OSError:
                continue
            if datetime.fromtimestamp(mtime).strftime("%Y-%m-%d") == today:
                candidates.append(stale)

    if not candidates:
        return None, 0.0

    try:
        latest = max(candidates, key=lambda f: f.stat().st_mtime)
        return latest, latest.stat().st_mtime
    except OSError:
        return None, 0.0


def main():
    project_dir, session_id, hook_input = get_project_dir()
    if not project_dir:
        sys.exit(0)

    state_path = get_state_path(session_id)
    state = load_state(state_path)

    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    yesterday = (now - timedelta(days=1)).strftime("%Y-%m-%d")

    current_log, current_mtime = find_current_log(project_dir, today, yesterday)

    # The current log was written since the last check — reset and stay quiet.
    if current_log is not None and current_mtime != state["last_mtime"]:
        save_state(state_path, {"counter": 0, "last_mtime": current_mtime, "reminded": False})
        sys.exit(0)

    state["counter"] += 1

    # Remind at most once per session, and only after the threshold — a short
    # session that never warranted a log is never nagged.
    if state["counter"] >= THRESHOLD and not state["reminded"]:
        state["reminded"] = True
        save_state(state_path, state)
        if current_log is None:
            reason = (
                f"SESSION LOG REMINDER: {state['counter']} responses with no session "
                f"log for today. If this session's work is worth recording, create "
                f"quality_reports/session_logs/{today}_description.md (see "
                f".claude/rules/session-logging.md for what belongs in it, and what "
                f"must not). Do not append to a log from an earlier day."
            )
        else:
            reason = (
                f"SESSION LOG REMINDER: {state['counter']} responses without "
                f"updating the session log. Append your recent progress to "
                f"{current_log.name}."
            )
        json.dump({"decision": "block", "reason": reason}, sys.stdout)
        sys.exit(0)

    save_state(state_path, state)
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        # Fail open — never block Claude due to a hook bug
        sys.exit(0)
