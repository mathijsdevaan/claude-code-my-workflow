---
name: replication-audit
description: Launch a fresh-context correctness audit of the project's analysis code - code correctness, R-to-Python replication of key results, econometrics, output automation, and replication-package readiness. Use before submitting a paper, before sharing results with coauthors, when the user says "audit my code", "referee my analysis", or "is this correct", or for round-2 review of fixes after a prior audit.
argument-hint: "[scope: paper | scripts/R/file.R | explorations/name] [round N]"
allowed-tools: ["Read", "Grep", "Glob", "Bash", "Task"]
---

# Replication Audit (Referee 2)

Dispatches the `replication-auditor` agent. The agent runs as a subagent with
**fresh context** — this is deliberate: the Claude that wrote the code will
rationalize its own choices, so the auditor must not share this session's
context. Do not paste this session's reasoning about the code into the prompt.

## Steps

1. **Determine scope.** From `$ARGUMENTS` or by asking: whole paper pipeline,
   a specific script, or an exploration? Identify the primary language
   (usually R here) and where outputs live. Note the project type for the
   agent's scope-calibration table (paper = full intensity; exploration =
   code audit only).

2. **Determine round.** If `quality_reports/replication_audits/` contains a
   prior report for this scope, this is round N+1: the agent must read the
   prior report and the author response, and classify each prior concern
   (Fixed / Justified / Ignored-escalate / New issues).

3. **Prepare directories** (the agent may only write in these):
   ```bash
   mkdir -p code/replication quality_reports/replication_audits
   ```

4. **Launch the `replication-auditor` agent** with a factual brief only:
   - scope (files/directories to audit) and project type
   - primary language and where data access instructions live
     (`data/PROVENANCE.md`; raw data is in Box per `.claude/rules/data-storage.md`)
   - round number and prior-report path if round 2+
   - reminder: report-only; replication scripts to `code/replication/`;
     report to `quality_reports/replication_audits/`
   Do NOT include: this session's interpretation of the results, what you
   expect the audit to find, or justifications for coding choices.

5. **Relay the report.** Present the verdict, Major Concerns, and the
   replication comparison table. Do not soften findings.

6. **Author response (separate step, on request).** When the user wants to
   respond: create `quality_reports/replication_audits/response_round[N].md`
   with, per Major Concern, **Fixed** (what changed, where) or **Justified**
   (why no change), plus a summary table of code changes. Fixes are applied by
   the main session (the author), never by the auditor. Then re-run this skill
   for the next round.

## What this skill does NOT do

- Fix the code (the author does, after reading the report)
- Replace `/review-r` (style/conventions) or `/blindspot` (perception of
  output) — run those separately
- Audit slide decks (that's `/slide-excellence`)
