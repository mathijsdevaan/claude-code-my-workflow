# Data Storage Convention

**Raw and processed data live in Box, not in the project folder.**

The project folder holds code, writing, and documentation — small text files
that belong in git. Data (often large, sometimes confidential, frequently
updated) lives outside the project folder, synced via UC Berkeley Box.

## Paths

- **Per-project data:** `~/Library/CloudStorage/Box-Box/Research/[project-name]/`
  - `[project-name]` matches the project folder name exactly (e.g.,
    `Peer-Promotion-RCT`).
  - Inside this Box folder, use subdirectories as needed: `raw/`, `processed/`,
    `intermediate/`, `archive/`.

- **Shared reference data** (used across projects): if/when this becomes
  needed, use `~/Library/CloudStorage/Box-Box/Research/_shared/`.

## Project-folder layout

Inside each project, `data/` is a **gitignored** directory containing only:

- `PROVENANCE.md` — documents what's in the corresponding Box folder
- Small non-sensitive derived files (< 1 MB, public-OK) if genuinely useful to
  ship with the project
- **No raw data files. No large processed datasets.**

The `.gitignore` in every project prevents accidental commits of `data/raw/`,
`data/processed/`, `.RData`, `.rds`, `.dta`, large `.csv`, etc. The pre-commit
hook (`scripts/git-hooks/pre-commit`) is a second line of defense.

## Claude's defaults

When working with data in a project:

1. **Default data paths to Box**, using the project-name convention above.
   Construct paths like:
   ```r
   boxRoot <- "~/Library/CloudStorage/Box-Box/Research/Peer-Promotion-RCT"
   rawDat  <- fread(file.path(boxRoot, "raw", "employee_records_2025.csv"))
   ```

2. **Verify Box is synced locally** before running analysis:
   ```bash
   ls ~/Library/CloudStorage/Box-Box/Research/[project-name]/
   ```
   If the folder is missing or empty, Box may not have finished syncing.

3. **Never copy raw data into the project folder** without the user's explicit
   instruction. The pre-commit hook will block accidental commits, but don't
   rely on that as the only safeguard.

4. **Update `data/PROVENANCE.md`** when new data is added to Box or when
   processing steps change. This file is the only record of what's in Box,
   because Box contents aren't visible to Claude or to git.

## Data source patterns

Data reaches a project through three channels. Handle each consistently.

### 1. Uploaded (partner firm, RA, collaborator, email attachment)

- **Destination:** Box `raw/` subfolder, immediately on arrival
- **Do not modify the raw file.** Cleaning produces new files in `processed/`.
- **Document in `PROVENANCE.md`:** sender, date received, IRB protocol,
  contact person, access restrictions
- **If the file arrived via email:** save the email (or forward to yourself
  with a descriptive subject) so the provenance chain is recoverable

### 2. Downloaded from the web

Two sub-patterns depending on stability and size:

**2a. Small / static public datasets** (Census tables, Penn World Table,
one-off bulk downloads):
- Place in Box `raw/`, treat as Type 1
- Document the URL and download date in `PROVENANCE.md`

**2b. API calls, scraping, or dynamic downloads:**
- Write a download script: `code/00_download.R` (or `.py`)
- The **script** lives in git; the **data it produces** lives in Box `raw/`
- Document in `PROVENANCE.md`: script path, date of last successful run,
  any API keys required (store keys in environment variables or a
  gitignored config — never commit them)
- This pattern is the most reproducible. Prefer it when feasible.

### 3. Created inside the project

**3a. Experimental / survey data** (Qualtrics exports, RCT outcomes,
lab logs):
- Treat as Type 1 — goes to Box `raw/` on arrival, with IRB-aware access
  restrictions documented
- Often the strictest confidentiality; be deliberate

**3b. Simulated data** (Monte Carlo, synthetic benchmarks):
- If cheap to regenerate (< 1 minute): don't store. Code lives in git, data
  regenerates on demand.
- If expensive to regenerate: store in Box `processed/` with the generating
  script and the random seed documented in `PROVENANCE.md`

**3c. Derived datasets your own code produces** (merged, cleaned, reshaped,
matched):
- Always Box `processed/`, never the project folder
- Build via a named script (e.g., `code/01_clean.R`, `code/02_merge.R`)
- `PROVENANCE.md` records the script, input files, build date, and row count

### Decision rule, quick form

| Source | Where it goes | What's in git |
|---|---|---|
| Partner / email / RA upload | Box `raw/` | `PROVENANCE.md` entry |
| Public static dataset | Box `raw/` | `PROVENANCE.md` with URL |
| API / scraped / dynamic | Box `raw/` | Download script + `PROVENANCE.md` |
| Experimental output | Box `raw/` | `PROVENANCE.md` with IRB info |
| Cheap simulation | Not stored | Generating script only |
| Expensive simulation | Box `processed/` | Script + seed in `PROVENANCE.md` |
| Cleaned / merged derivative | Box `processed/` | Build script + `PROVENANCE.md` |

## Why Box (not Dropbox, not GitHub)

- **Institutional ownership.** UC Berkeley provides Box; it meets standard IRB
  and HIPAA-adjacent requirements.
- **Access controls.** Box folders can be shared with specific coauthors or
  RAs with read-only or read-write permissions.
- **Version history.** Box retains older file versions, useful if a cleaning
  step overwrites a raw file by mistake.
- **Not GitHub.** GitHub repos — even private ones — are the wrong place for
  confidential administrative data or individual-level records covered by IRB
  protocols.

## When the convention doesn't apply

- **Synthetic / toy data** used only for examples: may live in `data/` inside
  the project, un-gitignored if small and public.
- **Public datasets already in a stable location** (e.g., a World Bank CSV
  with a permanent URL): reference by URL in code, don't duplicate in Box.
- **Personal / non-research projects** (e.g., a side project): use whatever
  storage fits that project. This rule is for research.
