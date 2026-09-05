# Session Logging

**Location:** `quality_reports/session_logs/YYYY-MM-DD_description.md`
**Template:** `templates/session-log.md`

## Three Triggers (all proactive)

### 1. Post-Plan Log

After plan approval, immediately capture: goal, approach, rationale, key context.

### 2. Incremental Logging

Append 1-3 lines whenever: a design decision is made, a problem is solved, the user corrects something, or the approach changes. Do not batch.

**Decisions live in their tracker, not here.** Research decisions go to `research/decisions/`, Claude-behavior decisions to CLAUDE.md's Key Decisions table, infrastructure decisions to `docs/architecture-decisions.md`. The session log records that a decision happened and links to it — it never duplicates the entry.

### 3. End-of-Session Log

When wrapping up: high-level summary, quality scores, open questions, blockers.

## Which Repo the Log Goes In

**A session log belongs to the repo whose work it describes — not the repo the
session happened to run in.**

Sessions frequently run in one project while doing work on another. When a
session in repo A touches project B, the log goes in B. If B has no repo yet,
park the log in B's working tree until it does. Never log B's work into A.

### Confidentiality of log contents

Before writing any session log, assume the repo is or will become public.
Never record:

- Partner, client, or funder names
- Collaborator or RA names
- Private repository URLs
- Data file or dataset names, and on-disk paths outside this repo

Refer to them generically instead — "a partner-firm project", "a collaborator",
"the study dataset". If the substance can't survive that abstraction, the log
belongs in the private project's repo, not here.

**Why this is strict:** a log about private work committed to a public repo is
a disclosure, and deleting the file does not undo it — the content persists in
commit history, pull request diffs, and forks. Recovery means rewriting
published history. Cheap to avoid, expensive to fix. See `meta-governance.md`
for the generic-vs-specific decision framework.

## Quality Reports

Generated **only at merge time** -- not at every commit or PR.
Save to `quality_reports/merges/YYYY-MM-DD_[branch-name].md` using `templates/quality-report.md`.
