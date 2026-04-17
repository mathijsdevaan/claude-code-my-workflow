# Academic Presentation Decks (Seminars, Conferences, Job Talks)

**Trigger:** When `**Slide style:** academic` is declared in `CLAUDE.md`, OR when the user
says they are preparing any of: a "seminar," "conference talk," "academic presentation,"
"job talk," or "workshop presentation."

## Theme

- Use `\usetheme[progressbar=none,numbering=none,block=fill]{metropolis}` + `\usepackage{UCBerkeleyAcademic}`
- File: `Preambles/UCBerkeleyAcademic.sty`
- Compile with XeLaTeX (required for fontspec: Fira Sans)
- Document preamble needs `\PassOptionsToPackage{table}{xcolor}` BEFORE `\documentclass`

## Document skeleton

```latex
\PassOptionsToPackage{table}{xcolor}
\documentclass[aspectratio=169,10pt]{beamer}
\usetheme[progressbar=none,numbering=none,block=fill]{metropolis}
\usepackage{UCBerkeleyAcademic}

% Short versions shown in footer (author | title | page)
\renewcommand{\insertshortauthor}{LastName}
\renewcommand{\insertshorttitle}{Short Title}

\begin{document}

% Use \titleslide{title}{authors}{venue} — NOT \maketitle
\titleslide
  {Full Paper Title}
  {Author Name \\[0.4em] \small Affiliation}
  {Venue \textbullet\ Date}

\section{Introduction}  % produces minimal divider slide

\begin{frame}{First content slide}
  ...
\end{frame}

\end{document}
```

For multi-author papers, the authors argument takes a tabular:
```latex
\titleslide
  {Paper Title}
  {\begin{tabular}{ccc}
    Author One & Author Two & Author Three \\
    \small Affil 1 & \small Affil 2 & \small Affil 3
   \end{tabular}}
  {Conference \textbullet\ 2026}
```

## Slide Style

- **Dense slides acceptable** — audience is methods-literate
- **Small frame title** is default; use `\largeframetitle` for section introductions
- **Equations OK and welcome** — use `amsmath` environments
- **Inline citations** via `\cit{Author Year; Author Year}` — renders small gray
- **Tables** use booktabs (`\toprule`, `\midrule`, `\bottomrule`); no zebra striping
- **Figures** should be publication-ready (consistent with paper)

## Color Usage

- Frame titles: AccentRed (automatic via theme — red bar, white text)
- Body text: near-black
- Inline citations: CiteGray (automatic via `\cit{}`)
- Accent / emphasis: `\textcolor{AccentRed}{...}` sparingly

## Deck Structure (30–90 min academic talk)

Standard academic talk structure — adapt length but preserve order:

1. **Title slide** — full author list, affiliations, venue, date
2. **Motivation** (2–3 slides) — the puzzle, why it matters, stakes
3. **Contribution** (1 slide) — positioning in the literature, what's new
4. **Data and setting** — context, sample, key variables, summary stats
5. **Empirical strategy / identification** — specification, identifying variation, threats
6. **Main results** — headline table(s), effect sizes, interpretation
7. **Mechanisms** — how does X cause Y? Tests that distinguish mechanisms.
8. **Heterogeneity** — if relevant, what predicts the effect?
9. **Robustness** — pre-registered checks, alternative specifications, falsification
10. **Discussion / conclusion** — what we learned, what remains, policy implications
11. **Appendix slides** — referenced from main body, for Q&A

## Section Dividers

Use `\section{Name}` between major blocks — Metropolis renders them as minimal slides
with bold title + olive rule, consistent with the reference style. Reserve for: Introduction,
Data, Strategy, Results, Mechanisms, Robustness, Conclusion.

## Audience Notes

- Academic audiences expect methodological rigor — assume familiarity with standard
  identification strategies (DID, IV, RDD, RCT) but still defend yours explicitly
- Lead with the contribution to the literature, not with "my paper is about X"
- Show null results and failed robustness checks — hiding them is noticed
- Cite generously inline (via `\cit{}`); the full reference list goes in the paper
- Preregistration deviations should be disclosed on the relevant analysis slide
- Expect hostile questions; reserve 20–30% of time for Q&A

## What to avoid

- Title-slide clutter (no university logo; let the authors + venue speak)
- Over-branding (no Berkeley blue diagonal footer — use the subtle charcoal bar)
- Equations without interpretation (every symbol needs a natural-language gloss)
- Vague mechanism language ("consistent with a learning story" → what data would falsify that?)
- Ignoring pre-registration (if the paper is an RCT with a plan, mention it)
