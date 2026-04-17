# CLAUDE.MD — Academic Project Development with Claude Code

<!-- HOW TO USE: This file is the starting template. When you copy this repo for a new
     project, replace the [BRACKETED PLACEHOLDERS] below, pick ONE "Current State"
     variant and delete the others, and set the **Slide style** declaration.
     See templates/new-project-checklist.md for the full startup procedure.
     Keep this file under ~150 lines — Claude loads it every session. -->

**Project:** [Project name — replace when copying this template for a new project]
**Institution:** UC Berkeley, Haas School of Business
**Slide style:** [teaching | academic — pick one; determines theme + conventions]

---

## Core Principles

- **Plan first** — enter plan mode before non-trivial tasks; save plans to `quality_reports/plans/`
- **Verify after** — compile/render and confirm output at the end of every task
- **Single source of truth** — Beamer `.tex` is authoritative for slide decks
- **Quality gates** — nothing ships below 80/100
- **[LEARN] tags** — when corrected, save `[LEARN:category] wrong → right` to MEMORY.md

---

## Folder Structure

```
[YOUR-PROJECT]/
├── CLAUDE.MD                    # This file
├── .claude/                     # Rules, skills, agents, hooks
├── Bibliography_base.bib        # Centralized bibliography
├── Figures/                     # Figures and images
├── Preambles/                   # LaTeX headers + Beamer themes
├── Slides/                      # Beamer .tex files
├── scripts/                     # Utility scripts + R code
├── quality_reports/             # Plans, session logs, merge reports
├── explorations/                # Research sandbox (see rules)
├── templates/                   # Session log, project checklist, skill templates
└── references/                  # Reference papers and decks
```

---

## Commands

```bash
# LaTeX (3-pass, XeLaTeX only)
cd Slides && TEXINPUTS=../Preambles:$TEXINPUTS xelatex -interaction=nonstopmode file.tex
BIBINPUTS=..:$BIBINPUTS bibtex file
TEXINPUTS=../Preambles:$TEXINPUTS xelatex -interaction=nonstopmode file.tex
TEXINPUTS=../Preambles:$TEXINPUTS xelatex -interaction=nonstopmode file.tex

# Quality score
python scripts/quality_score.py Slides/file.tex
```

---

## Quality Thresholds

| Score | Gate | Meaning |
|-------|------|---------|
| 80 | Commit | Good enough to save |
| 90 | PR | Ready for deployment |
| 95 | Excellence | Aspirational |

---

## Skills Quick Reference

| Command | What It Does |
|---------|-------------|
| `/compile-latex [file]` | 3-pass XeLaTeX + bibtex |
| `/proofread [file]` | Grammar/typo/overflow review |
| `/visual-audit [file]` | Slide layout audit |
| `/pedagogy-review [file]` | Narrative, notation, pacing review |
| `/review-r [file]` | R code quality review |
| `/slide-excellence [file]` | Combined multi-agent review |
| `/validate-bib` | Cross-reference citations |
| `/devils-advocate` | Challenge slide design |
| `/create-lecture` | Full lecture creation |
| `/commit [msg]` | Stage, commit, PR, merge |
| `/lit-review [topic]` | Literature search + synthesis |
| `/research-ideation [topic]` | Research questions + strategies |
| `/interview-me [topic]` | Interactive research interview |
| `/review-paper [file]` | Manuscript review |
| `/data-analysis [dataset]` | End-to-end R analysis |
| `/preregistration` | Scaffold aspredicted.org preregistration |
| `/rct-toolkit` | RCT analysis starter (fixest + modelsummary) |
| `/revise-resubmit` | R&R response tracker + cover letter |
| `/learn [skill-name]` | Extract discovery into persistent skill |
| `/context-status` | Show session health + context usage |
| `/deep-audit` | Repository-wide consistency audit |

---

## Beamer Theme System

Two themes available in `Preambles/`. The `**Slide style**` declaration at the top
of this file determines which one Claude uses for slide-related work.

### Teaching (`beamerthemeUCBerkeleyTeaching.sty`)

For executive education and MBA lectures. Berkeley-branded, sparse practitioner style.
Full conventions in `.claude/rules/teaching-slides.md`.

**Colors:** `BerkeleyBlue` (#003262), `Medalist` (#C4820E), `FoundersRock`, `CaliforniaGold`

**Custom Commands:**

| Command | Effect | Use Case |
|---------|--------|----------|
| `\smallframetitle` | Smaller bold title | Content-heavy slides |
| `\normalframetitle` | Large title (default) | Standard slides |
| `\tableheadrow` | Gold background row | First row of tables |
| `\tableheadcol{text}` | White bold column header | Table headers |

### Academic (`beamerthemeUCBerkeleyAcademic.sty`)

For seminars, conference talks, and job talks. Dense, citation-heavy, modern sans-serif
styling with dark red title bars and charcoal footer. Metropolis-based.
Full conventions in `.claude/rules/academic-slides.md`.

**Colors:** `AccentRed` (#A12830), `FooterGray` (#3F3F3F), `OliveRule` (#9B8B5A), `CiteGray`

**Custom Commands:**

| Command | Effect | Use Case |
|---------|--------|----------|
| `\cit{Author, Year}` | Inline gray citation | Dense reference annotation |
| `\largeframetitle` | Larger title | Section-intro slides |
| `\smallframetitle` | Smaller title (default) | Content-dense slides |

---

## Current State

<!-- At project start: uncomment ONE variant matching this project's type
     (research / MBA course / exec ed session), fill it in, delete the others. -->

<!-- RESEARCH PROJECT:
**Phase:** [idea / data / analysis / drafting / R&R / published]
**Target venue:** [journal]
**Due:** [deadline]
**Active tasks:**
- [task 1]
- [task 2]

**Key files:**
- Main draft: paper/main.tex
- Analysis: code/03_analysis.R
- Preregistration: rnr/preregistration.md (if RCT)
-->

<!-- MBA COURSE:
**Course:** [course code, term]
**Duration:** 14 × 2hr lectures, Aug–Oct

| # | Topic | Beamer file | Status | Next update |
|---|-------|-------------|--------|-------------|
| 1 |       |             |        |             |
| 2 |       |             |        |             |
-->

<!-- EXEC ED SESSION:
**Client:** [company], [date]
**Audience:** [description, approx size]
**Focus:** [one-sentence theme]
**Deck:** session.tex
-->
