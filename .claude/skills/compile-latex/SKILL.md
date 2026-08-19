---
name: compile-latex
description: Compile a Beamer LaTeX slide deck with XeLaTeX (3 passes + bibtex). Use when compiling lecture slides.
argument-hint: "[filename without .tex extension]"
allowed-tools: ["Read", "Bash", "Glob"]
---

# Compile Beamer LaTeX Slides

Compile a Beamer slide deck using XeLaTeX with full citation resolution.

## Steps

1. **Navigate to Slides/ directory** and compile with 3-pass sequence:

```bash
cd Slides
TEXINPUTS=../Preambles:$TEXINPUTS xelatex -interaction=nonstopmode $ARGUMENTS.tex
BIBINPUTS=..:$BIBINPUTS bibtex $ARGUMENTS
TEXINPUTS=../Preambles:$TEXINPUTS xelatex -interaction=nonstopmode $ARGUMENTS.tex
TEXINPUTS=../Preambles:$TEXINPUTS xelatex -interaction=nonstopmode $ARGUMENTS.tex
```

**Alternative (latexmk):**
```bash
cd Slides
TEXINPUTS=../Preambles:$TEXINPUTS BIBINPUTS=..:$BIBINPUTS latexmk -xelatex -interaction=nonstopmode $ARGUMENTS.tex
```

2. **Check for warnings — read the `.log` file directly:**
   - Read `Slides/$ARGUMENTS.log` itself; do NOT rely only on grepping terminal
     output. Grep on terminal output produces false positives from package
     description strings and can miss real warnings.
   - Look for: lines starting with `!` (errors), `Overfull \\hbox` /
     `Underfull \\hbox`, undefined citations, `Label(s) may have changed`,
     missing fonts.
   - Ignore lines that merely contain the word "warning" inside package
     metadata.
   - Report any issues found

3. **Open the PDF** for visual verification:
   ```bash
   open Slides/$ARGUMENTS.pdf          # macOS
   # xdg-open Slides/$ARGUMENTS.pdf    # Linux
   ```

4. **Report results:**
   - Compilation success/failure
   - Number of overfull hbox warnings
   - Any undefined citations
   - PDF page count

## Why 3 passes?
1. First xelatex: Creates `.aux` file with citation keys
2. bibtex: Reads `.aux`, generates `.bbl` with formatted references
3. Second xelatex: Incorporates bibliography
4. Third xelatex: Resolves all cross-references with final page numbers

## Circuit breaker (3 strikes)

If you have attempted **3 different approaches** to fix the *same* compile error
and it is not resolved, STOP. Do not keep editing. Instead:

1. Quote the exact error line from the `.log` file
2. List the 3 approaches you tried and why each failed
3. Ask the user how to proceed

"Same error" = the error persists at the same or a nearby line. A *new* error
elsewhere (e.g., a fresh overfull box after a fix) resets the counter. This rule
overrides zero-warning perfectionism: the cost of stopping to ask is 2 minutes;
the cost of spiraling is an hour of edits that make the file progressively worse.

## Important
- **Always use XeLaTeX**, never pdflatex
- **TEXINPUTS** is required: your Beamer theme lives in `Preambles/`
- **BIBINPUTS** is required: your `.bib` file lives in the repo root
