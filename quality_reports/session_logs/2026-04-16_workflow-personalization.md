# Session Log: Workflow Personalization

**Date:** 2026-04-16
**Goal:** Review the forked academic workflow repo and adapt it for user's research + teaching needs. Deeper personalization after the 2026-04-02 onboarding session.

## Key Context

- User is UC Berkeley Haas professor — org behavior, social networks, R/Python/LaTeX
- Research: quantitative, observational admin data + within-org RCTs (dominant)
- Teaching: exec ed 1–2x/month + 8-week MBA block Aug–Oct
- Solo workflow, no coauthors in this repo
- **Framing:** this repo is the TEMPLATE — every new project (research / MBA / exec ed) starts by copying it. CLAUDE.md should provide scaffolding for customization, not specific project state.
- Pruning appetite: moderate

## Plan

`quality_reports/plans/2026-04-16_workflow-personalization.md` (DRAFT). Walked through recommendations with user one at a time.

## Decisions approved

### Part 1 — Pruning
- Delete `master_supporting_docs/` (legacy, nearly empty)
- Delete `guide/` source (keep compiled `docs/workflow-guide.html`)

### Part 2a — CLAUDE.md cleanup
- Line 3 `[YOUR PROJECT NAME]` → self-explanatory placeholder `[Project name — replace when copying this template for a new project]`
- "Current Project State" table → three commented-out variants (research / MBA / exec ed) for customization at project start
- Delete "Quarto CSS Classes" empty table
- Academic Presentations: **build two parallel systems**
  - Two rule files: `.claude/rules/teaching-slides.md` + `.claude/rules/academic-slides.md`
  - Two theme files: `beamerthemeUCBerkeleyTeaching.sty` + `beamerthemeUCBerkeleyAcademic.sty`

### Major plan revision — drop Quarto
User initially interested, then reconsidered. Removes: `Quarto/` folder, 4 skills (translate-to-quarto, qa-quarto, deploy, extract-tikz), 3 agents (quarto-critic, quarto-fixer, beamer-translator), 1 rule (beamer-quarto-sync.md), 1 script (sync_to_docs.sh). Skills: 22 → 18. Git history preserves everything.

## Academic theme preview

Built `beamerthemeUCBerkeleyAcademic.sty` draft at `/tmp/academic-theme-preview/`. Compiled 5 sample slides (title, motivation, empirical strategy with equations, regression table, mechanisms + robustness). User saw renders and found the visual distinction works.

Key design: smaller frametitle (`\large \bfseries`), BerkeleyBlue instead of Medalist gold, black body text, tighter margins (1.5em), subtle text-only footer, no blue diagonal / no wordmark logo, `\largeframetitle` as inverse switch, booktabs + amsmath preloaded.

## Discovered issue — Open Sans not installed

The existing `beamerthemeUCBerkeley.sty` fails to find "Open Sans" on this machine (confirmed via `fc-list` and xelatex compile errors). The existing teaching theme is also affected. User needs to install Open Sans (free from Google Fonts) before either theme will render correctly in production. Used Helvetica Neue as preview fallback.

## Open — still to discuss

- Part 2c: investigate `.claude/settings.local.json` Skill access restriction (only `commit` allowed?)
- Part 3: new research skills (preregistration, rct-toolkit, revise-resubmit), domain-reviewer customization, large-file commit guard hook
- Part 4: broader productivity observations (template-vs-project-repo pattern, personal memory, research-project/ template skeleton)

## Process feedback captured

User flagged: responses too long, recommendations under-motivated. Adjusted to: every recommendation gets *what it is* / *why it helps you specifically* / *what the tradeoff is*. Then further shortened on request. Preference: walk through plan items one at a time with pause for reaction, not whole-plan dumps.

---

## Updates since creation

### Teaching theme preview

Built comparison preview at `/tmp/teaching-theme-preview/` using existing `beamerthemeUCBerkeley.sty` with exec-ed-style content (sparse bullets, Team Building session). Rendered 5 slides. User saw both previews and agreed the teaching vs academic visual distinction is clear:

| Element | Teaching | Academic |
|---|---|---|
| Frame title | Medalist gold, large | Berkeley Blue, large bold |
| Body text | Berkeley Blue | Black |
| Footer | Blue diagonal + logo | Thin text "UC Berkeley • n/N" |
| Density | Sparse | Dense |
| Tables | Gold header + zebra | Booktabs |
| Margins | 2em | 1.5em |

### Three real setup issues surfaced during preview

Independent of the academic theme discussion — these affect the current teaching theme too:

1. **Open Sans not installed on this machine** — `fc-list | grep -i "open sans"` returns nothing. Both themes fail to find the sans font, cascading into rendering errors. Preview used Helvetica Neue fallback. Fix: install Open Sans from Google Fonts (free).
2. **`UCBerkeley_wordmark_white` logo missing from `Preambles/`** — teaching theme footer can't render the logo. Preview used a generated placeholder.
3. **Teaching theme footer overlap bug** — when a slide has content near the bottom, the blue diagonal footer cuts into it (visible on the Discussion slide, "Five minutes." clipped). Layout risk for real exec-ed decks.

### Open — continuing next

- Add the three setup fixes above to the plan
- Plan item: build `beamerthemeUCBerkeleyAcademic.sty` + `academic-slides.md` rule file
- Plan item: maybe rename existing theme/rule to `Teaching` variants for symmetry
- Still to discuss: Part 2c (`settings.local.json` Skill restriction), Part 3 (research skills, domain-reviewer, large-file hook), Part 4 (broader productivity observations)

### Reference deck style target

User shared `master_supporting_docs/supporting_slides/Hospital_management_MRL (2).pdf` (La Forgia, Paris, Shi) as the academic style target. Preferred over my first academic draft.

Defining elements (now captured):
- Frame title = red bar with white text (accent color ~ `#A12830`)
- Footer = three-column charcoal bar (`#3F3F3F`): short author | short title | page
- Section divider = bold title + thin olive rule (`#9B8B5A`)
- Sans-serif throughout (reference appears to use Fira Sans; preview uses Helvetica Neue)
- Inline citations in gray `[Author, Year]`
- Two-column colored-header boxes for compare-and-contrast slides
- Base on Beamer's `metropolis` theme (installed at `/usr/local/texlive/2018/...`), heavily customized

Built working approximation at `/tmp/academic-v2/` — 5 slides match the reference closely. User viewing.

---

## Execution phase (Path 1 — in-session)

User chose to execute the full plan immediately. All 14 items completed:

### Deletions / renames
- Moved reference deck → `references/reference-deck-laForgia-paris-shi.pdf`
- Deleted `master_supporting_docs/` and `guide/`
- Dropped Quarto infrastructure: `Quarto/` folder, 4 skills (translate-to-quarto, qa-quarto, deploy, extract-tikz), 3 agents (quarto-critic, quarto-fixer, beamer-translator), `beamer-quarto-sync.md`, `scripts/sync_to_docs.sh`
- Renamed `Preambles/beamerthemeUCBerkeley.sty` → `Preambles/beamerthemeUCBerkeleyTeaching.sty` (updated `\ProvidesPackage` internally)
- Deleted `.claude/rules/exec-ed-slides.md` (replaced by broader `teaching-slides.md`)

### New files written
- `Preambles/beamerthemeUCBerkeleyAcademic.sty` — Metropolis-based, dark red frame bars, charcoal 3-column footer, Fira Sans, inline citation helper
- `.claude/rules/teaching-slides.md` — broadened from exec-ed scope to cover both exec ed and MBA
- `.claude/rules/academic-slides.md` — triggers on `**Slide style:** academic`, specifies deck structure (motivation → lit → data → strategy → results → mechanisms → robustness)
- `.claude/skills/preregistration/SKILL.md` — aspredicted 8-field walkthrough, produces markdown + R skeleton
- `.claude/skills/rct-toolkit/SKILL.md` — fixest + modelsummary + data.table + camelCase; cluster at main unit of analysis (study-dependent)
- `.claude/skills/revise-resubmit/SKILL.md` — 3 modes (initial parse, update, finalize); produces response letter + cover letter as PDF
- `scripts/git-hooks/pre-commit` — blocks `.RData`/`.rds`/`.dta` and files >50MB; tested working at /tmp/hooktest
- `templates/new-project-checklist.md` — beginner git walkthrough (6 steps + day-to-day workflow + troubleshooting)
- `templates/manual-setup-steps.md` — font install (Open Sans, Fira Sans) + logo restoration instructions

### Rewrites
- `CLAUDE.md` — full rewrite: self-explanatory placeholder, `**Slide style:**` declaration, both themes documented, Quarto references removed, three commented-out Current State variants
- `.claude/agents/domain-reviewer.md` — 5 lenses: (1) Theoretical coherence, (2) Front-end/back-end alignment, (3) Identification clarity, (4) Effect size interpretation, (5) Mechanism evidence. Re-framed from lecture-review to manuscript-review primary.

### Counts after execution
- Skills: 22 → 21 (−4 Quarto, +3 research)
- Agents: 10 → 7 (−3 Quarto-related)
- Rules: 20 → 19 (−1 Quarto, +1 net: teaching renamed not counted as new; academic is new; exec-ed deleted)

### User conventions captured
- Preregistration platform: aspredicted.org
- R stack: fixest + modelsummary + data.table, camelCase variables
- Cluster SE: at main unit of analysis (study-dependent; skill asks)
- R&R output: PDF (via pandoc + xelatex)

### Manual steps remaining (user action)
1. Install Open Sans + Fira Sans from Google Fonts → **DONE during session** (user confirmed via fc-list: 22 Open Sans variants, 18 Fira Sans variants installed)
2. Restore `Preambles/UCBerkeley_wordmark_white.png` — still pending
3. Run verification compile of both themes (documented in manual-setup-steps.md)

### Not yet committed
All changes staged/untracked in working tree. User has not yet run `/commit` or `git commit`. They can commit when ready.

### 4c and 4d dropped
- 4c (personal-memory.md) — user declined
- 4d (session-log hook stale-state fix) — user declined, accepting false-alarm reminders
