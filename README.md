# Claude Code for Academic Research

A template repository for AI-assisted academic work — lecture slides, research
papers, data analysis, and replication packages. You describe what you want;
Claude plans the approach, runs specialized review agents, fixes issues,
verifies quality against numeric gates, and presents results.

This is both a **working template** (copied to start each new project) and a
**public reference** others can fork and adapt. See
`.claude/rules/meta-governance.md` for how that dual nature is managed.

**Last Updated:** 2026-08-19

---

## Quick Start

**Starting a new project from this template (local):**

```bash
./scripts/new_project.sh "My-Project-Name"
```

or run `/new-project` inside Claude Code. Either way you get a fresh git
history, the large-file commit guard installed, and template leftovers removed.
`templates/new-project-checklist.md` documents every step, including a
git-for-beginners primer.

**Forking from GitHub:** fork, clone, then open `CLAUDE.md` and replace the
bracketed placeholders (project name, slide style). The rules, skills, agents,
and hooks work out of the box; the Beamer themes and R conventions are the
parts you'll most want to adapt.

---

## How It Works

- **Plan first.** Non-trivial tasks start in plan mode; plans are saved to
  `quality_reports/plans/` so they survive context compression.
- **Contractor mode.** After plan approval, an orchestrator loop implements,
  verifies, reviews (specialized agents), fixes, and scores — autonomously,
  with hard loop limits and a 3-strikes circuit breaker.
- **Quality gates.** Nothing ships below 80/100 (`scripts/quality_score.py`);
  90 for PRs. Rubrics live in `.claude/rules/quality-gates.md`.
- **Context survival.** Hooks snapshot state before compaction and restore it
  after; a Stop hook enforces session logging; MEMORY.md accumulates `[LEARN]`
  entries across sessions.
- **Evidence discipline.** Research projects track hypotheses, insights, and
  binding decisions in `research/` with a falsification-gated status machine —
  a hypothesis cannot reach "confirmed" without passing a falsification test
  written before the analysis ran.

## What's Included

**8 agents · 25 skills · 21 rules · 7 hooks.** The authoritative skill list
with one-line descriptions is the Skills Quick Reference table in
[CLAUDE.md](CLAUDE.md) — it is kept in sync with `.claude/skills/` on disk.

- **Slide production** — two UC Berkeley Beamer themes (`teaching` for exec
  ed/MBA, `academic` for seminars/job talks), XeLaTeX compile pipeline, and
  layered review: proofreading, visual audit, pedagogy review, TikZ critique
  (arithmetic anti-collision checks, not eyeballing), devil's advocate, and a
  combined `/slide-excellence` pass.
- **Research workflow** — `/research-ideation`, `/interview-me`, `/lit-review`,
  `/preregistration`, `/rct-toolkit`, `/data-analysis`, `/review-paper`,
  `/revise-resubmit`, and the `research/` hypothesis tracker via
  `/research-log`.
- **Epistemics & correctness** — `/blindspot` (pre-interpretation audit of
  output: what's unexplained, what's conveniently absent, what's undersold),
  `/replication-audit` (fresh-context correctness audit with R↔Python
  replication of key results), `/validate-bib --verify` (per-entry
  fact-checking of bibliography entries against the actual papers).
- **Infrastructure** — plan-first workflow, orchestrator protocol, session
  logging, exploration sandbox with a fast-track quality bar, data-storage
  convention (raw data lives in UC Berkeley Box, never in git, with a
  pre-commit large-file guard), and `/new-project` bootstrapping.

## Data Convention

Code, writing, and documentation live in git. Data lives in Box
(`~/Library/CloudStorage/Box-Box/Research/[project-name]/`), documented in
`data/PROVENANCE.md`. See `.claude/rules/data-storage.md` for the full
decision table by data source.

## Prerequisites

- [Claude Code](https://code.claude.com/docs/en/overview) (CLI or VS Code)
- XeLaTeX (TeX Live / MacTeX) — required for the Beamer themes' fonts
- R (with `data.table`, `fixest`, `modelsummary`) for the analysis skills
- Fonts and logo per `templates/manual-setup-steps.md` (one-time per machine)

## Adapting for Your Field

1. Fill in `CLAUDE.md` placeholders and pick a slide style
2. Customize `.claude/agents/domain-reviewer.md` with your field's review lenses
3. Adjust `.claude/rules/r-code-conventions.md` (or add conventions for your language)
4. Fill in `.claude/rules/knowledge-base-template.md` if building a course
5. Swap the Beamer themes in `Preambles/` for your institution's branding

---

## Credits

- Forked from **[claude-code-my-workflow](https://github.com/pedrohcgs/claude-code-my-workflow)**
  by Pedro Sant'Anna (Emory), who built the original orchestrator, quality-gate,
  and hook infrastructure for a PhD econometrics course. His
  [guide](https://psantanna.com/claude-code-my-workflow/) remains an excellent
  walkthrough of the underlying design.
- Several patterns adapted from **[MixtapeTools](https://github.com/scunning1975/MixtapeTools)**
  by Scott Cunningham (Baylor): the hypothesis tracker's falsification-gated
  status machine, `/blindspot`, the Referee-2 replication audit, per-entry
  bibliography verification, TikZ anti-collision arithmetic, and the 3-strikes
  circuit breaker.
- Other setups worth studying: [clo-author](https://github.com/hsantanna88/clo-author)
  (Hugo Sant'Anna), [claudeblattman](https://github.com/chrisblattman/claudeblattman)
  (Chris Blattman), [autoresearch](https://github.com/karpathy/autoresearch)
  (Andrej Karpathy).

## License

MIT License. See [LICENSE](LICENSE).
