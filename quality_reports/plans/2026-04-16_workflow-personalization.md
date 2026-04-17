# Plan: Personalize Forked Workflow for Research + Teaching

**Status:** DRAFT (Parts 1, 2a, 2b approved in session; Parts 2c, 3, 4 pending)
**Date:** 2026-04-16

## Context

Forked from Pedro Sant'Anna's template (built for econometrics PhD teaching). User is UC Berkeley Haas professor doing:
- **Research (dominant):** quantitative, observational admin data + within-org RCTs
- **Teaching:** exec ed 1–2x/month + 8-week MBA block Aug–Oct
- Solo workflow

**Framing:** this repo is the TEMPLATE. Every new project (research / MBA / exec ed) starts by copying it.

Goal of this plan: trim dead weight, finish half-done setup, add research-side tools, and make slide styling automatic per project type.

---

## Part 1: Remove what you won't use — APPROVED

- Delete `master_supporting_docs/` (legacy, nearly empty). *Note: currently holds the reference deck `Hospital_management_MRL (2).pdf`. Move it elsewhere first — e.g., to `Figures/references/` or a new `references/` folder — before deleting.*
- Delete `guide/` source (keep compiled `docs/workflow-guide.html`)

---

## Part 2a: Clean up CLAUDE.md — APPROVED

- Replace `[YOUR PROJECT NAME]` with self-explanatory placeholder: `[Project name — replace when copying this template for a new project]`
- Replace "Current Project State" lecture table with three commented-out variants (research project / MBA course / exec ed session) for customization at project start
- Delete "Quarto CSS Classes" empty table (Quarto being dropped — see below)
- Update "Academic Presentations" subsection to reference the two-theme system (see Part 2b)

---

## Part 2b: Two-theme slide system (teaching + academic) — APPROVED

**The mechanism:** each project's `CLAUDE.md` declares one line near the top:

```markdown
**Slide style:** academic
```

(or `teaching`). Claude reads it at session start, applies the matching theme + rule automatically.

**Template provides both options:**

1. **Rename:** `Preambles/beamerthemeUCBerkeley.sty` → `Preambles/beamerthemeUCBerkeleyTeaching.sty`
2. **Rename:** `.claude/rules/exec-ed-slides.md` → `.claude/rules/teaching-slides.md` — broaden content to cover both exec ed and MBA conventions
3. **Create:** `Preambles/beamerthemeUCBerkeleyAcademic.sty` — extracted from the working preview at `/tmp/academic-v2/preview.tex`. Approximates the La Forgia/Paris/Shi reference deck:
   - Metropolis-based with heavy customization
   - Dark red frame-title bars (`#A12830`)
   - Charcoal 3-column footer (author | title | page)
   - Minimal section dividers with olive rule
   - Sans-serif throughout, inline gray citations
4. **Create:** `.claude/rules/academic-slides.md` — triggers on `**Slide style:** academic`; specifies academic deck conventions (motivation → literature → data → identification → results → robustness), citation format, density norms
5. **Update CLAUDE.md template:** add `**Slide style:** [teaching | academic — pick one when starting a new project]` declaration near the top
6. **Install missing fonts** (affects both themes — current setup can't render body text):
   - **Open Sans** (for teaching theme) — free from Google Fonts
   - **Fira Sans** (for academic theme) — free from Google Fonts
7. **Restore or recreate `UCBerkeley_wordmark_white`** — the logo file is missing from `Preambles/` (or wherever it should live). Required by teaching theme footer.
8. **Fix teaching theme footer overlap bug** — discovered in preview: slide content can run into the blue diagonal footer. Low-priority; address when it bites in a real deck.

---

## Part 2c: Check `.claude/settings.local.json` — PENDING

Contains a restriction that effectively whitelists only the `commit` skill. Every other skill invocation hits a permission prompt. Probably accidental. Decision needed: remove the restriction, or confirm intentional.

---

## Part 3: Research-side skills — APPROVED

All 5 items walked through and approved with user conventions captured.

### 3a. `preregistration` skill

Scaffolds aspredicted.org-format preregistration (user preference: aspredicted over OSF). Hypotheses → analysis plan → R code skeleton. Skill checks hypotheses are falsifiable and pre-committed, flags ambiguous language. Output: markdown preregistration doc + skeleton `.R` file.

### 3b. `rct-toolkit` skill — conventions captured

R analysis starter for RCT data. Produces: balance table, power check at realized N, ITT + controls + FE estimates, LATE via IV if non-compliance, attrition check, heterogeneous effects on pre-specified subgroups. Publication-ready tables.

**User's R conventions (use these when building):**
- Cluster level for SEs: **depends on study — whatever the main unit of analysis is** (skill should ask at invocation)
- Table package: **modelsummary**
- Regression library: **fixest** (`feols`)
- Variable naming: **camelCase**
- Data backbone: **data.table**

### 3c. `revise-resubmit` skill

R&R response tracker: reviewer comment → planned response → manuscript location. Status tracking (OPEN / IN PROGRESS / DONE). Generates formal response document and cover letter at resubmission.

**User preference:** final output as **PDF**.

### 3d. Customize `domain-reviewer` agent — 5 lenses finalized

Replace generic template with these 5 lenses (in order of priority — first two fire first):

1. **Theoretical coherence** — argument developed systematically, core constructs defined and used consistently, mechanisms match scope conditions, right theoretical traditions engaged
2. **Front-end / back-end alignment** — does intro promise match empirics? Are theorized hypotheses the same as tested ones? Do claimed contributions match what results support?
3. **Identification clarity** — RCT (spillover, attrition, non-compliance, SUTVA) or observational (selection, reverse causality, omitted variables). Is identifying variation clearly stated and defended?
4. **Effect size interpretation** — practical vs. statistical significance, overselling, honest framing
5. **Mechanism evidence** — how, not just whether. Is a specific mechanism proposed? Does the empirical strategy test it directly or only the reduced-form effect? Are alternatives ruled out? Does the data's variation structure distinguish competing mechanisms, or are they observationally equivalent? If heterogeneous effects are used as mechanism evidence, is that inference justified?

Lens 1 and 2 reflect user's self-identified sociologist's priorities; lens 5 replaces the earlier "preregistration deviation" lens (too narrow — RCT-only bookkeeping).

### 3e. Pre-commit large-file guard hook

Blocks `git commit` before push for:
- Files > 50 MB
- `.RData`, `.rds`, `.dta` (any size — almost always analysis data)
- `.csv` > 10 MB

Override via `git commit --no-verify` when legitimately needed.

**Deferred / skipped:**
- Qualitative coding helper — user doesn't do qualitative work
- Social network analysis workflow — user didn't flag as priority
- Manuscript-formatter for specific journals — defer until target journals are stable

---

## Part 4: Productivity observations — PENDING (4a APPROVED)

### 4a. Template vs project repos — APPROVED

Keep `Claude Setup/` as a clean template. Start each new project (research / MBA / exec ed) by copying the folder to a new location with its own git history. Template stays lean and evolvable; past projects stay frozen and stable.

**Deliverable: `templates/new-project-checklist.md`** — beginner-friendly walkthrough covering:
- Why the procedure exists (brief git primer for someone new to git)
- Step 1: copy the template folder (`cp -R`)
- Step 2: start fresh git history (`rm -rf .git && git init`) with explanation of *why* fresh history is wanted
- Step 3: customize `CLAUDE.md` — project name, Current State variant, `**Slide style:**` declaration
- Step 4: clean template leftovers (delete template's session logs and plans)
- Step 5: first commit (`git add .` + `git commit -m "..."`)
- Step 6 (optional, deferred): push to GitHub — points to future `templates/git-github-setup.md` (not written yet)
- **Day-to-day workflow section**: periodic `git add . && git commit -m "..."` rhythm with example messages
- **When things go wrong section**: `git status`, `git log --oneline -10`, `git checkout -- file` for basic recovery

Explicitly scoped to **solo research workflow** — no branches, merges, PRs, rebasing. Extend later if coauthors join.

Full draft content captured in session transcript; write to file when executing this plan.

### 4b. Drop Quarto infrastructure entirely

User decision from earlier in session. Removes: `Quarto/` folder, 4 skills (`translate-to-quarto`, `qa-quarto`, `deploy`, `extract-tikz`), 3 agents (`quarto-critic`, `quarto-fixer`, `beamer-translator`), 1 rule (`beamer-quarto-sync.md`), 1 script (`scripts/sync_to_docs.sh`). Git history preserves all of it. Skills: 22 → 18.

### 4c. Personal memory file — DROPPED

User decision: not needed for now.

### 4d. Session-log hook fix — DROPPED

User decision: leave the hook as-is. False-alarm messages can be ignored. Revisit if it becomes genuinely disruptive.

---

## Suggested execution order

Small independent steps — stop at any point.

1. Move reference deck out of `master_supporting_docs/`, then delete `master_supporting_docs/` and `guide/` source
2. Clean up CLAUDE.md placeholders (Part 2a)
3. Drop Quarto infrastructure (Part 4.1)
4. Check `settings.local.json` (Part 2c) — 30-second task
5. Install missing fonts; restore wordmark logo (Part 2b items 6 + 7)
6. Build two-theme system: rename existing theme+rule, build academic counterparts (Part 2b items 1–5)
7. Customize `domain-reviewer` (Part 3.4)
8. Add large-file commit hook (Part 3.5)
9. Build Tier-1 research skills: `preregistration`, `rct-toolkit`, `revise-resubmit` (Part 3.1–3.3)
10. Seed personal-memory.md (Part 4.2)
11. Fix session-log hook or document workaround (Part 4.3)

---

## Files that will be modified when executed

- `CLAUDE.md` — placeholders, slide-style declaration, Current State variants
- `Preambles/beamerthemeUCBerkeley.sty` → renamed to `beamerthemeUCBerkeleyTeaching.sty`
- `Preambles/beamerthemeUCBerkeleyAcademic.sty` — new
- `Preambles/UCBerkeley_wordmark_white.{png,pdf}` — restored
- `.claude/rules/exec-ed-slides.md` → renamed to `teaching-slides.md`, broadened
- `.claude/rules/academic-slides.md` — new
- `.claude/agents/domain-reviewer.md` — field customization
- `.claude/hooks/pre-commit-large-file-guard.sh` — new
- `.claude/hooks/log-reminder.py` — bug fix (optional)
- `.claude/settings.local.json` — review/loosen
- `.claude/state/personal-memory.md` — new
- `.claude/skills/{preregistration,rct-toolkit,revise-resubmit}/SKILL.md` — new
- **Deletions:** `master_supporting_docs/` (after moving reference deck), `guide/` source, `Quarto/`, 4 Quarto skills, 3 Quarto agents, `beamer-quarto-sync.md`, `sync_to_docs.sh`

---

## Verification after each step

- File deletions: `git status` + file count drop
- Theme builds: compile preview `.tex` with new `.sty`, visually inspect rendered PDF
- Skill additions: invoke `/skill-name` on a trivial test case, confirm sensible output
- Hook addition: try to commit a dummy 100MB file to a test branch — should be blocked
- CLAUDE.md changes: start a fresh session, confirm no leftover `[YOUR ...]` placeholders in context dump

---

## Open questions for Part 3 when we get there

1. Target journals you submit to most often? (Affects manuscript-formatter scope if we build it.)
2. R conventions for `rct-toolkit`: cluster-SE level, table package (modelsummary / stargazer / fixest tables), preferred control structure.
