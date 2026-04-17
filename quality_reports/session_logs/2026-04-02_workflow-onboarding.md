# Session Log: Workflow Onboarding

**Date:** 2026-04-02
**Goal:** Onboard new user and adapt workflow for their research/teaching needs

## Key Context

- User is a professor at UC Berkeley's Haas School of Business
- Specializes in organizational behavior and social networks
- Research stack: R (fixest, data.table, ggplot2), Python as needed, large administrative datasets
- Writing in LaTeX, teaching executive education
- Wants to adapt this workflow for both research projects and teaching materials

## Decisions

- Saved user profile to memory system
- Discussed how existing skills map to their workflow
- Explored CLAUDE.md structure: folder layout, commands, quality gates, skills reference
- Explained Quarto (RevealJS HTML slides) — user unfamiliar, may not need it
- Explained [LEARN] tags — persistent memory across sessions
- Read `beamerthemeUCBerkeley.sty` from Preambles/ — identified colors + custom commands
- Updated CLAUDE.md: added UC Berkeley institution, Beamer Custom Environments with Berkeley theme subsection and Academic Presentations placeholder
- Created `.claude/rules/exec-ed-slides.md` — style guide for exec ed decks (sparse slides, practitioner tone, deck structure)
- User mentioned a separate academic Beamer skill at `~/.claude/skills/beamer-slides/SKILL.md` — file doesn't exist yet, deferred
- Explained git workflow: branch+PR+merge vs direct commit to main
- Committed all changes directly to main (not pushed to remote yet)

## Open Questions

- Academic Beamer theme — user wants a separate style for academic audiences, needs to create/locate the skill
- Whether to push commit to GitHub remote
- Which other workflow files to explore next

---

## 2026-04-16 — Workflow Personalization (Continuation)

**Goal:** Deeper personalization of the forked template after ~2 weeks of reflection.

**Plan:** `quality_reports/plans/2026-04-16_workflow-personalization.md` (DRAFT, in progress)

### User clarifications gathered this session

- Time split: mostly research, but structured teaching — exec ed 1–2x/month + 8-week MBA block Aug–Oct
- Research: quantitative, observational admin data + within-org RCTs
- Not prioritizing: qualitative coding, social-network-specific tooling
- Pruning appetite: moderate
- Solo workflow — no collaboration infrastructure needed
- **Key framing:** this repo is explicitly the TEMPLATE. Every new project (research / MBA / exec ed) starts by copying this repo. So CLAUDE.md in this repo should contain scaffolding for customization, not specific project state.

### Decisions approved so far (Parts 1 + 2a)

1. **Part 1 — Pruning:**
   - Delete `master_supporting_docs/` (legacy, nearly empty)
   - Delete `guide/` source (keep compiled `docs/workflow-guide.html`)

2. **Part 2a — CLAUDE.md cleanup:**
   - Line 3 `[YOUR PROJECT NAME]` → self-explanatory placeholder `[Project name — replace when copying this template for a new project]`
   - "Current Project State" lecture table → three commented-out variants (research project / MBA course / exec ed session) for customization at project start
   - Delete "Quarto CSS Classes" empty table
   - Academic Presentations subsection: **build two parallel systems**
     - Two rule files: `.claude/rules/teaching-slides.md` (merges exec-ed + MBA) and `.claude/rules/academic-slides.md` (new)
     - Two theme files: `beamerthemeUCBerkeleyTeaching.sty` and `beamerthemeUCBerkeleyAcademic.sty`
     - Academic theme draft shown to user: smaller fonts, subtle text footer (no blue diagonal / logo), black body text, booktabs + amsmath preloaded, `\largeframetitle` as inverse switch

3. **Major plan revision — drop Quarto entirely:**
   - User initially interested in Quarto for interactive slides, then reconsidered — rather reassess if/when a need arises
   - Removes: `Quarto/`, 4 skills (translate-to-quarto, qa-quarto, deploy, extract-tikz), 3 agents (quarto-critic, quarto-fixer, beamer-translator), 1 rule (beamer-quarto-sync.md), 1 script (sync_to_docs.sh)
   - Simplifies Core Principles in CLAUDE.md (no more SSOT sync line)
   - Drops skill count from 22 → 18; agents from 10 → 7
   - Git history preserves everything if the user changes mind

### Open — still to discuss in this session

- User reviewing the academic theme draft — awaiting approval/tweaks
- Part 2b (academic Beamer theme) is now subsumed into Part 2a Point 4 decision above
- Part 2c: investigate `.claude/settings.local.json` Skill restriction
- Part 3: new research skills (preregistration, rct-toolkit, revise-resubmit), domain-reviewer customization, large-file commit guard hook
- Part 4: broader productivity observations

### Process feedback from user

- User explicitly flagged that responses were too long and under-motivated. Adjusted to: every recommendation gets *what it is* / *why it helps you specifically* / *what the tradeoff is*. Then further simplified on request to shorter responses.
- Preference: walk through plan recommendations one at a time with pause for reaction, rather than dumping the whole plan.
