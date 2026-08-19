---
paths:
  - "Slides/**/*.tex"
  - "Figures/**/*.tex"
---

# TikZ Visual Quality Standards

**Every TikZ diagram must be visually polished before it is considered complete.**

## Compute, Never Eyeball

Claude cannot eyeball where a curve passes or whether a label fits a gap. The
compiler catches none of these collisions. Replace visual intuition with
arithmetic. (Anti-collision math adapted from Scott Cunningham's MixtapeTools,
https://github.com/scunning1975/MixtapeTools.)

### Coordinate map (mandatory)

Write a `% Coordinate map:` comment block before every `tikzpicture`, listing
each node/shape with its position and size. This is what makes the arithmetic
below checkable.

```latex
% Coordinate map:
%   boxA: center (0,0), 5cm wide -> right edge x=2.5
%   boxB: center (6.5,0), 5cm wide -> left edge x=4.0
%   curve A->B: bend left=35, chord 6.5cm
\begin{tikzpicture}
```

### Bézier curves (every `bend`)

For each curved arrow: `max_depth = (chord/2) × tan(bend_angle/2)`, and
`safe_distance = max_depth + 0.5cm`. Any label closer than `safe_distance` to
the baseline, on the side the curve bends, must move.

| Bend angle | tan(angle/2) |
|-----------|-------------|
| 20° | 0.176 |
| 25° | 0.222 |
| 30° | 0.268 |
| 35° | 0.315 |
| 40° | 0.364 |
| 45° | 0.414 |

Worked example — arrow across 8.4cm with `bend left=35`: half-chord 4.2 ×
0.315 = depth **1.32cm**; safe distance **1.82cm**; a label "below" the
baseline must be at y ≤ −1.82, not −1.5. Also check whether the curve's sweep
crosses any other arrow; if so, bend the other direction.

### Label width vs. gap (every label between nodes)

`usable = (center-to-center) − halfwidth_A − halfwidth_B − 0.6cm`.
Estimate label width by character count:

| Font size | Width per character |
|-----------|-------------------|
| `\scriptsize` | 0.10cm |
| `\footnotesize` | 0.12cm |
| `\small` | 0.15cm |
| `\normalsize` | 0.18cm |

Bold: +10%. Monospace: +15%. If estimated width > usable space, the collision
is guaranteed — move the label above/below or shorten it.

### Plotted curves

For `plot ({A*\x},{B + C*exp(-\x*\x/2)})`-style curves, compute
`y = B + C·exp(−(X/A)²/2)` at every x where another object sits; require
0.3cm clearance. Peak is `B + C` at x = 0.

### Minimum clearances

| Object pair | Minimum |
|---|---|
| Label ↔ label | 0.3cm |
| Label ↔ axis line | 0.3cm |
| Label ↔ drawn shape boundary | 0.4cm |
| Arrow origin ↔ box edge | 0.15cm |
| Any object ↔ slide edge | 0.5cm |

Don't match y-coordinates across different shapes — a y that clears one shape
may sit inside another. Compute each boundary independently.

### Two LaTeX traps

- **Scaling:** `scale=0.8` shrinks coordinates but not text, creating invisible
  collisions. If you must scale, use
  `[scale=0.8, every node/.style={scale=0.8}]`; better, design at intended size.
- **Parameterized styles inside frames:** never define TikZ styles taking `#1`
  arguments inside a Beamer frame — the frame parser eats `#` and the errors
  cascade and resist all downstream fixes. Put `\tikzset{}` in the preamble.

## Label Positioning

- Labels must NEVER overlap with curves, lines, dots, braces, or other labels
- When two labels are near the same vertical position, stagger them
- Group labels: right of final data point
- Axis labels: at arrow tips
- Annotation labels: adjacent to braces/arrows, outside data area
- Use consistent font size

## Visual Semantics

- **Solid dots/lines** = observed outcomes, realized paths
- **Hollow circles/dashed lines** = counterfactual outcomes, unrealized paths
- Use consistent colors for semantic meaning (positive, negative, neutral)
- Define colors in your Beamer theme for reuse

### Line Weights
- Axes: `thick`
- Data lines: `thick`
- Annotation arrows: `thick` (NOT `very thick`)
- Grid/reference lines: `dashed, gray!40`

## Spacing and Proportions

- Standard scale: `[scale=1.1]` for full-width diagrams
- Dot radius: `4pt` for data points
- Minimum 0.2 units between any label and nearest graphical element
- Axes extend beyond all data points

## Checklist

```
[ ] No label-label overlaps
[ ] No label-curve overlaps
[ ] Consistent dot style (solid=observed, hollow=counterfactual)
[ ] Consistent line style (solid=observed, dashed=counterfactual)
[ ] Color semantics correct
[ ] Arrow annotations point FROM label TO feature
[ ] Axes extend beyond all data points
[ ] Labels legible at presentation size
```

## Single Source of Truth

**The Beamer `.tex` file is the authoritative source for ALL TikZ diagrams.**
Edit TikZ in the Beamer file FIRST, then copy verbatim to `extract_tikz.tex`.
