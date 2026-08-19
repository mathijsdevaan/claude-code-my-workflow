---
name: validate-bib
description: Validate bibliography entries against citations in all lecture files. Find missing entries and unused references. With --verify, also fact-check every entry against the actual published paper (one agent per entry).
argument-hint: "[--verify]"
allowed-tools: ["Read", "Grep", "Glob", "Bash", "Write", "Task"]
---

# Validate Bibliography

Cross-reference all citations in lecture files against bibliography entries.

## Steps

1. **Read the bibliography file** and extract all citation keys

2. **Scan all lecture files for citation keys:**
   - `.tex` files: look for `\cite{`, `\citet{`, `\citep{`, `\citeauthor{`, `\citeyear{`
   - `.qmd` files: look for `@key`, `[@key]`, `[@key1; @key2]`
   - Extract all unique citation keys used

3. **Cross-reference:**
   - **Missing entries:** Citations used in lectures but NOT in bibliography
   - **Unused entries:** Entries in bibliography not cited anywhere
   - **Potential typos:** Similar-but-not-matching keys

4. **Check entry quality** for each bib entry:
   - Required fields present (author, title, year, journal/booktitle)
   - Author field properly formatted
   - Year is reasonable
   - No malformed characters or encoding issues

5. **Report findings:**
   - List of missing bibliography entries (CRITICAL)
   - List of unused entries (informational)
   - List of potential typos in citation keys
   - List of quality issues

## Files to scan:
```
Slides/*.tex
Quarto/*.qmd
```

## Bibliography location:
```
Bibliography_base.bib  (repo root)
```


---

## Deep verification mode: `--verify`

Default mode (above) checks **internal consistency** — keys match, fields exist.
`--verify` checks **external accuracy** — does each entry correctly describe a
paper that actually exists? Adapted from Scott Cunningham's MixtapeTools
`/bibcheck` (https://github.com/scunning1975/MixtapeTools).

**Why one agent per entry:** a single agent verifying a whole .bib file gives
the first 10–15 entries careful treatment and pattern-matches the rest. Narrow
parallel agents defeat that attention decay; the bottleneck moves to
orchestration, which is what cheap parallel agents are for.

### Steps

1. Run the default mode first (steps 1–5 above). Only verified-used entries
   need deep verification unless the user asks for the full file.
2. Create a timestamped run directory — re-runs never clobber prior audits:
   ```bash
   mkdir -p "quality_reports/bibcheck_$(date +%Y%m%d_%H%M%S)"
   ```
   Copy the source `.bib` in as `input.bib`; split into one file per entry
   (brace-balanced — count `{`/`}`, don't split on blank lines).
3. **Launch one general-purpose agent per entry** (batch ~10 concurrent).
   Each agent's brief:
   - Identify the work from the entry (title + authors + year).
   - Find the canonical anchor: DOI or publisher landing page (WebSearch/WebFetch).
   - Cross-check EVERY field: authors (all of them, order, spelling), title,
     year, journal, volume, issue, pages, DOI.
   - Specifically test for **field mixing** — values that belong to a
     different paper by the same authors (right authors + right title +
     wrong journal/year is the classic hallucination pattern).
   - Return JSON: `{key, status: clean|corrected|unverifiable, one_sentence,
     canonical_url, issues: [], corrected_bib}`.
4. **Reviewer pass** (one agent): re-check every `unverifiable` entry,
   adjudicate suspicious corrections, flag disagreements.
5. Write to the run directory: `bibcheck_report.md` (table: key | status |
   issues | source URL) and `corrected.bib` (all entries, corrections applied).
6. **NEVER overwrite the source `.bib`** (`Bibliography_base.bib` is
   write-protected anyway). Present the diff; the user applies it.

### Scope discipline

- This checks that entries accurately describe real papers. It does NOT check
  whether a citation supports the claim it's attached to.
- Never write citations from scratch — inventing citations is exactly the
  failure mode this mode exists to catch.
