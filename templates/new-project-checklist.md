# Starting a New Project from This Template

This is the step-by-step procedure for starting a new project — a research paper,
an MBA course, or an exec ed session — using this template as the base.

Follow it every time you start something new. Takes about 5 minutes.

---

## What git is, in one paragraph

Git tracks every version of your files over time. Every time you "commit," git
saves a snapshot you can return to. It runs locally on your Mac — nothing leaves
your computer unless you explicitly push to GitHub. For solo research work on
your own machine, git's job is: give you an undo button that works across weeks,
and let you see what changed since yesterday. You don't need to master git — you
need about 6 commands, listed below.

---

## Step 1: Copy the template

Open Terminal. Navigate to where you keep your projects:

```bash
cd ~/Claude\ Projects/
```

Copy the template folder to a new name. Pick something descriptive — the paper's
short title, the course name, or the session client:

```bash
cp -R "Claude Setup" "Peer-Promotion-RCT"
cd "Peer-Promotion-RCT"
```

---

## Step 2: Start a fresh git history

The template folder already has a git history (from when you forked it). You
want a new project to start with a blank history — "this is day one of this
project." So we delete the template's git history and start a new one:

```bash
rm -rf .git
git init
```

This only affects your copy. The original "Claude Setup" template still has its
full history intact.

---

## Step 3: Install the large-file commit guard

The template includes a pre-commit hook that blocks accidental commits of large
files or data formats (`.RData`, `.rds`, large CSVs, etc.). Activate it for this
project:

```bash
git config core.hooksPath scripts/git-hooks
```

This tells git to look in `scripts/git-hooks/` for hooks. The guard is now
active for every commit in this project. If you try to commit a data file, it
will block you with a clear message and an override option.

---

## Step 4: Customize CLAUDE.md

Open `CLAUDE.md` in your editor. Make three edits:

1. **Replace the project name placeholder.** Find:
   ```
   **Project:** [Project name — replace when copying this template for a new project]
   ```
   Change to your project name:
   ```
   **Project:** Peer Promotion RCT
   ```

2. **Set the slide style.** Find:
   ```
   **Slide style:** [teaching | academic — pick one; determines theme + conventions]
   ```
   Replace with either `teaching` or `academic`:
   ```
   **Slide style:** academic
   ```

3. **Uncomment one "Current State" variant.** At the bottom of `CLAUDE.md`
   there are three commented-out state blocks (research project / MBA course /
   exec ed session). Uncomment the one that matches, fill it in, and **delete
   the other two**.

---

## Step 5: Clean out template leftovers

These files came from the template but aren't yours:

```bash
rm -f quality_reports/session_logs/*.md
rm -f quality_reports/plans/*.md
rm -f references/reference-deck-*.pdf   # only if you don't want the exemplars
```

---

## Step 6: Set up the Box data folder (if this project uses data)

**Skip this step if the project has no datasets** (e.g., a pure theory paper,
a teaching deck, a non-empirical exec-ed session).

Otherwise:

1. Open Box (browser or Mac app).
2. Create a folder in Box at `Research/[project-name]/` — match the project
   folder name exactly (e.g., `Peer-Promotion-RCT`).
3. Inside the Box folder, create subfolders as needed: `raw/`, `processed/`,
   `intermediate/`, `archive/`.
4. Verify the folder syncs to your Mac. In Terminal:
   ```bash
   ls ~/Library/CloudStorage/Box-Box/Research/[project-name]/
   ```
   If the folder appears, Box has synced it locally. If not, wait a minute
   and retry, or open the Box app to force sync.
5. In this project folder, open `data/PROVENANCE.md` and fill in:
   - The Box path at the top
   - Today's date as "Last sync verified"

Data files (raw, processed, intermediate) live **in Box, not in this
project folder**. The `.gitignore` and pre-commit hook are configured to
prevent accidental commits of data. See `.claude/rules/data-storage.md`
for the full convention.

---

## Step 7: Make your first commit

A "commit" is a snapshot git saves. Your first commit marks "the moment this
project was born."

First, tell git to track everything in the folder:

```bash
git add .
```

The `.` means "everything in this current folder." Then save the snapshot:

```bash
git commit -m "Initial setup from Claude Setup template"
```

The `-m "..."` part is the commit message — a short note about what this
snapshot contains. Future-you will thank present-you for meaningful messages.

If you get an error about user.email or user.name being missing, run:

```bash
git config user.email "your@email.edu"
git config user.name "Your Name"
```

(These go into this project's config only, not globally.)

---

## Step 8: Set up GitHub backup

Now link this project to a private GitHub repo so commits are backed up off your
Mac. Skip this only if you genuinely don't want cloud backup (rare — it's free
and protects against laptop loss, disk failure, accidental `rm -rf`).

### 8a. Create the GitHub repo

1. Go to https://github.com/new
2. Repository name: match your folder name (e.g., `Peer-Promotion-RCT`)
3. Visibility: **Private** (research data, drafts, and notes do not belong on
   public GitHub)
4. Do NOT initialize with README, .gitignore, or license — your local repo
   already has content and adding these on GitHub creates merge conflicts
5. Click "Create repository"
6. On the next page, copy the HTTPS URL — it looks like:
   `https://github.com/yourusername/Peer-Promotion-RCT.git`

### 8b. Link local to remote

In Terminal, in your project folder:

```bash
git remote add origin https://github.com/yourusername/Peer-Promotion-RCT.git
```

The word `origin` is the conventional name for "my main remote." You're telling
git "when I say `origin`, I mean this GitHub URL."

### 8c. First push

```bash
git push -u origin main
```

Breakdown:
- `-u origin main` sets the **default** remote and branch, so future pushes can
  be just `git push` (no arguments)
- You only need the `-u` flag once, on the first push

If this is your first push from this Mac, GitHub will ask for authentication.
The modern method is a **Personal Access Token (PAT)** — a password substitute.
See https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens
for the current setup procedure. Save the PAT in your Mac keychain when
prompted, and you won't need to re-enter it.

### 8d. Verify

```bash
git status
```

Should say "Your branch is up to date with 'origin/main'." That means your local
and GitHub are in sync.

Open your GitHub repo in a browser — you should see your files.

---

# Day-to-day git workflow

You've made your initial commit and set up backup. As you work, save snapshots
periodically and push them to GitHub. A reasonable rhythm for solo research:

- **Mid-session:** `git add .` + `git commit -m "..."` after finishing a
  meaningful chunk of work (not every file save)
- **Before a risky change:** commit first so you can roll back
- **End of day:** one final commit AND a push to GitHub for off-site backup

Each snapshot:

```bash
git add .
git commit -m "Describe what this snapshot contains"
```

Example commit messages:
- "Clean raw employee data, drop test accounts"
- "Add balance table for baseline sample"
- "Rewrite §3 identification argument"
- "Respond to R1.2 comment in manuscript"

End-of-day backup:

```bash
git push
```

That's it. One command, no arguments (because `-u` was set in Step 8c). You
don't need branches, merges, pull requests, or anything else for solo research
work. Just: commit during the day, push at the end.

**If you forget to push for a few days:** no harm done. All your commits still
live locally. `git push` catches GitHub up with everything at once.

---

# When something goes wrong

These two commands get you out of most trouble:

```bash
# "What changed since my last commit?"
git status

# "Show me the last few snapshots I made"
git log --oneline -10
```

If you mess up a file and want to go back to the last committed version:

```bash
git checkout -- path/to/file.R
```

If you staged a file with `git add` but want to un-stage it (not delete it):

```bash
git reset HEAD path/to/file
```

If you're deeply confused, ask Claude. Don't Google git — you'll end up on
Stack Overflow answers from 2013 that use outdated commands and make things
worse.

---

# What NOT to do

- **Don't `git push --force`** — unless you know exactly what this does,
  it can overwrite history irretrievably.
- **Don't commit data files** — the pre-commit hook will block you anyway.
  But be deliberate about what you stage with `git add`.
- **Don't use `git reset --hard`** — this throws away uncommitted work.
  Ask Claude first if you're considering it.

---

## Reference: commands you actually need

| Command | What it does |
|---------|-------------|
| `git status` | Show what's changed since last commit |
| `git add .` | Stage all changes |
| `git commit -m "msg"` | Save a snapshot |
| `git log --oneline -10` | Show last 10 commits |
| `git diff` | Show line-by-line what changed |
| `git checkout -- file` | Revert a file to last committed version |

That's it. Everything else you can Google when you need it.
