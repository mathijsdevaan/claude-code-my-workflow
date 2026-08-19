#!/usr/bin/env python3
"""
Context Usage Monitor Hook

Monitors context usage and provides progressive warnings:
- At 40%, 55%, 65%: Suggest /learn for skill extraction
- At 80%: Info-level warning (auto-compact approaching)
- At 90%: Caution-level warning (complete current task with full quality)

Hook Event: PostToolUse (on common tools)
Throttles to 60-second intervals when below warning threshold.

Output: JSON with hookSpecificOutput.additionalContext so reminders are
injected into Claude's context (plain stdout from a PostToolUse hook is
only shown in transcript mode and never reaches Claude).

State is keyed by session_id from the hook input, so tool-call counts and
shown-warning flags reset with each new session instead of accumulating
per project forever.

Note: Since direct context % isn't available, this uses a heuristic based on
tool call count within the current session.
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

# Thresholds (effective percentage, where 100% = auto-compact)
LEARN_THRESHOLDS = [40, 55, 65]
THRESHOLD_WARN = 80
THRESHOLD_CRITICAL = 90

# Throttle interval in seconds (skip checks if below threshold and recent check)
THROTTLE_INTERVAL = 60

# Remove per-session cache files untouched for this long
STALE_CACHE_SECONDS = 7 * 24 * 3600


def get_session_dir() -> Path:
    """Get the per-project directory for storing cache files."""
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "")
    if not project_dir:
        session_dir = Path.home() / ".claude" / "sessions" / "default"
    else:
        import hashlib
        project_hash = hashlib.md5(project_dir.encode()).hexdigest()[:8]
        session_dir = Path.home() / ".claude" / "sessions" / project_hash
    session_dir.mkdir(parents=True, exist_ok=True)
    return session_dir


def get_cache_file(session_id: str) -> Path:
    """Get the cache file for this session (keyed by session_id)."""
    return get_session_dir() / f"context-monitor-cache-{session_id}.json"


def prune_stale_caches() -> None:
    """Best-effort removal of cache files from long-finished sessions."""
    now = time.time()
    try:
        for f in get_session_dir().glob("context-monitor-cache-*.json"):
            if now - f.stat().st_mtime > STALE_CACHE_SECONDS:
                f.unlink()
    except OSError:
        pass


def read_cache(cache_file: Path) -> dict:
    """Read the context monitor cache."""
    if not cache_file.exists():
        return {}
    try:
        return json.loads(cache_file.read_text())
    except (json.JSONDecodeError, IOError):
        return {}


def save_cache(cache_file: Path, data: dict) -> None:
    """Save the context monitor cache."""
    try:
        cache_file.write_text(json.dumps(data, indent=2))
    except IOError:
        pass


def estimate_context_percentage(cache_file: Path) -> float:
    """
    Estimate context usage as a percentage.

    This is a heuristic since we don't have direct access to Claude's context
    window. We use the session's tool call count as a proxy.

    Returns a value from 0-100 representing estimated context usage.
    """
    cache = read_cache(cache_file)

    # Increment tool call counter
    tool_calls = cache.get("tool_calls", 0) + 1
    cache["tool_calls"] = tool_calls
    save_cache(cache_file, cache)

    # Heuristic: assume ~150 tool calls fills context (very rough estimate)
    # This is intentionally conservative to trigger warnings early
    MAX_TOOL_CALLS = 150

    percentage = min((tool_calls / MAX_TOOL_CALLS) * 100, 100)
    return percentage


def is_throttled(cache_file: Path, percentage: float) -> bool:
    """Check if we should skip this check due to throttling."""
    cache = read_cache(cache_file)
    last_check = cache.get("last_check_time", 0)
    now = time.time()

    # If below warning threshold and checked recently, skip
    if percentage < THRESHOLD_WARN and (now - last_check) < THROTTLE_INTERVAL:
        return True

    # Update last check time
    cache["last_check_time"] = now
    save_cache(cache_file, cache)
    return False


def get_shown_thresholds(cache_file: Path) -> dict:
    """Get which thresholds have already been shown in this session."""
    cache = read_cache(cache_file)
    return {
        "learn": cache.get("shown_learn", []),
        "warn_80": cache.get("shown_warn_80", False),
        "warn_90": cache.get("shown_warn_90", False)
    }


def mark_threshold_shown(cache_file: Path, threshold_type: str,
                         value: int | bool = True) -> None:
    """Mark a threshold as shown."""
    cache = read_cache(cache_file)
    if threshold_type == "learn":
        shown = cache.get("shown_learn", [])
        if value not in shown:
            shown.append(value)
        cache["shown_learn"] = shown
    else:
        cache[f"shown_{threshold_type}"] = value
    save_cache(cache_file, cache)


def emit_reminder(message: str) -> None:
    """Emit a reminder as PostToolUse additionalContext JSON."""
    json.dump({
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": message
        }
    }, sys.stdout)


def format_learn_reminder(percentage: float, threshold: int) -> str:
    """Format a /learn skill reminder."""
    return (
        f"Context at ~{percentage:.0f}% (estimated). "
        "If this session produced a non-obvious discovery or reusable workflow, "
        "consider using /learn to capture it as a skill before context compacts. "
        "Skills are saved to .claude/skills/ and persist across sessions."
    )


def format_warn_80(percentage: float) -> str:
    """Format the 80% warning message."""
    return (
        f"Context at ~{percentage:.0f}% (estimated). "
        "Auto-compact will handle context management automatically. "
        "No rush - just be aware that context will be summarized soon."
    )


def format_warn_90(percentage: float) -> str:
    """Format the 90% critical warning message."""
    return (
        f"Context at ~{percentage:.0f}% (estimated) - auto-compact approaching. "
        "Complete the current task with full quality; do NOT cut corners or skip "
        "verification. Consider: save key decisions to the session log, update "
        "the current plan status, and mark completed todos as done."
    )


def run_context_monitor() -> int:
    """Main monitoring logic."""
    # Read hook input
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, IOError):
        hook_input = {}

    session_id = str(hook_input.get("session_id") or "default")
    cache_file = get_cache_file(session_id)
    prune_stale_caches()

    # Estimate current context usage
    percentage = estimate_context_percentage(cache_file)

    # Check throttling
    if is_throttled(cache_file, percentage):
        return 0

    shown = get_shown_thresholds(cache_file)

    # Check /learn thresholds (40%, 55%, 65%)
    for threshold in LEARN_THRESHOLDS:
        if percentage >= threshold and threshold not in shown["learn"]:
            emit_reminder(format_learn_reminder(percentage, threshold))
            mark_threshold_shown(cache_file, "learn", threshold)
            return 0  # Only show one message at a time

    # Check 90% threshold (critical)
    if percentage >= THRESHOLD_CRITICAL and not shown["warn_90"]:
        emit_reminder(format_warn_90(percentage))
        mark_threshold_shown(cache_file, "warn_90", True)
        return 0  # Non-blocking warning (exit 2 would block Claude)

    # Check 80% threshold (info)
    if percentage >= THRESHOLD_WARN and not shown["warn_80"]:
        emit_reminder(format_warn_80(percentage))
        mark_threshold_shown(cache_file, "warn_80", True)
        return 0

    return 0


def main() -> int:
    """Main entry point."""
    return run_context_monitor()


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        # Fail open — never block Claude due to a hook bug
        sys.exit(0)
