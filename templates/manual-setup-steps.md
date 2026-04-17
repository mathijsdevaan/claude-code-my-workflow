# Manual Setup Steps

**Status on this Mac:** DONE as of 2026-04-16.
- Open Sans and Fira Sans installed (confirmed via `fc-list`)
- `UCBerkeley_wordmark_white.pdf` placed in `Preambles/`
- Both themes compile cleanly end-to-end

**When to revisit:** setting up a new Mac, or if fonts / logo go missing.

---

A few one-time setup items require you to do manually. Once done, they apply to
every project that uses this template going forward.

---

## 1. Install fonts

The Beamer themes use two fonts that are not installed on your Mac by default.
Without them, the slides fall back to system fonts and look wrong (body text may
not render at all).

### Open Sans (required by the teaching theme)

1. Open https://fonts.google.com/specimen/Open+Sans
2. Click "Get font" (top right)
3. Click "Download all" in the popup
4. Unzip the downloaded file
5. Open Font Book (Spotlight → type "Font Book")
6. Drag the Open Sans `.ttf` files into Font Book
7. Quit Font Book

### Fira Sans (required by the academic theme)

1. Open https://fonts.google.com/specimen/Fira+Sans
2. Click "Get font"
3. Click "Download all"
4. Unzip
5. Drag the Fira Sans `.ttf` files into Font Book
6. Quit Font Book

### Verify installation

Open Terminal and run:

```bash
fc-list | grep -i "open sans\|fira sans" | head -5
```

If both appear in the output, you're set.

---

## 2. Restore the UC Berkeley wordmark logo

The teaching theme references a file called `UCBerkeley_wordmark_white` — a
white UC Berkeley logo that sits on the blue diagonal footer. This file is
currently missing from `Preambles/`.

### Where to get it

Option A (official): download from UC Berkeley Brand Center at
`brand.berkeley.edu/resources/`. Look for the white wordmark at 500px+ width.
Save as `UCBerkeley_wordmark_white.png` (or `.pdf`).

Option B (fallback): create a text-based placeholder using ImageMagick:
```bash
convert -size 600x60 xc:'#003262' \
  -font Helvetica-Bold -pointsize 32 -fill white \
  -gravity West -annotate +20+0 'UC BERKELEY' \
  Preambles/UCBerkeley_wordmark_white.png
```

### Install

Put the file in `Preambles/`:

```bash
mv ~/Downloads/UCBerkeley_wordmark_white.png \
   "~/Claude Projects/Claude Setup/Preambles/"
```

The teaching theme expects this specific filename. Don't rename it.

---

## 3. Verify everything compiles

Once fonts and logo are in place, test both themes:

```bash
cd "~/Claude Projects/Claude Setup"

# Teaching theme test (requires Open Sans + logo)
mkdir -p /tmp/theme-test
cp Preambles/beamerthemeUCBerkeleyTeaching.sty /tmp/theme-test/
cp Preambles/UCBerkeley_wordmark_white.png /tmp/theme-test/  # if installed
cat > /tmp/theme-test/test-teaching.tex <<EOF
\PassOptionsToPackage{table}{xcolor}
\documentclass[aspectratio=169]{beamer}
\usetheme{UCBerkeleyTeaching}
\title{Test Teaching}
\author{You}
\begin{document}
\begin{frame}\titlepage\end{frame}
\begin{frame}{Test frame}
\begin{itemize}
\item Bullet one
\item Bullet two
\end{itemize}
\end{frame}
\end{document}
EOF
cd /tmp/theme-test && xelatex -interaction=nonstopmode test-teaching.tex

# Academic theme test (requires Fira Sans)
cp "~/Claude Projects/Claude Setup/Preambles/beamerthemeUCBerkeleyAcademic.sty" /tmp/theme-test/
cat > /tmp/theme-test/test-academic.tex <<EOF
\PassOptionsToPackage{table}{xcolor}
\documentclass[aspectratio=169,10pt]{beamer}
\usetheme[progressbar=none,numbering=none]{metropolis}
\usepackage{UCBerkeleyAcademic}
\title{Test Academic}
\author{You}
\begin{document}
\maketitle
\begin{frame}{Test frame}
\begin{itemize}
\item Bullet one
\item Bullet two
\end{itemize}
\end{frame}
\end{document}
EOF
xelatex -interaction=nonstopmode test-academic.tex

# Open both PDFs
open test-teaching.pdf test-academic.pdf
```

If both PDFs render cleanly with proper fonts and (for teaching) the blue
diagonal footer with the Berkeley logo — you're done. This one-time setup
now benefits every project you start from this template.

---

## When to revisit

- If you switch Macs: repeat steps 1 and 2 on the new machine.
- If UC Berkeley updates its brand: replace the wordmark file.
- If Google Fonts updates Open Sans or Fira Sans: optional — current versions
  will keep working.
