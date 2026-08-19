# Plan: Adopt selected patterns from Scott Cunningham's MixtapeTools

**Date:** 2026-08-19
**Status:** COMPLETED (2026-08-19)
**Source evaluated:** https://github.com/scunning1975/MixtapeTools (cloned to scratchpad; full analysis in session)

---

## Context

Mathijs asked for an evaluation of Scott Cunningham's Claude Code setup and a plan to
adopt what improves this template. The comparative evaluation found:

- **Our biggest gap:** no research-project tracker. Tracking is scattered across the
  CLAUDE.md "Current State" block, session logs, and preregistration docs. Cunningham's
  GTD harness (hypotheses/insights/decisions with a falsification-gated status machine)
  fills this.
- **Epistemics skills we lack:** pre-interpretation output audit (`/blindspot`),
  correctness/replication code audit in an isolated context (Referee 2), and external
  bibliography *accuracy* verification (our `validate-bib` only checks internal key
  consistency).
- **Technique upgrades:** TikZ review by arithmetic instead of eyeballing; a 3-strikes
  circuit breaker for compile-fix loops; reading the `.log` file directly; negative-
  knowledge sections in CLAUDE.md ("Dropped Analyses", "Estimation Philosophy").
- **Shared gap he also has:** manual project bootstrap → automate ours.

User decisions (2026-08-19): lightweight GTD (no dashboard); port blindspot +
referee-2 code audit + bibcheck verification (NOT split-pdf); all quick wins; build
`/new-project` automation.

Meta-governance: everything below is GENERIC (helps any fork) → committed. Credit
MixtapeTools in adapted files (his attribution pattern is worth copying too).

---

## Phase 1 — Quick wins (edits to existing files)

1. **CLAUDE.md template** (`CLAUDE.md`, the commented-out "Current State: Research
   project" variant): add three sections adapted from his `claude/CLAUDE.md`:
   - **Estimation Philosophy** — behavioral constraint: no excitement/concern about
     point estimates until the design is intentional; attachment is to design, not
     findings.
   - **Dropped Analyses** — negative-knowledge cache: things tried and abandoned so
     Claude doesn't re-suggest them.
   - **Key Decisions Made** — dated table (Date | Decision | Rationale) for *research*
     decisions (distinct from `docs/architecture-decisions.md`, which is infrastructure).

2. **3-strikes circuit breaker** → `.claude/rules/orchestrator-protocol.md` (Limits
   section) and `.claude/skills/compile-latex/SKILL.md`: after 3 distinct failed
   approaches to the *same* error — stop, quote the log line, list the 3 approaches and
   why each failed, ask the user. Define "same error" (persists at same/nearby line);
   new error elsewhere resets the counter. Overrides zero-warning perfectionism.

3. **TikZ arithmetic rules** → merge into `.claude/agents/tikz-reviewer.md` and
   `.claude/rules/tikz-visual-quality.md` (from his `tikz_rules.md`):
   - Bézier label clearance: `max_depth = (chord/2)·tan(bend/2)`, safe distance =
     depth + 0.5cm, with the tan(θ/2) lookup table and a worked example.
   - Label width estimation: width-per-character table by font size (`\scriptsize`
     0.10cm … `\normalsize` 0.18cm; bold +10%, mono +15%) + gap math
     (`usable = center-to-center − halfwidths − 0.6cm`).
   - Required `% Coordinate map:` comment block before every `tikzpicture`.
   - Never `scale` a complex diagram; never define parameterized TikZ styles inside a
     Beamer frame (`#` is eaten by the frame parser — `\tikzset{}` in preamble).
   - Clearance table (label↔label 0.3cm, label↔axis 0.3cm, object↔slide edge 0.5cm).
   - Framing principle at top of the agent: "Claude cannot eyeball where a curve
     passes — compute, never eyeball."

4. **Log-reading rule** → `.claude/skills/compile-latex/SKILL.md` and
   `.claude/rules/verification-protocol.md`: after compiling, read the `.tex`'s `.log`
   file directly rather than only grepping terminal output (grep false-positives on
   package-description strings and misses real warnings).

5. **MEMORY.md** — add `[LEARN]` entries: hook-only-silent-failures principle
   (visible failures fix themselves); typed session isolation (isolate when auditing
   implementation, not when auditing perception); replace-perception-with-arithmetic.

## Phase 2 — Lightweight research tracker (GTD-lite)

New top-level `research/` directory (template, `.gitkeep`ed like `Slides/`) with a
starter kit in `templates/research-tracker/`:

- `templates/research-tracker/hypotheses-INDEX.md`, `H00_example.md` — hypothesis file
  format: frontmatter (`id, title, status, parent, date_proposed, date_resolved`) +
  Claim (one testable sentence) + Courtroom block (Estimand / Population / Variation /
  Mechanism / Falsification) + **Kills It** (falsifiers written before the test) +
  Evidence (links to insights).
- `templates/research-tracker/insights-INDEX.md`, insight template — frontmatter
  (`date, updates: <HID>, result: confirmed|rejected|complicated, script, output`) +
  Finding + Key Numbers (numbers mandatory: estimate, SE, CI, p, N, clusters) +
  Implication.
- `templates/research-tracker/decisions-INDEX.md` — one row per binding decision
  (ID | Decision | Date | Rationale | Constrains).

**Status machine** (documented in a new rule `.claude/rules/research-tracking.md`,
path-scoped to `research/**`):
`conjecture → testing → confirmed | rejected | complicated`, with the two hard rules:
(a) a hypothesis **cannot reach `confirmed` without a passing falsification insight**;
(b) first confirming evidence moves it only to `testing`. Parent status = worst child
status.

**New skill `.claude/skills/research-log/SKILL.md`** — `/research-log [conjecture|
insight|decide|status]`, adapted from his `INTERROGATION.md`:
- `conjecture`: 6 questions asked one at a time (estimand as a *named* quantity,
  population, variation, mechanism, falsification "what result kills this?"), then a
  one-sentence claim in the fixed grammar "[Population] experienced [direction]
  [outcome] due to [variation], identified by [design]" → assign ID → write file +
  INDEX row.
- `insight`: numbers mandatory; hypothesis link mandatory; script provenance required
  (integrates with our `scripts/R/` + `/data-analysis` conventions); applies the
  conservative status rule.
- `decide`: decision + what it constrains downstream; offer to propagate to CLAUDE.md
  Key Decisions table.
- `status`: counts by status, latest insight, next actions derived from statuses.

**Integration:** `/preregistration` output seeds initial hypotheses (add one
cross-reference line to that skill); CLAUDE.md "Current State: Research project"
variant points at `research/` as the tracker.

## Phase 3 — New epistemics skills

1. **`.claude/skills/blindspot/SKILL.md`** — port his 2×2 (Unexplained Feature /
   Convenient Absence / Unasked Question / Unexploited Strength) with the forcing
   function "list every visible feature before interpreting any"; mundane explanations
   (rounding, sample restriction, measurement) before substantive ones; "does N change
   across columns without explanation?"; CLEAR / CONDITIONAL / HOLD ruling. Trigger:
   output exists, interpretation about to happen (after `/data-analysis`, before
   writing results sections). Runs in-session (audits perception, not implementation —
   no isolation needed). Add to CLAUDE.md skills table.

2. **Replication audit** — new agent `.claude/agents/replication-auditor.md` + thin
   dispatch skill `.claude/skills/replication-audit/SKILL.md`. Adapted from his
   `personas/referee2.md`, scoped to our stack (R primary, Python as the replication
   language; drop Stata):
   - Launched as a subagent → fresh context = his "fresh terminal" isolation, free.
   - Capability table: MAY read + run author code, MAY create scripts only in
     `code/replication/`, MAY file reports in `quality_reports/replication_audits/`;
     FORBIDDEN to modify author code — report only.
   - Audits: code correctness (merge diagnostics, NA handling, variable construction),
     R↔Python replication of sample construction + final tables to 6 decimals with the
     heterogeneity taxonomy (package defaults vs. syntax error vs. numerical precision),
     replication-package readiness (/10 score; absolute paths = automatic failure),
     econometrics sanity (clustering level, bad controls, magnitude plausibility).
   - Scope-calibration table (paper = full intensity; exploration = code only).
   - Tools: Read, Grep, Glob, Bash, Write (Write constrained by prompt to the two
     directories above). Complements `r-reviewer` (style) — does not replace it.

3. **Bibliography verification** — extend `.claude/skills/validate-bib/SKILL.md` with a
   `--verify` deep mode (default behavior unchanged):
   - Timestamped run dir `quality_reports/bibcheck_<ts>/` (never clobber prior runs).
   - One parallel general-purpose agent per entry (batched ~10 at a time): find the
     canonical DOI/landing page via WebSearch/WebFetch, cross-check every field, test
     for field-mixing, return JSON (`status: clean|corrected|unverifiable`, issues,
     corrected entry).
   - Reviewer pass re-checks `unverifiable` and suspicious corrections; emits
     `corrected.bib` + report. **Never overwrite `Bibliography_base.bib`** (it's
     protect-files.sh-protected anyway) — user applies the diff.
   - Rationale to include in the skill: per-entry agents defeat attention decay
     ("first 10–15 entries get careful treatment, the next 60 get pattern-matched").

## Phase 4 — `/new-project` automation

- **`scripts/new_project.sh`** — automates the mechanical steps of
  `templates/new-project-checklist.md`: arg = project name → `cp -R` the template to a
  sibling dir (refuse if target exists) → `rm -rf .git && git init` →
  `git config core.hooksPath scripts/git-hooks` → delete template leftovers
  (session logs, plans, this plan file, reference decks) → print next manual steps
  (CLAUDE.md fields, Box folder, GitHub remote).
- **`.claude/skills/new-project/SKILL.md`** — wraps the script; asks for project name +
  slide style (teaching|academic), runs the script, then edits the new CLAUDE.md
  (project name, slide style, uncomment the right Current State variant), reminds about
  Box setup (per `.claude/rules/data-storage.md`) and the private-GitHub step.
- **`templates/new-project-checklist.md`** — add a short header: "Automated: run
  `/new-project` — this checklist remains the reference for what happens and the git
  primer." **Preserve the existing uncommitted edit in this file** (Step 1's
  DO-NOT-create-manually line).

## Phase 5 — Documentation sync + logging

- Add the 4 new/changed skills to CLAUDE.md's Skills Quick Reference
  (`/research-log`, `/blindspot`, `/replication-audit`, `/new-project`;
  `validate-bib --verify` note).
- MEMORY.md `[LEARN]` entries (see Phase 1.5) + one `[LEARN:workflow]` on
  falsification-gated status tracking.
- Session log per `.claude/rules/session-logging.md` →
  `quality_reports/session_logs/2026-08-19_mixtapetools-adoption.md`.
- Attribution line ("Adapted from Scott Cunningham's MixtapeTools, MIT-spirit
  credit + URL") at the top of each ported skill/agent.

## Not in scope (noted for later)

- **Dashboard server** — deferred by user decision; the file schema is
  dashboard-compatible if we add it later.
- **`/split-pdf`** — declined; `review-paper`'s 5-page chunking stays as is.
- **Stale-reference cleanup** (README counts wrong at "10 agents, 22 skills";
  `deep-audit` targets deleted `guide/workflow-guide.qmd`; dead `pdf-processing` rule
  scope; `sync_to_docs.sh` references in verification-protocol/verifier/settings).
  Discovered during this evaluation but independent — suggest as a separate session.

## Files touched (summary)

| Action | Paths |
|---|---|
| Edit | `CLAUDE.md`, `MEMORY.md`, `.claude/rules/orchestrator-protocol.md`, `.claude/rules/tikz-visual-quality.md`, `.claude/rules/verification-protocol.md`, `.claude/agents/tikz-reviewer.md`, `.claude/skills/compile-latex/SKILL.md`, `.claude/skills/validate-bib/SKILL.md`, `.claude/skills/preregistration/SKILL.md`, `templates/new-project-checklist.md` |
| Create | `.claude/rules/research-tracking.md`, `.claude/skills/research-log/SKILL.md`, `.claude/skills/blindspot/SKILL.md`, `.claude/skills/replication-audit/SKILL.md`, `.claude/skills/new-project/SKILL.md`, `.claude/agents/replication-auditor.md`, `scripts/new_project.sh`, `templates/research-tracker/*` (5 files), `research/.gitkeep`, session log |

## Verification

1. `bash -n scripts/new_project.sh`, then run it against a temp name in the scratchpad
   parent dir; confirm fresh git history, hooksPath set, leftovers removed; delete the
   test copy.
2. Dry-run `/research-log conjecture` on a toy hypothesis inside `explorations/`
   (fast-track rules apply there); confirm files + INDEX rows are created and the
   status machine rules are stated in output; remove test files.
3. Dry-run `/blindspot` on a small fabricated regression output; confirm the 4-quadrant
   report + ruling renders.
4. `/validate-bib` default mode on `Bibliography_base.bib` — confirm unchanged behavior;
   `--verify` smoke test on the 1-entry stub.
5. Skill frontmatter lint: each new SKILL.md has name/description/argument-hint;
   confirm they appear in the skills listing.
6. Quality gate: `python scripts/quality_score.py` is .tex/.qmd/.R-only, so for these
   markdown changes run `/proofread` mentality manually — re-read each edited file for
   internal consistency (CLAUDE.md table ↔ actual skills on disk).
7. Nothing in this plan touches `Bibliography_base.bib` or `settings.json`
   (protect-files.sh would block anyway).
