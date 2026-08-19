# Session Log: MixtapeTools Adoption

**Date:** 2026-08-19
**Plan:** `quality_reports/plans/great-i-want-to-enchanted-scott.md` (APPROVED)

## Objective

Evaluate Scott Cunningham's MixtapeTools repo (github.com/scunning1975/MixtapeTools)
and adopt selected patterns into this template.

## Key context

- Evaluation found our biggest gap is the absence of a research-project tracker;
  his GTD harness (hypotheses/insights/decisions + falsification-gated statuses)
  fills it. Adopting the lightweight version (no dashboard).
- Porting: /blindspot, replication-audit (Referee 2 adapted), validate-bib --verify
  (bibcheck adapted). Declined: /split-pdf, dashboard server.
- Quick wins: CLAUDE.md research-state sections (Estimation Philosophy, Dropped
  Analyses, Key Decisions), 3-strikes circuit breaker, TikZ arithmetic rules,
  read-the-.log rule, MEMORY.md [LEARN] entries.
- New /new-project skill + scripts/new_project.sh to automate the manual checklist.

## Design decisions

| Decision | Alternatives considered | Rationale |
|----------|------------------------|-----------|
| Subagent = "fresh terminal" for replication audit | Separate terminal session (Cunningham's approach) | Subagents get fresh context for free; no manual session juggling |
| research/ top-level dir + templates/research-tracker/ starter kit | Root-level hypotheses/ etc. (his layout) | Keeps project root uncluttered; consistent with our folder conventions |
| Extend validate-bib with --verify mode | Separate /bibcheck skill | Internal-consistency and external-accuracy checks belong on one surface |

## Incremental work log

- [start] Plan approved; session log created.
- [phase 1] Quick wins applied: CLAUDE.md research-state sections, circuit breaker (orchestrator + compile-latex), .log-reading rule (compile-latex + verification-protocol), TikZ arithmetic (rule + agent), 4 MEMORY.md entries.
- [phase 2] Research tracker built: templates/research-tracker/ (6 files), research/.gitkeep, .claude/rules/research-tracking.md, .claude/skills/research-log/SKILL.md.
- [phase 3a] /blindspot ported; replication-auditor agent + /replication-audit dispatch skill created (fresh-context subagent = Cunningham's fresh-terminal isolation).
- [phase 3b] validate-bib extended with --verify deep mode (per-entry parallel verification agents + reviewer pass, timestamped run dirs, never overwrites source bib).
- [phase 4] scripts/new_project.sh + /new-project skill created; checklist header updated (uncommitted Step-1 edit preserved).
- [phase 5] CLAUDE.md skills table synced (24 rows, matches disk).

## End of session

**Summary:** All 5 phases of the MixtapeTools adoption plan implemented and verified.
- New skills: /research-log, /blindspot, /replication-audit, /new-project; validate-bib gained --verify.
- New agent: replication-auditor. New rule: research-tracking. New templates: research-tracker kit (6 files).
- Edits: CLAUDE.md (research-state sections + skills table), MEMORY.md (4 [LEARN] entries), orchestrator-protocol (circuit breaker), tikz rule + agent (arithmetic anti-collision), verification-protocol + compile-latex (.log reading + circuit breaker), preregistration (tracker seeding), new-project-checklist (automation header).

**Verification:** new_project.sh tested end-to-end on a throwaway project (fresh history, hooksPath, cleanup — then deleted); tracker templates round-tripped; skill frontmatter linted; CLAUDE.md table matches skills on disk.

**Quality scores:** n/a — all markdown infrastructure; quality_score.py scores .tex/.qmd/.R only.

**Open items:**
- Stale-reference cleanup (README counts, deep-audit's deleted guide target, dead pdf-processing rule scope, sync_to_docs.sh references) — separate session suggested.
- Dashboard server for the research tracker — deferred by user decision; file schema is compatible.
- Not committed — awaiting user go-ahead.

## Post-review streamlining fixes (same session)

User asked for a conflict audit before committing; six friction points found, five fixed:
1. Drift check made live: mirrored into CLAUDE.md research variant (research-tracking rule is scoped to research/** and never loads while writing prose); rule now notes the mirroring.
2. Blindspot mandate softened: required only for results bound for a paper, deck, or coauthor email.
3. Orchestrator limits disambiguated: verification retries (max 2) vs. circuit breaker (3 fix attempts for one persistent error).
4. session-logging rule: decisions live in their tracker (research/decisions, CLAUDE.md table, architecture-decisions.md); session log links, never duplicates.
5. new_project.sh now removes .claude/settings.local.json and .claude/state on copy.
6. MEMORY.md contradiction resolved per user decision: session logs mandatory for ALL work including template sessions; superseding entry documents that forks stay clean via new_project.sh cleanup.

Deferred (noted, not requested): /interview-me vs /research-log interview-style inconsistency; pruning always-on rules (both slide themes + meta-governance, ~710 lines) in child projects.
