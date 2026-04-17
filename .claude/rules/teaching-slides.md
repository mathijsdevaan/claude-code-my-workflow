# Teaching Slide Decks (Exec Ed + MBA)

**Trigger:** When `**Slide style:** teaching` is declared in `CLAUDE.md`, OR when the user
says they are preparing any of: an "exec ed" / "executive education" deck, an "MBA
lecture," or "class slides."

## Theme

- Use `\usetheme{UCBerkeleyTeaching}` — file: `Preambles/beamerthemeUCBerkeleyTeaching.sty`
- Compile with XeLaTeX (required for fontspec: Georgia + Open Sans)
- Logo file `UCBerkeley_wordmark_white` must be in the LaTeX search path

## Slide Style

- **Sparse slides** — prefer visuals and short phrases over paragraphs
- **Max 4–5 bullet points** per slide; each bullet ≤ 1.5 lines
- **Use `\smallframetitle`** when a slide needs more content space
- **Tables** use `\tableheadrow` + `\tableheadcol{}` for Berkeley-styled headers
- **Alternating row colors** are automatic (built into theme)

## Color Usage

- Frame titles: Medalist gold (automatic via theme)
- Body text: Berkeley Blue (automatic via theme)
- Use `\textcolor{FoundersRock}{...}` for inline accent/emphasis
- Use `\textcolor{CaliforniaGold}{...}` sparingly for highlights

## Deck Structure

### Exec ed session (90 min, single deck)
- Title slide (auto-styled)
- Agenda / session overview
- Content sections with discussion prompts between
- Case study or exercise slides
- Key takeaways / summary
- Q&A / discussion slide

### MBA lecture (2 hr, per-lecture deck)
- Title slide with lecture number and topic
- Learning objectives (3–5, outcome-focused)
- Motivating example or case
- Core concepts (with frequent examples)
- Application exercises or discussion breaks
- Summary and preview of next lecture
- Readings reminder

## Audience Notes

- **Exec ed:** practitioners, not academics. Minimize jargon; define technical terms.
  Lead with "why this matters" before methods or theory. Real-world examples over
  formal proofs. Encourage discussion.
- **MBA:** more methods exposure than exec ed but still practitioner-oriented.
  Examples matter more than proofs. Connect every concept to a management decision.
  Assign readings that illustrate the concept in a specific company context.

## What to avoid

- Equation-heavy slides (use conceptual diagrams instead)
- Dense bullet lists (max 5 bullets, ideally 3)
- Citations cluttering the slide (move to reading list)
- Jargon without immediate definition
- Abstract theory without grounding example
