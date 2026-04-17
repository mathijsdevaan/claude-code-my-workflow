---
name: revise-resubmit
description: Build and maintain a revision tracker for journal R&Rs. Parses a reviewer letter into a structured tracker (comment → response → manuscript location → status). Tracks progress through the revision. At resubmission, generates formal response document and cover letter as PDF.
argument-hint: "[path to reviewer letter, or existing tracker file, or 'init']"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Bash", "AskUserQuestion"]
---

# Revise-and-Resubmit Tracker

Manage the revision cycle for a journal R&R. Each reviewer comment gets a planned response, a manuscript location, and a status. Produces a PDF response document at submission time.

**Input:** `$ARGUMENTS` — one of:
- Path to a reviewer letter (PDF, markdown, or text)
- Path to an existing `rnr/response_tracker.md` (to update)
- The word `init` (create empty tracker for manual entry)

**Output:**
- `rnr/response_tracker.md` — the living document
- `rnr/response_letter.pdf` — at submission, the formal response
- `rnr/cover_letter.pdf` — at submission, the editor cover letter

---

## Mode 1: Initial parse (new R&R)

If the input is a reviewer letter file, parse it into a structured tracker.

### Steps

1. **Read the reviewer letter.** If PDF, extract text. Find:
   - The editor's letter (summary of decision + main concerns)
   - Individual reviewer sections (usually 2–4 reviewers)
   - Comments within each reviewer (usually numbered)

2. **Split into discrete comments.** A "comment" is one distinct requested change or question. Long paragraph comments often contain multiple embedded requests — split them.

3. **Assign IDs.** Editor comments: E.1, E.2... Reviewer 1: R1.1, R1.2... etc.

4. **For each comment, extract:**
   - The verbatim text (quoted)
   - The type: Mandatory revision / Clarification / Suggestion / Concern
   - Estimated difficulty: Quick / Moderate / Substantial

5. **Draft the tracker file.** Do NOT fill in responses — those come from the user during revision. Save to `rnr/response_tracker.md`:

```markdown
# R&R Response Tracker
**Paper:** [Title]
**Journal:** [Name]
**Submitted:** [YYYY-MM-DD]
**R&R received:** [YYYY-MM-DD]
**Due:** [Deadline, if any]

## Editor

### E.1 [one-line summary]
- **Verbatim:** "[quoted text from editor letter]"
- **Type:** [Mandatory / Clarification / Suggestion / Concern]
- **Difficulty:** [Quick / Moderate / Substantial]
- **Planned response:** [TO FILL IN]
- **Manuscript location:** [section, page when done]
- **Status:** OPEN

## Reviewer 1

### R1.1 [one-line summary]
- **Verbatim:** "[quoted text]"
- **Type:** ...
- **Difficulty:** ...
- **Planned response:** [TO FILL IN]
- **Manuscript location:** [TO FILL IN]
- **Status:** OPEN

[etc.]
```

6. **Summarize.** Tell the user how many comments were extracted per reviewer and estimated overall difficulty.

---

## Mode 2: Update (existing tracker)

If the tracker file exists, the user is mid-revision. Help them update.

### Actions available
- Add a planned response to a specific comment
- Mark a comment status: OPEN → IN PROGRESS → DONE
- Fill in manuscript location after making the change
- Add a note or follow-up

Ask which comment, then make the update. Save atomically.

Periodically, offer a status report: X of N comments DONE, Y IN PROGRESS, Z OPEN. Flag any OPEN comments approaching the deadline.

---

## Mode 3: Submission preparation

When the user says the revision is done (or invokes `finalize`):

1. **Verify every comment has a response and location.** Any still OPEN? Flag them and stop — don't generate submission documents until everything is addressed.

2. **Generate `rnr/response_letter.md`** in the format journals expect. Typical structure:

```markdown
# Response to Reviewers
**[Paper Title]**
**Manuscript ID: [if assigned]**

We thank the editor and reviewers for their thoughtful engagement with our paper.
Below we respond to each comment, indicating the changes made and where they
appear in the revised manuscript.

---

## Editor

### E.1 [Summary]
**Comment:** "[verbatim]"

**Response:** [planned response — now the actual response after revision]

**Location in revised manuscript:** [section, page]

---

## Reviewer 1

### R1.1 [Summary]
...
```

3. **Generate `rnr/cover_letter.md`** — editor-facing cover letter:

```markdown
Dear [Editor name],

Thank you for the opportunity to revise our paper, "[Title]," for [Journal].
We have addressed all concerns raised by the editor and reviewers. The main
revisions include:

1. [Top substantive change]
2. [Second substantive change]
3. [Third substantive change]

A detailed response to each comment is included in the accompanying response
document.

We believe the paper is substantially stronger for these revisions, and we
thank the reviewers for their engagement.

Sincerely,
[Author name]
[Affiliation]
```

4. **Compile both to PDF.** Use pandoc or a minimal LaTeX template:

```bash
pandoc rnr/response_letter.md -o rnr/response_letter.pdf \
  --pdf-engine=xelatex \
  -V geometry:margin=1in \
  -V fontsize:11pt

pandoc rnr/cover_letter.md -o rnr/cover_letter.pdf \
  --pdf-engine=xelatex \
  -V geometry:margin=1in \
  -V fontsize:11pt
```

5. **Final check.** Verify the PDFs compiled and have the expected page count.

---

## Important Rules

1. **Never fabricate responses.** If a comment has no planned response, stop and ask the user.
2. **Verbatim quotes matter.** Reviewers want to see their comment quoted back.
3. **Status discipline.** Don't mark DONE until the user confirms both the response is written AND the manuscript change is made.
4. **Tracker is append-only (mostly).** Prefer adding notes to rewriting history. If a planned response changes, record the change rather than overwriting.
5. **Final output is PDF.** User preference — always compile the response letter and cover letter to PDF before handing back.
6. **Respect reviewer voice.** Don't paraphrase reviewer comments — quote them.
