---
name: rct-toolkit
description: Generate a standard R analysis script for RCT data. Produces balance tables, power check at realized N, ITT estimates with fixest + modelsummary, LATE if non-compliance, attrition check, and pre-specified heterogeneous effects. Uses data.table as backbone. Clusters SEs at user-specified main unit of analysis.
argument-hint: "[path to clean data file, or 'new' to scaffold without data]"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Bash", "AskUserQuestion"]
---

# RCT Analysis Toolkit

Generate a standard R analysis script tailored to the user's RCT. Uses `fixest` + `modelsummary` + `data.table` + camelCase variables.

**Input:** `$ARGUMENTS` — path to a clean data file, or `new` to scaffold without reading data.

**Output:**
- `code/rct_analysis.R` — full analysis script
- `code/rct_analysis.log` — output log (after running)
- `output/tables/` — Markdown + LaTeX tables
- `output/figures/` — effect plots (optional)

---

## Steps

### 1. Gather study parameters

Ask the user, one at a time:

1. **Unit of randomization.** Individual? Team? Org? Geographic market?
2. **Main unit of analysis.** (Cluster level for SEs — may differ from #1 if there are nested levels.)
3. **Treatment variable name** in the dataset.
4. **Primary outcome(s).** Names in the dataset.
5. **Pre-specified covariates** (from preregistration, if it exists).
6. **Pre-specified subgroups** for heterogeneous effects (from preregistration).
7. **Is there non-compliance?** (Will we need LATE in addition to ITT?)
8. **Is there attrition?** (Do we need an attrition model?)
9. **Block / strata variable**, if randomization was stratified.

If a `preregistration/preregistration.md` file exists in the project, READ IT FIRST and pre-fill as many answers as possible. Only ask about the parts the preregistration doesn't specify.

### 2. Peek at the data (if `$ARGUMENTS` is a data path)

- Load a sample with `data.table::fread`
- Report: column names, N rows, treatment assignment balance (counts)
- Verify the treatment variable and outcomes from step 1 actually exist

If columns are missing, stop and ask the user to clarify variable names.

### 3. Generate the analysis script

Write `code/rct_analysis.R` with the following structure. Use **camelCase** throughout. Use **`data.table`** for manipulation. Use **`fixest::feols`** for regressions. Use **`modelsummary`** for tables.

```r
# code/rct_analysis.R
# RCT analysis for [STUDY NAME]
# Generated [YYYY-MM-DD] by rct-toolkit skill

library(data.table)
library(fixest)
library(modelsummary)

# ---- 0. Load data ----
dat <- fread("[DATA PATH]")

# ---- 1. Sample construction ----
# Apply pre-registered exclusions
dat <- dat[exclusionCriterion1 == FALSE]
dat <- dat[!is.na(treatmentVar)]

# ---- 2. Balance table ----
balanceVars <- c("[covariate list from step 1]")
balance <- dat[, lapply(.SD, mean, na.rm = TRUE),
               by = treatmentVar,
               .SDcols = balanceVars]
# Include t-tests / F-tests for joint balance
# Use modelsummary::datasummary_balance for a publication-ready version
datasummary_balance(
  ~ treatmentVar,
  data = dat[, .SD, .SDcols = c("treatmentVar", balanceVars)],
  output = "output/tables/balance.md"
)

# ---- 3. Power check at realized N ----
# Rough MDE at observed N, assuming 80% power, alpha = 0.05
library(pwr)
nTreat <- sum(dat[[treatmentVar]] == 1)
nControl <- sum(dat[[treatmentVar]] == 0)
pwr.t2n.test(n1 = nTreat, n2 = nControl, power = 0.8, sig.level = 0.05)

# ---- 4. Main ITT estimates ----
# Baseline
m1 <- feols(outcomeVar ~ treatmentVar, data = dat,
            cluster = ~ clusterVar)

# With covariates
m2 <- feols(outcomeVar ~ treatmentVar + cov1 + cov2,
            data = dat, cluster = ~ clusterVar)

# With block fixed effects (if stratified)
m3 <- feols(outcomeVar ~ treatmentVar + cov1 + cov2 | blockVar,
            data = dat, cluster = ~ clusterVar)

modelsummary(
  list("Baseline" = m1, "+Controls" = m2, "+Block FE" = m3),
  stars = c("*" = .1, "**" = .05, "***" = .01),
  gof_omit = "AIC|BIC|R2 Adj|R2 Within|RMSE",
  output = "output/tables/main_itt.md"
)

# ---- 5. LATE (if non-compliance) ----
# First stage
fs <- feols(takeUp ~ treatmentVar + cov1 + cov2, data = dat,
            cluster = ~ clusterVar)
# 2SLS
late <- feols(outcomeVar ~ cov1 + cov2 | 0 | takeUp ~ treatmentVar,
              data = dat, cluster = ~ clusterVar)

# ---- 6. Attrition check ----
# If attrition is a concern, test whether attrition is balanced across arms
attritionMod <- feols(attrited ~ treatmentVar + cov1 + cov2,
                      data = dat, cluster = ~ clusterVar)

# ---- 7. Heterogeneous effects (pre-specified only) ----
# Interaction with pre-specified subgroup variable
m_het <- feols(outcomeVar ~ treatmentVar * subgroupVar + cov1 + cov2,
               data = dat, cluster = ~ clusterVar)

# ---- 8. Robustness (pre-registered) ----
# [Add robustness checks from preregistration here]

# ---- 9. Save session info for replication ----
sessionInfo()
```

Adjust the template based on the user's answers: drop sections not relevant (e.g., if no non-compliance, drop LATE), adapt variable names, include pre-specified subgroups.

### 4. Flag what's NOT in the script

At the end of the file, add a comment block listing:
- Pre-registered analyses that ARE in the script
- Pre-registered analyses NOT YET included (flag for manual add)
- Exploratory analyses to do separately with clear flagging in results

### 5. Save a brief README

`code/README.md` — one-page description of what the script does, what inputs it expects, what it produces, and how to reproduce (order of scripts, seed, R package versions).

---

## Important Rules

1. **Use the user's conventions.** fixest, modelsummary, data.table, camelCase. Don't switch to tidyverse or stargazer without asking.
2. **Cluster SEs correctly.** Always at the user-specified main unit of analysis, which may differ from unit of randomization.
3. **Pre-register separation.** If `preregistration/preregistration.md` exists, clearly separate pre-specified analyses from exploratory ones in the script.
4. **Never fabricate results.** If you can't run the script, say so — don't pretend numbers.
5. **Keep the skeleton clean.** It's a starting point, not a full analysis. The user fills in the details.
6. **Default to ITT.** LATE only if non-compliance was flagged. Baseline before heterogeneity before robustness.
