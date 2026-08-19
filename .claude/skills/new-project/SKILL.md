---
name: new-project
description: Bootstrap a new project from this template - copy the folder, fresh git history, install commit guard, clean template leftovers, customize CLAUDE.md. Use when the user says "new project", "start a new paper/course/session", or "set up a project from the template".
argument-hint: "[Project-Name]"
allowed-tools: ["Read", "Edit", "Bash", "Glob", "AskUserQuestion"]
---

# New Project Bootstrap

Automates `templates/new-project-checklist.md`. Run this FROM the template repo
("Claude Setup"); the new project is created as a sibling directory.

## Steps

1. **Gather inputs** (ask only for what's missing):
   - **Project name** — descriptive, hyphenated (e.g., `Peer-Promotion-RCT`).
   - **Project type** — research paper | MBA course | exec ed session
     (determines which "Current State" variant survives).
   - **Slide style** — `teaching` (exec ed / MBA) or `academic`
     (seminar / conference / job talk).

2. **Run the script:**
   ```bash
   ./scripts/new_project.sh "Project-Name"
   ```
   It copies the template, wipes git history, `git init`s, sets
   `core.hooksPath scripts/git-hooks`, and deletes template session logs and
   plans. It refuses to overwrite an existing directory.

3. **Customize the new project's CLAUDE.md** (in the NEW directory):
   - Replace `[Project name — ...]` with the project name.
   - Set `**Slide style:**` to the chosen value.
   - In "Current State": uncomment the variant matching the project type,
     delete the other two, and remove the instruction comment.

4. **Research projects only:** offer to instantiate the research tracker —
   create `research/{hypotheses,insights,decisions}/` and copy the INDEX
   templates from `templates/research-tracker/` (see its README).

5. **Remind about the manual steps** (Claude must not do these):
   - **Box data folder** (if the project uses data): create
     `~/Library/CloudStorage/Box-Box/Research/[Project-Name]/{raw,processed,intermediate,archive}`
     in Box, verify local sync, fill in `data/PROVENANCE.md`
     (per `.claude/rules/data-storage.md`).
   - **First commit** — offer to run it.
   - **GitHub backup**: create a **private** repo, add remote, push
     (checklist Step 8 has the beginner-friendly walkthrough).

6. **Verify:** in the new directory, `git log` shows only the fresh history,
   `git config core.hooksPath` returns `scripts/git-hooks`, and
   `quality_reports/session_logs/` is empty.

## Notes

- The checklist stays authoritative for the *why* and the git primer; this
  skill is the *doing*.
- Never run the script from inside a real project (it checks for template
  markers and refuses, but don't rely on that).
