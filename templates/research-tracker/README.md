# Research Tracker Starter Kit

Lightweight hypothesis/insight/decision tracking, adapted from Scott Cunningham's
MixtapeTools GTD harness (https://github.com/scunning1975/MixtapeTools).

## To instantiate in a project

```bash
mkdir -p research/hypotheses research/insights research/decisions
cp templates/research-tracker/hypotheses-INDEX.md research/hypotheses/INDEX.md
cp templates/research-tracker/insights-INDEX.md   research/insights/INDEX.md
cp templates/research-tracker/decisions-INDEX.md  research/decisions/INDEX.md
```

Then file everything through `/research-log` — the skill enforces the format and
the status machine. `H00_example.md` and `insight-template.md` show the target
formats; don't copy them into projects.

## The core idea

Findings don't exist until filed. A hypothesis cannot reach `confirmed` without
passing a falsification test that was written down BEFORE the analysis ran
("Kills It"). The tracker is the shared external memory between you and Claude:
Claude forgets between sessions; the files don't.

See `.claude/rules/research-tracking.md` for the status machine rules.
