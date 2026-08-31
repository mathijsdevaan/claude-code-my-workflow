#!/usr/bin/env bash
# sync_from_template.sh — pull template infrastructure updates into an
# existing project that was created from the template.
#
# Usage:   scripts/sync_from_template.sh [path-to-template]
# Run FROM inside a project (any directory in its git repo). If the template
# path is omitted, looks for a sibling directory whose CLAUDE.md still
# carries the template placeholder marker.
#
# What it does:
#   1. Refuses to run in the template itself, or on a dirty working tree.
#   2. Creates a review branch: template-sync-YYYY-MM-DD.
#   3. Applies the TEMPLATE's scripts/template_sync_manifest.txt
#      (mirror / overlay / file modes — see that file for semantics).
#   4. Records the template's commit in .template-version.
#   5. Stages everything and prints the diff summary for review.
#
# It never commits. Review the staged diff, then commit and merge — or throw
# the branch away (git checkout - && git branch -D <branch>) to undo it all.

set -euo pipefail

MARKER='replace when copying this template'
EXCLUDES=(--exclude '.DS_Store' --exclude '__pycache__' --exclude '*.pyc' --exclude '.Rhistory')

err() { echo "ERROR: $*" >&2; exit 1; }
note() { echo "  note: $*"; }

# --- Locate the project ------------------------------------------------------

PROJECT_DIR="$(git rev-parse --show-toplevel 2>/dev/null)" \
  || err "not inside a git repository. Run this from within a project."
cd "$PROJECT_DIR"

if [ -f CLAUDE.md ] && grep -q "$MARKER" CLAUDE.md; then
  err "this looks like the TEMPLATE repo (CLAUDE.md still has the placeholder marker).
Run this script from inside a project, not the template."
fi

if [ -n "$(git status --porcelain)" ]; then
  err "working tree is not clean. Commit or stash your changes first, so the
sync lands on a clean baseline and can be reverted in one step."
fi

# --- Locate the template -----------------------------------------------------

TEMPLATE_DIR="${1:-${TEMPLATE_DIR:-}}"
if [ -z "$TEMPLATE_DIR" ]; then
  PARENT_DIR="$(dirname "$PROJECT_DIR")"
  candidates=()
  for d in "$PARENT_DIR"/*/; do
    d="${d%/}"
    [ "$d" = "$PROJECT_DIR" ] && continue
    if [ -f "$d/CLAUDE.md" ] && grep -q "$MARKER" "$d/CLAUDE.md" 2>/dev/null \
       && [ -f "$d/scripts/template_sync_manifest.txt" ]; then
      candidates+=("$d")
    fi
  done
  if [ ${#candidates[@]} -eq 1 ]; then
    TEMPLATE_DIR="${candidates[0]}"
  elif [ ${#candidates[@]} -eq 0 ]; then
    err "could not find the template as a sibling directory.
Pass its path explicitly: scripts/sync_from_template.sh /path/to/template"
  else
    err "multiple template candidates found: ${candidates[*]}
Pass the right one explicitly: scripts/sync_from_template.sh /path/to/template"
  fi
fi

TEMPLATE_DIR="$(cd "$TEMPLATE_DIR" && pwd)"
MANIFEST="$TEMPLATE_DIR/scripts/template_sync_manifest.txt"
[ -f "$MANIFEST" ] || err "no manifest at $MANIFEST — is $TEMPLATE_DIR really the template?"
[ "$TEMPLATE_DIR" != "$PROJECT_DIR" ] || err "template and project are the same directory."

TEMPLATE_HASH="$(git -C "$TEMPLATE_DIR" rev-parse HEAD 2>/dev/null || echo 'unknown')"
TEMPLATE_DIRTY=no
if [ -n "$(git -C "$TEMPLATE_DIR" status --porcelain 2>/dev/null)" ]; then
  TEMPLATE_DIRTY=yes
  echo "WARNING: the template repo has uncommitted changes. They WILL be copied,"
  echo "         but .template-version will record commit $TEMPLATE_HASH, which"
  echo "         does not include them. Consider committing the template first."
fi

echo "==> Syncing from: $TEMPLATE_DIR (commit ${TEMPLATE_HASH:0:7}, dirty: $TEMPLATE_DIRTY)"
echo "==> Into project: $PROJECT_DIR"

# --- Create the review branch ------------------------------------------------

BRANCH="template-sync-$(date +%Y-%m-%d)"
n=2
while git show-ref --verify --quiet "refs/heads/$BRANCH"; do
  BRANCH="template-sync-$(date +%Y-%m-%d)-$n"
  n=$((n + 1))
done
git checkout -q -b "$BRANCH"
echo "==> On new branch: $BRANCH"

# --- Apply the manifest ------------------------------------------------------

SYNCED_PATHS=()
while read -r mode path _; do
  case "$mode" in ''|\#*) continue ;; esac
  src="$TEMPLATE_DIR/$path"
  dst="$PROJECT_DIR/$path"
  case "$mode" in
    mirror)
      if [ -d "$src" ]; then
        mkdir -p "$dst"
        rsync -a --delete "${EXCLUDES[@]}" "$src/" "$dst/"
        echo "  mirror  $path"
      else
        note "mirror $path: not in template, skipped (local copy NOT deleted)"
        continue
      fi
      ;;
    overlay)
      if [ -d "$src" ]; then
        mkdir -p "$dst"
        for sub in "$src"/*/; do
          [ -d "$sub" ] || continue
          subname="$(basename "$sub")"
          rsync -a --delete "${EXCLUDES[@]}" "$sub" "$dst/$subname/"
        done
        # top-level files in an overlay dir: copy, never delete
        find "$src" -maxdepth 1 -type f ! -name '.DS_Store' ! -name '.Rhistory' \
          -exec cp -p {} "$dst/" \;
        echo "  overlay $path (project-local subdirectories preserved)"
      else
        note "overlay $path: not in template, skipped"
        continue
      fi
      ;;
    file)
      if [ -f "$src" ]; then
        mkdir -p "$(dirname "$dst")"
        cp -p "$src" "$dst"
        echo "  file    $path"
      else
        note "file $path: not in template, skipped (local copy NOT deleted)"
        continue
      fi
      ;;
    *)
      err "unknown mode '$mode' in manifest (line: $mode $path)"
      ;;
  esac
  SYNCED_PATHS+=("$path")
done < "$MANIFEST"

# --- Record sync state -------------------------------------------------------

{
  echo "template_commit=$TEMPLATE_HASH"
  echo "template_dirty=$TEMPLATE_DIRTY"
  echo "synced_on=$(date +%Y-%m-%d)"
} > .template-version

# --- Stage and report --------------------------------------------------------

if [ ${#SYNCED_PATHS[@]} -gt 0 ]; then
  git add -A -- "${SYNCED_PATHS[@]}" .template-version
else
  git add -A -- .template-version
fi

echo
echo "==> Staged changes:"
git diff --cached --stat || true
echo
if git diff --cached --quiet; then
  echo "Project already matches the template — nothing to sync."
  echo "Clean up with: git checkout - && git branch -D $BRANCH"
else
  cat <<NEXT
Next steps (or run /sync-template in Claude Code, which walks through them):
  1. Review the diff:            git diff --cached
     Pay attention to DELETIONS in docs/ and scripts/, and to overwrites
     of .claude/settings.json (re-apply project-specific permissions).
  2. Commit:                     git commit -m "Sync infrastructure from template (${TEMPLATE_HASH:0:7})"
  3. Merge/push per your workflow (plain push for solo projects, or /commit
     for the branch->PR->merge cycle).
  To undo everything instead:    git checkout - && git branch -D $BRANCH
NEXT
fi
