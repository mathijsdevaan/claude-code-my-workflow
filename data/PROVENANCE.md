# Data Provenance

**Actual data lives in Box**, not in this folder. This file documents what's
in the project's Box folder, because Box contents aren't visible to git or
Claude without a local sync check.

**Box location:** `~/Library/CloudStorage/Box-Box/Research/[PROJECT-NAME]/`
**Last sync verified:** [YYYY-MM-DD — run `ls` on the Box path above]

---

## Raw data

### raw/[filename.ext]
- **Source:** [partner firm / agency / survey / public dataset]
- **Received:** [YYYY-MM-DD, via email / secure transfer / API / download]
- **Contact:** [person name + email]
- **IRB protocol:** [number, or "n/a" for public data]
- **Access restrictions:** [who is allowed to see raw; any coauthor carve-outs]
- **Coverage:** [time period, geography, sample definition]
- **Known issues:** [coding changes, missing periods, schema quirks]

---

## Processed / derived data

### processed/[filename.ext]
- **Built by:** [path/to/script.R, specific functions if non-obvious]
- **Input:** [raw/source_file.csv and any intermediate inputs]
- **Built on:** [YYYY-MM-DD]
- **Row count:** [N]
- **Unit of observation:** [person / firm / person-year / etc.]
- **Key variables:** [list the main columns and their types]
- **Notes:** [assumptions made during cleaning, decisions worth flagging]

---

## Intermediate files

If analysis produces intermediate files that are expensive to rebuild
(e.g., large `.rds` caches, matched datasets), document them here the same way.

---

## Archive

When a dataset is superseded (e.g., partner re-extracts with a corrected
variable), move the old file to `archive/` in Box and note the reason here.

### archive/[old_filename.ext_YYYYMMDD]
- **Why archived:** [reason]
- **Replaced by:** [new filename]
- **Don't use for new analysis**

---

## Update discipline

Update this file whenever:
- New raw data arrives in Box
- A new processed dataset is built
- A partner replaces a file you're already using
- IRB scope changes affecting what's accessible
- Anything about the data changes that future-you won't remember
