---
name: preregistration
description: Scaffold an aspredicted.org-format preregistration for a new RCT or observational study. Walks through hypotheses, outcomes, sample size, and analysis plan. Produces a markdown preregistration doc ready to paste into aspredicted.org, plus an R code skeleton implementing the analysis plan.
argument-hint: "[short study name or research question]"
allowed-tools: ["Read", "Grep", "Glob", "Write", "AskUserQuestion"]
---

# Preregistration Scaffold (aspredicted.org format)

Walk the user through filling out an aspredicted.org-style preregistration. Produce a markdown document and an R code skeleton.

**Input:** `$ARGUMENTS` — a short study name or research question.

**Output:**
- `preregistration/preregistration.md` — ready to paste into aspredicted.org
- `preregistration/analysis_plan.R` — skeleton implementing the analysis plan

---

## Steps

1. **Determine study type.** Ask if this is an RCT, an observational study, or a secondary analysis of existing data. Different aspredicted fields apply.

2. **Walk through the aspredicted fields, one at a time.** Do NOT batch these questions — ask them one by one and let the user think through each.

   **The 8 aspredicted fields (RCT version):**

   1. **Have any data been collected for this study already?** (yes/no, with context)
   2. **What's the main question being asked or hypothesis being tested in this study?**
   3. **Describe the key dependent variable(s) specifying how they will be measured.**
   4. **How many and which conditions will participants be assigned to?**
   5. **Specify exactly which analyses you will conduct to examine the main question/hypothesis.**
   6. **Describe exactly how outliers will be defined and handled, and your precise rule(s) for excluding observations.**
   7. **How many observations will be collected or what will determine sample size? No need to justify decision, but be precise about exactly how the number will be determined.**
   8. **Anything else you would like to pre-register?** (e.g., secondary analyses, exploratory hypotheses, robustness checks)

   **For observational studies:** adapt fields 1, 4, 7 to describe data acquisition, analytical sample definition, and estimation sample.

3. **Quality checks as you go.** For each answer, verify:

   - **Hypotheses are falsifiable.** "X will affect Y" is vague. "X will increase Y by at least 5%" or "X will increase Y, estimated via OLS of Y on X with covariates Z, p<0.05 two-sided" is pre-committed.
   - **Hypotheses are not derivable from the data.** If the user has already peeked at the data, flag this — aspredicted specifically asks.
   - **Outcome measures are specified, not just named.** "Promotion" is not an outcome; "indicator = 1 if employee moves up at least one grade level within 24 months, measured from personnel records as of Dec 31" is.
   - **Analysis plan is specific enough to run.** Not "we'll use regression" — but which estimator, which controls, which standard errors, which sample.
   - **Sample size rule is concrete.** Either a target N with power calc, or a stopping rule, or "all available observations meeting criteria X."

   When you catch vagueness, point it out and ask the user to sharpen.

4. **Generate the markdown preregistration file.** Layout matches aspredicted.org's 8 fields so the user can paste each section into the corresponding form field.

5. **Generate the R code skeleton.** Translate the analysis plan into a runnable `.R` file with:
   - Data loading placeholder
   - Sample construction (exclusions from field 6)
   - Balance checks (for RCTs)
   - Main analysis using `fixest::feols` with `data.table`
   - `modelsummary` table output
   - Standard errors clustered at the user-specified main unit of analysis

   Use **camelCase** for variable names.

6. **Flag what's NOT preregistered.** Add a section to the markdown doc titled "Exploratory analyses not pre-registered" — explicitly listing any analysis the user wants to do but can't pre-specify. This protects them in review.

---

## Report Format

`preregistration/preregistration.md`:

```markdown
# Preregistration: [Study Name]

**Platform:** aspredicted.org
**Date:** [YYYY-MM-DD]
**Study type:** [RCT / Observational / Secondary data analysis]

## 1. Data collection status
[Answer]

## 2. Main hypothesis
[Answer]

## 3. Dependent variable(s)
[Answer]

## 4. Conditions / treatment assignment
[Answer]

## 5. Analyses
[Answer — specific enough that someone else could run it]

## 6. Outliers and exclusions
[Answer]

## 7. Sample size
[Answer — concrete rule]

## 8. Other pre-registered items
[Answer]

---

## Exploratory analyses NOT pre-registered

These are planned but not pre-committed. When reported, they should be flagged as exploratory.

- [List]
```

---

## Important Rules

1. **Ask one question at a time.** Do not batch — preregistration is a thinking exercise, not a form-filling one.
2. **Push back on vagueness.** Your main job is catching pre-registrations that won't constrain the author's future claims.
3. **Generate the code skeleton AFTER the markdown is complete.** Skeleton must match the analysis plan exactly.
4. **Do not pre-register analyses the user hasn't thought through.** If they can't describe it precisely, it goes in the exploratory section.
5. **Respect the format.** aspredicted.org has a specific 8-field structure — preserve it.
