# Architecture Decisions

A record of decisions made when personalizing this template. Each entry
captures the decision, what was considered and rejected, the consequences
(good and bad), and where to look if the decision is ever revisited.

Format inspired by ADR (architecture decision records). New decisions go
at the top; do not rewrite past entries — append corrections as new entries.

---

## 2026-04-16: Template-vs-project repo separation

**Decision:** This repo is **only** a template. Each research project,
MBA course, or exec-ed session gets its own repo, created by copying this
folder and running `rm -rf .git && git init`. The template itself stays
lean and free of any specific project's state.

**Alternatives considered:**
- One repo for everything (template + active work): rejected — project-
  specific plans, logs, and data conventions would pollute the template.
- Submodules or symlinks from projects back to the template: rejected —
  too much mechanism for a solo researcher; updates are manual anyway.

**Consequences:**
- Template improvements don't auto-propagate to past projects. Each project
  is frozen at copy time (this is fine for research; reproducibility matters).
- `templates/new-project-checklist.md` documents the copy procedure.
- Git history stays meaningful per-project.

**If revisiting:** If coauthors or RAs join regularly, consider a shared
"template repo + per-project project repos that pull from it" pattern with
real submodules. For solo work, copy-and-diverge is simpler.

---

## 2026-04-16: Two-theme Beamer system (teaching + academic)

**Decision:** Two separate Beamer themes, each with its own rule file,
activated by `**Slide style:** [teaching | academic]` declaration near the
top of CLAUDE.md.

- Teaching: `Preambles/beamerthemeUCBerkeleyTeaching.sty` + `.claude/rules/teaching-slides.md`
- Academic: `Preambles/UCBerkeleyAcademic.sty` + `.claude/rules/academic-slides.md`

**Alternatives considered:**
- Single theme with runtime options (e.g., `\usetheme[academic]{...}`):
  rejected — visual and content conventions differ too much; one file would
  be complex to maintain.
- One theme, two rule files: rejected — rule changes alone can't produce
  the visual distinction user wanted (dark red bars vs. Berkeley Blue/Gold).

**Consequences:**
- Two `.sty` files to update when Berkeley's brand guidelines change.
- Requires Fira Sans (academic) and Open Sans (teaching) installed; see
  `templates/manual-setup-steps.md`.
- The `**Slide style:**` declaration in CLAUDE.md is authoritative —
  Claude reads it at session start.

**If revisiting:** If the academic theme identity changes substantially,
the underlying Metropolis base can be swapped for another minimalist theme
(e.g., `simple`, `boxes`). The `UCBerkeleyAcademic.sty` customization on
top would mostly transfer.

---

## 2026-04-16: Academic theme visual design (no red bar, red rule instead)

**Decision:** Frame titles are bold black text on white with a thin red
underline (0.6pt, AccentRed `#A12830`) spanning the full slide width.
Section dividers use an olive-colored rule (`#9B8B5A`). Footer is a
charcoal 3-column bar (`#3F3F3F`) showing author | title | page.

**Alternatives considered:**
- Red fill bar with white text (matching reference deck exactly): rejected
  by user — "I don't like the red bar up top."
- Dark red title text with red underline: deferred — cleaner but less visual
  separation from body.
- No color at all: rejected — loses the identity marker the user wanted.

**Consequences:**
- Distinctive-looking without being heavy; suits seminar audiences.
- The red rule may appear subtle at small zoom levels — verified the color
  is actually `#A12830`, not black.
- `\titleslide{title}{authors}{venue}` macro required because
  `\maketitle` under Metropolis mangles multi-author layouts.

**If revisiting:** The thickness and color of the rule are one-line changes
in `UCBerkeleyAcademic.sty`. Easier than reshuffling the whole theme.

---

## 2026-04-16: Dropped Quarto infrastructure

**Decision:** Removed Quarto entirely. Deleted `Quarto/` folder, 4 skills
(`translate-to-quarto`, `qa-quarto`, `deploy`, `extract-tikz`), 3 agents
(`quarto-critic`, `quarto-fixer`, `beamer-translator`), 1 rule
(`beamer-quarto-sync.md`), and 1 script (`sync_to_docs.sh`). Reduced
skills from 22 → 21 (21 because 3 research skills were added); agents
10 → 7.

**Alternatives considered:**
- Keep for possible future interactive-slide use: rejected — user has
  never used Quarto, felt ongoing cost not justified by speculative benefit.
- Keep just the infrastructure, no skills: rejected — partial infrastructure
  creates confusion about what's supported.

**Consequences:**
- Shorter skill menu at session start (reduced context overhead).
- If user later wants interactive web slides, they can evaluate tooling fresh
  at that time. Git history preserves all of it.
- Simpler mental model: one slide system (Beamer PDF).

**If revisiting:** `git log --all` will find the deleted Quarto infrastructure.
But by the time interactive slides become needed, better tools may exist.

---

## 2026-04-16: Data storage convention (Box, not git)

**Decision:** All raw and processed data live in UC Berkeley Box at
`~/Library/CloudStorage/Box-Box/Research/[project-name]/`. The project folder
has a gitignored `data/` directory with only `PROVENANCE.md` tracked.
Three patterns defined for different data sources (uploaded / downloaded /
created) in `.claude/rules/data-storage.md`.

**Alternatives considered:**
- Data inside project folder, gitignored: rejected — risks syncing issues
  with large files, doesn't leverage Berkeley-provided storage.
- Dropbox instead of Box: rejected — Box is institutional (IRB-appropriate),
  Dropbox is personal.
- External drive only: rejected — loses access controls and sharing
  capabilities Box provides.

**Consequences:**
- Data is never at risk of committing to GitHub (gitignore + pre-commit hook).
- IRB-appropriate storage by default.
- User must manually create the Box folder when starting a project (Step 6
  in the checklist).
- `PROVENANCE.md` becomes the authoritative inventory of data since Box
  contents aren't visible to git.

**If revisiting:** The path convention is in one line in `data-storage.md`.
If Berkeley changes Box sync location, or user switches to a different
storage provider, one file to update.

---

## 2026-04-16: Domain-reviewer 5-lens customization

**Decision:** Replaced the generic 5 review lenses in
`.claude/agents/domain-reviewer.md` with:
1. Theoretical coherence
2. Front-end / back-end alignment
3. Identification clarity (RCT + observational)
4. Effect size interpretation
5. Mechanism evidence (how X causes Y, not just whether)

**Alternatives considered:**
- Keep the original generic lenses: rejected — produced vague feedback
  that duplicated `proofreader` and `review-paper`.
- Include preregistration-deviation as its own lens: rejected — too narrow
  (RCT-only bookkeeping); covered inside other lenses when relevant.

**Consequences:**
- Agent output now matches the failure modes that sink papers at ASQ / AMJ
  / OrgSci / MgmtSci.
- Lenses 1 and 2 reflect user's self-identified sociologist priorities and
  fire first.
- Lens 5 catches the "observationally equivalent stories" failure mode.

**If revisiting:** If the user shifts research focus (e.g., more experimental,
less sociological), the theoretical-coherence lens might be rebalanced toward
behavioral-economics or management conventions.

---

## 2026-04-16: Three research skills added

**Decision:** Added three skills tailored to RCT + observational workflow:
- `preregistration` — scaffolds aspredicted.org preregistration
- `rct-toolkit` — R analysis starter using fixest + modelsummary + data.table
- `revise-resubmit` — R&R response tracker, PDF final output

**Alternatives considered:**
- Social-network-analysis toolkit: rejected — user's research involves
  networks but SNA tooling wasn't flagged as a priority.
- Qualitative-coding helper: rejected — user doesn't do qualitative work.
- Journal-specific manuscript formatters: deferred — fiddly to maintain,
  target journals can change.

**Consequences:**
- Skills encode user conventions: `fixest`, `modelsummary`, `data.table`,
  camelCase, cluster SEs at main unit of analysis, aspredicted format,
  PDF R&R output.
- Each skill will feel generic on first use until actual project context
  fills it in.

**If revisiting:** Skills are single-file SKILL.md definitions; easy to
modify or add new ones. Conventions are listed near the top of each file.

---

## 2026-04-16: Pre-commit large-file guard

**Decision:** Added `scripts/git-hooks/pre-commit` that blocks commits of
files > 50 MB, `.RData`/`.rds`/`.dta` regardless of size, and `.csv` > 10
MB. Override via `git commit --no-verify`. Activated per-project via
`git config core.hooksPath scripts/git-hooks`.

**Alternatives considered:**
- Global git template hook (set once for user's entire Mac): rejected —
  per-project is safer; user doesn't want this behavior on non-research repos.
- Rely only on `.gitignore`: rejected — gitignore requires user to know
  which files to list; hook catches unknown unknowns.

**Consequences:**
- Any project started from this template has the guard after Step 3 of the
  checklist.
- Protection against accidentally pushing confidential data to GitHub.
- Occasional friction if the user legitimately wants to commit a small
  data file; easy override.

**If revisiting:** Thresholds are in the first few lines of the hook; adjust
without touching the rest.

---

## 2026-04-16: Solo GitHub workflow (push, not PRs)

**Decision:** Day-to-day workflow is `git add / git commit / git push`.
No feature branches, no PRs, no merges. The `new-project-checklist.md`
recommends one push at end of day for off-site backup. Claude Desktop's
"Create PR" suggestion is acknowledged but pointed out as unnecessary
ceremony for solo work.

**Alternatives considered:**
- PR-based workflow (main protected, feature branches, PRs to merge):
  rejected — pure overhead for solo work where the user reviews their
  own code.
- No GitHub at all, just local commits: rejected — loses off-site backup,
  which is the real value proposition.

**Consequences:**
- `git push` defaults cleanly (no arguments) after the initial `-u` setup.
- User doesn't learn branch/merge mechanics upfront; can add later when
  a coauthor joins.
- The checklist's "What NOT to do" section warns against `--force`,
  `reset --hard`, and committing data files.

**If revisiting:** If a coauthor joins a project, that project's workflow
upgrades to branch-and-PR. See the coauthor setup question (question 2
in the session that produced this template).

---

## 2026-04-16: CLAUDE.md placeholder strategy

**Decision:** The template's CLAUDE.md uses self-explanatory placeholders
(e.g., `[Project name — replace when copying this template for a new
project]`) and includes three commented-out "Current State" variants
(research project / MBA course / exec ed session) that the user uncomments
and fills in at project start.

**Alternatives considered:**
- Force a starter-prompt workflow to fill in placeholders at each session:
  rejected — imposes ritual for zero benefit in a stable template.
- Keep the project name static ("Research Workflow Template"): rejected —
  the template is distinct from a filled-in project; the placeholder
  communicates "replace me."
- Delete the Current State section entirely: rejected — three variants
  capture real patterns user said they use.

**Consequences:**
- Template CLAUDE.md stays uncommitted-looking until filled in (feature,
  not bug — signals incomplete setup clearly).
- At project start, the user makes ~5 quick edits to CLAUDE.md.
- Step 4 of `new-project-checklist.md` walks through these edits.

**If revisiting:** If a fourth project type emerges (e.g., a book manuscript,
a policy report), add a fourth commented variant to the template.
