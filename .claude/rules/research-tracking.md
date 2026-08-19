---
paths:
  - "research/**"
---

# Research Tracking: Hypotheses, Insights, Decisions

Adapted from Scott Cunningham's MixtapeTools GTD harness
(https://github.com/scunning1975/MixtapeTools).

**The tracker is the project's evidentiary memory.** Findings don't exist until
filed. File through `/research-log`, which enforces the formats in
`templates/research-tracker/`.

## Layout

```
research/
├── hypotheses/INDEX.md      # hierarchical DAG, status inline
├── hypotheses/HXX_slug.md   # claim + courtroom + Kills It + evidence links
├── insights/INDEX.md        # table, most recent first
├── insights/YYYY-MM-DD_slug.md
└── decisions/INDEX.md       # binding decisions table
```

## The status machine

```
conjecture → testing        first evidence or first test script assigned
testing   → confirmed       positive evidence AND falsification passes
testing   → rejected        evidence contradicts AND falsification confirms the negative
testing   → complicated     evidence mixed OR falsification fails
complicated → confirmed | rejected   (not terminal — resolve it)
```

**Hard rules (never soften these):**

1. A hypothesis CANNOT reach `confirmed` without a passing falsification
   insight. The falsifiers ("Kills It") must be written BEFORE the test runs.
2. First confirming evidence moves a hypothesis only to `testing`, never
   straight to `confirmed`.
3. Parent hypothesis status = worst child status.
4. Insights require numbers (estimate, SE, CI, p, N) and script provenance —
   a script path that exists. Ad-hoc console results are not filed; create the
   script first.
5. `conjecture → rejected` directly is allowed (killed by theory or data
   availability before testing).

## Claude's behavior in this directory

- Never edit hypothesis statuses without evidence filed in `insights/`.
- Keep INDEX files in sync with the individual files — every file has an INDEX
  row, every INDEX row has a file.
- Drift check: citing a `complicated` or `testing` hypothesis as established
  in paper/slide prose is drift. (This rule only loads for `research/**` files,
  so the drift check is also mirrored in CLAUDE.md's research variant, which is
  always in context — that copy is the one that fires while writing prose.)
- Mirror binding decisions that change how Claude works (estimator, clustering,
  sample rules) into CLAUDE.md's "Key Decisions Made" table.
