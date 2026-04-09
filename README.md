# skill-usage-stats

> Analyze your Claude Code session history to see which skills you actually use — and clean up the ones you don't.

**[한국어 버전 →](README.ko.md)**

---

## What it does

| Step | Action |
|------|--------|
| 1. Scan | Reads all session files in `~/.claude/projects/` |
| 2. Report | Shows each skill's invocation count and last-used date, sorted by frequency |
| 3. Highlight | Lists installed skills never used, with their descriptions |
| 4. Suggest | Recommends deletion candidates with reasons |
| 5. Remove | Deletes confirmed skills — handles both local skills and plugins automatically |

---

## Installation

**Via plugin marketplace:**
```bash
/plugin marketplace add kl529/skill-usage-stats
/plugin install skill-usage-stats@kl529
```

**Manual:**
```bash
cp -r skills/skill-usage-stats ~/.claude/skills/
```

---

## Usage

Trigger with any of these phrases:

```
skill stats
skill usage
스킬 통계
어떤 스킬 썼어
```

---

## Example output

```
# Claude Skill Usage Stats
Analyzed: 2026-04-09

## Skills with usage history (13)

 Count  Last used     Skill
--------------------------------------------------
    31  2026-04-08    qa
    13  2026-04-08    design-review
     7  2026-04-06    investigate
     2  2026-04-07    browse
     1  2026-03-19    azure-pr

## Never-used skills (155)

  - autoplan
  - brand-guidelines
  - frontend-design [plugin]
  - agent-architecture:bdi-mental-states [plugin]  # Explores BDI mental state…
  - ...

---
Installed: 168 (local 64 + plugins 104) | Used: 13 | Unused: 155
```

After the report, Claude suggests deletion candidates with a one-line reason each, then waits for your confirmation before removing anything.

---

## How it works

`analyze.py` scans every `.jsonl` session file under `~/.claude/projects/` for entries containing `commandName`. This field is written each time a skill is invoked — regardless of whether it was triggered via slash command or natural language.

```
~/.claude/projects/
  └── -project-name/
        └── <session-id>.jsonl   ← scanned here
```

Installed skills are discovered from two sources:
- **Local skills** — directories under `~/.claude/skills/`
- **Plugins** — entries in `~/.claude/plugins/installed_plugins.json`, resolved to their sub-skill names

Deletion via `--delete` handles both: removes local skill directories and cleans up `installed_plugins.json` + plugin cache for plugin skills.

---

## Known limitations

- **No date filtering** — stats are all-time; no "last 30 days" view.

---

## Requirements

- Python 3.6+
- Claude Code with session history in `~/.claude/projects/`

---

## License

MIT
