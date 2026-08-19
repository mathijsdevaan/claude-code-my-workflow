---
name: blindspot
description: Peripheral-vision audit of empirical output before interpretation. Finds problems hiding in plain sight (unexplained features, convenient absences) and overlooked opportunities (unasked questions, unexploited strengths). Use when a figure, table, or set of results exists and interpretation or writing is about to happen.
allowed-tools: ["Read", "Bash", "Glob", "Grep"]
argument-hint: "[path to figure/table/results] [what you think the main finding is]"
---

# Blindspot: Make the Stone Stony Again

The frame comes from Viktor Shklovsky's defamiliarization — art exists to make
the stone stony again — applied to empirical research: see your own output as
a stranger would, before the story you want to tell automates your perception.

By the time you've spent months on a project, the main finding has collapsed
your attention. Everything else in the output — the spike at t=1, the missing
subgroup, the heterogeneity richer than the average — has become invisible. Not
because it's hidden, but because you stopped looking.

This skill audits your **perception** of your own output, not your code
(that's `/replication-audit`). It runs in-session — auditing perception needs
no isolation; auditing implementation does.

**Timing:** output exists, interpretation is about to happen. After
`/data-analysis` produces results; before results sections, slides, or emails
to coauthors. Do not invoke after the writing is done.

---

## The Blindspot Grid

Work through all four quadrants IN ORDER. Mark each finding **DONE** or
**FLAG** (no clean explanation yet).

|  | What's there but unseen | What's absent but unnoticed |
|---|---|---|
| **Problems** | Vice 1: The Unexplained Feature | Vice 2: The Convenient Absence |
| **Opportunities** | Virtue 1: The Unasked Question | Virtue 2: The Unexploited Strength |

## Vice 1: The Unexplained Feature

1. **List every visible feature of the output BEFORE interpreting any of
   them.** Every coefficient and sign, every spike or discontinuity, every
   pattern across columns, every sample size, every number. The main finding
   is just one item on this list.
2. **For each feature: what would generate this?** Work the mundane
   explanations first — rounding/discretization artifact, sample restriction,
   measurement issue, small-N coincidence — before substantive ones. "That's
   just noise" requires justification, not assertion.
3. **Name the single hardest feature to explain under the preferred
   interpretation.** Attempt to explain it. If you can't: say so, state what
   would resolve it, mark it FLAG.

Rule: if you can't explain every feature, you don't yet understand your output.

## Vice 2: The Convenient Absence

1. **What would a hostile referee demand to see?** Which essential robustness
   checks, falsification tests, and spec variants are missing?
2. **What subgroups were never examined?** Natural splits (tenure, gender,
   team, network position, region, period, treatment intensity) that should be
   in the table but aren't.
3. **What was dropped without comment?** Trimmed observations, excluded
   periods, covariates that quietly disappeared between drafts.
4. **Does N change across columns without explanation?** Almost never random —
   it traces to a decision, often an undocumented one.

Rule: if something should be there and isn't, that is a finding.

## Virtue 1: The Unasked Question

1. Is the average effect hiding a more interesting heterogeneity pattern —
   one that says *why* the treatment works?
2. Is there mechanism evidence — a *how*, not just a *that*? Do intermediate
   outcomes move?
3. Are the descriptives or a secondary outcome more interesting than the main
   regression?
4. **Is there a paper inside this paper?** Is the author reporting the
   second-most-interesting thing in their data?

## Virtue 2: The Unexploited Strength

1. Is the identification stronger than argued? Variation left on the table?
2. Is there a cheap falsification test that would crush the main objection —
   a placebo outcome, placebo group, or window where the effect must be zero?
3. Are descriptives undersold — would one figure land the argument better than
   the table?
4. Is the paper positioned too narrowly for the literature it speaks to?

---

## The Report

```
## Blindspot Report
**Output:** [what was audited]
**Date:** YYYY-MM-DD

### Vice 1: Unexplained Feature
- Features listed: [count] | Hardest to explain: [it] | Resolved? [yes/FLAG]
### Vice 2: Convenient Absence
- Missing checks: [...] | Missing subgroups: [...] | Unexplained N changes: [...]
### Virtue 1: Unasked Question
- Heterogeneity / mechanism / secondary findings worth pursuing: [...]
### Virtue 2: Unexploited Strength
- Undersold design features / unused falsification tests: [...]

### Ruling
[ ] CLEAR — proceed to interpretation; virtues noted.
[ ] CONDITIONAL — proceed, but acknowledge the open questions explicitly.
[ ] HOLD — do not interpret or publish until flagged vices are resolved.
```

Save the report to `quality_reports/blindspot_[output-name]_[date].md` when the
output audited is bound for a paper or deck; otherwise report inline.

## Integration

- If a FLAG concerns a hypothesis tracked in `research/`, note it in the
  relevant hypothesis file and set status `complicated` if the vice undermines
  filed evidence (per `.claude/rules/research-tracking.md`).
- A Virtue 1 finding worth pursuing → file it via `/research-log conjecture`.
