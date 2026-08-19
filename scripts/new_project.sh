#!/usr/bin/env bash
# new_project.sh — bootstrap a new project from this template.
# Automates Steps 1–3 and 5 of templates/new-project-checklist.md; the
# checklist remains the human-readable reference (and git primer).
#
# Usage:   ./scripts/new_project.sh "Project-Name"
# Run FROM the template repo root. Creates a sibling directory.

set -euo pipefail

if [ $# -ne 1 ] || [ -z "$1" ]; then
  echo "Usage: ./scripts/new_project.sh \"Project-Name\"" >&2
  exit 1
fi

PROJECT_NAME="$1"
TEMPLATE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PARENT_DIR="$(dirname "$TEMPLATE_DIR")"
TARGET_DIR="$PARENT_DIR/$PROJECT_NAME"

if [ ! -f "$TEMPLATE_DIR/CLAUDE.md" ] || [ ! -d "$TEMPLATE_DIR/Preambles" ]; then
  echo "ERROR: $TEMPLATE_DIR does not look like the template repo." >&2
  exit 1
fi

if [ -e "$TARGET_DIR" ]; then
  echo "ERROR: $TARGET_DIR already exists. Refusing to overwrite." >&2
  exit 1
fi

echo "==> Step 1: Copying template to $TARGET_DIR"
cp -R "$TEMPLATE_DIR" "$TARGET_DIR"

cd "$TARGET_DIR"

echo "==> Step 2: Fresh git history"
rm -rf .git
git init -q
git branch -m main 2>/dev/null || true

echo "==> Step 3: Installing large-file commit guard"
git config core.hooksPath scripts/git-hooks

echo "==> Step 5: Cleaning out template leftovers"
rm -f quality_reports/session_logs/*.md
rm -f quality_reports/plans/*.md
rm -f .claude/settings.local.json      # machine-local permissions; don't propagate
rm -rf .claude/state 2>/dev/null || true
rm -f .DS_Store scripts/.DS_Store explorations/.DS_Store 2>/dev/null || true
rm -f .Rhistory templates/.Rhistory 2>/dev/null || true

cat << NEXT

Done. New project at: $TARGET_DIR

Manual steps remaining (see templates/new-project-checklist.md):
  Step 4: Customize CLAUDE.md — project name, slide style (teaching|academic),
          uncomment ONE "Current State" variant, delete the others.
          (Or run /new-project in Claude Code, which does this for you.)
  Step 5b: Optionally rm references/reference-deck-*.pdf if you don't want exemplars.
  Step 6: If the project uses data — create the Box folder:
          ~/Library/CloudStorage/Box-Box/Research/$PROJECT_NAME/{raw,processed,intermediate,archive}
          and fill in data/PROVENANCE.md.
  Step 7: First commit (git add -A && git commit -m "Initial commit from template").
  Step 8: Private GitHub repo + git remote add origin + push.
NEXT
