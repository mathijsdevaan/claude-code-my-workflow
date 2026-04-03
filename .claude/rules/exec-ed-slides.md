# Executive Education Slide Decks

**Trigger:** When the user says they are preparing an "exec ed" or "executive education" deck.

## Theme

- Use `\usetheme{UCBerkeley}` — file: `Preambles/beamerthemeUCBerkeley.sty`
- Compile with XeLaTeX (required for fontspec: Georgia + Open Sans)
- Logo file `UCBerkeley_wordmark_white` must be in the LaTeX search path

## Slide Style

- **Sparse slides** — prefer visuals and short phrases over paragraphs
- **Max 4-5 bullet points** per slide; each bullet ≤ 1.5 lines
- **Use `\smallframetitle`** when a slide needs more content space
- **Tables** use `\tableheadrow` + `\tableheadcol{}` for Berkeley-styled headers
- **Alternating row colors** are automatic (built into theme)

## Color Usage

- Frame titles: Medalist gold (automatic via theme)
- Body text: Berkeley Blue (automatic via theme)
- Use `\textcolor{FoundersRock}{...}` for inline accent/emphasis
- Use `\textcolor{CaliforniaGold}{...}` sparingly for highlights

## Typical Deck Structure

- Title slide (auto-styled by theme)
- Agenda / session overview
- Content sections with discussion prompts
- Case study or exercise slides
- Key takeaways / summary
- Q&A / discussion slide

## Audience Notes

- Executive education audiences are practitioners, not academics
- Minimize jargon; define technical terms when unavoidable
- Lead with "why this matters" before methods or theory
- Use real-world examples and case studies over formal proofs
- Encourage discussion — include prompt slides between sections
