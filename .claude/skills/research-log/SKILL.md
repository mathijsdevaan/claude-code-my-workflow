---
name: research-log
description: File a research hypothesis, insight, or binding decision into the research/ tracker, or report tracker status. Use when the user states a new hypothesis or conjecture, reports a result worth keeping, makes an analysis decision, or asks where the project stands.
argument-hint: "[conjecture | insight | decide | status]"
allowed-tools: ["Read", "Write", "Edit", "Grep", "Glob", "Bash", "AskUserQuestion"]
---

# Research Log

Interrogation-driven filing into `research/`. Formats live in `templates/research-tracker/`; the status machine lives in
`.claude/rules/research-tracking.md` — its hard rules override anything else.

**Setup check (all modes):** if `research/hypotheses/` doesn't exist, create
`research/{hypotheses,insights,decisions}/` and copy the three INDEX templates
from `templates/research-tracker/` first.

If no mode argument is given, infer it from what the user just said (a guess
about the world → conjecture; a number from analysis → insight; a spec choice
→ decide) and confirm the inference in one line.

## /research-log conjecture

Ask these questions ONE AT A TIME — wait for each answer. If an answer is
vague, use the follow-up before moving on.

1. **Estimand** — a NAMED quantity (ATT, ATE, LATE, elasticity, proportion),
   not "the effect of X on Y". *Follow-up if vague:* "Is this the average
   effect on the treated, or on everyone? What units?"
2. **Population** — who, where, when, at what unit of analysis.
3. **Variation** — what varies, at what level, and why it's plausibly
   exogenous. *Follow-up:* "Who chose this, and what determined the timing?"
4. **Mechanism** — the story that would generate the effect. *Follow-up:*
   "What would we observe in the data if this mechanism is the one operating?"
5. **Falsification** — "What specific result would kill this?" Must be
   concrete. *Follow-up:* "If your design is valid, what should we see in a
   period or group with no treatment?"
6. **Parent** — is this a child of an existing hypothesis? (Check
   `research/hypotheses/INDEX.md`.)

Then:
- Propose ONE sentence in the fixed grammar: *"[Population] experienced
  [direction] [outcome] due to [variation], identified by [design]."* Get
  approval.
- Assign the next ID (H01, H02…; children H01a, H01b…).
- Write `research/hypotheses/HXX_slug.md` from `templates/research-tracker/H00_example.md`
  with status `conjecture`, and add the INDEX entry.
- Close with: "**Kills it:** [the falsification condition]. Next: [the script
  that would test this]."
- If `preregistration/preregistration.md` exists, offer to seed hypotheses
  from its hypotheses section instead of starting blank.

## /research-log insight

1. **Numbers are mandatory.** Not "we found an effect" but "ATT = 2.3pp
   (SE = 0.8, 95% CI [0.7, 3.9], p = 0.004, N = 847)". If the user has no
   numbers, ask for them or go read the output.
2. **Hypothesis link is mandatory.** Which HXX does this update? If none
   fits, file the conjecture first.
3. **Script provenance is mandatory.** The `script:` path must exist (usually
   `scripts/R/…`). If it doesn't: "Is this from an ad-hoc analysis? Create the
   script first, then file."
4. Classify the result: `confirmed` / `rejected` / `complicated` evidence.
5. Write `research/insights/YYYY-MM-DD_slug.md` from the template; add the
   INDEX row (most recent first); append the evidence link to the hypothesis
   file; update the hypothesis status **conservatively**:
   - First confirming evidence → `testing`, NOT `confirmed` (needs falsification)
   - `confirmed` only if a passing falsification insight exists for this
     hypothesis
   - Falsification fails → `complicated`, and say so plainly
   - Propagate: parent status = worst child status
6. Report the status change and what would move it next.

## /research-log decide

1. State the decision **specifically** — "Cluster SEs at the team level", not
   "we should probably cluster".
2. Record the rationale (one or two sentences, including alternatives rejected).
3. Ask: what does this **constrain downstream**? (Which scripts, tables,
   hypotheses inherit it.)
4. Add the row to `research/decisions/INDEX.md` (next D-ID).
5. If the decision changes how Claude should work every session (estimator,
   sample rule, clustering), offer to mirror it into CLAUDE.md's
   "Key Decisions Made" table.

## /research-log status

Report four things, briefly:
1. Hypothesis counts by status (and any parent whose status is stale relative
   to its children — fix per the worst-child rule).
2. Latest insight (date + one-line finding).
3. Integrity check: INDEX rows ↔ files match; every `confirmed` hypothesis has
   a passing falsification insight (flag violations loudly).
4. Next actions derived from statuses: `conjecture` → write the test script;
   `testing` → run falsification; `complicated` → the named resolution.

## What this skill does NOT do

- Run analyses or write analysis code (that's `/data-analysis`).
- Move a hypothesis to `confirmed` as a courtesy. The falsification gate is
  the point.
- Edit `research/` files outside the formats above.
