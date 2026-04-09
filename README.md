# skill-usage-stats

> Analyze your Claude Code session history to see which skills you actually use — and clean up the ones you don't.

**[한국어 버전 →](README.ko.md)**

---

## What it does

| Step | Action |
|------|--------|
| 1. Scan | Reads all session files in `~/.claude/projects/` |
| 2. Report | Shows each skill's invocation count, sorted by frequency |
| 3. Highlight | Lists skills installed but never used |
| 4. Suggest | Recommends deletion candidates with reasons |
| 5. Remove | Deletes unused skills on your confirmation |

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
스킬 통계        (Korean)
어떤 스킬 썼어   (Korean)
skill stats
skill usage
```

---

## Example output

```
# Claude Skill Usage Stats
분석일: 2026-04-09

## 사용 기록 있는 스킬 (12개)

  횟수  스킬
------------------------------
    31회  qa
    13회  design-review
     7회  investigate
     4회  review
     2회  commit

## 한 번도 안 쓴 스킬 (52개)

  - autoplan
  - brand-guidelines
  - canvas-design
  - ...

---
설치된 스킬: 64개 | 사용한 스킬: 12개 | 미사용: 52개
```

After the report, Claude suggests deletion candidates with a one-line reason each, then waits for your confirmation before removing anything.

---

## How it works

`analyze.py` scans every `.jsonl` file under `~/.claude/projects/` for entries containing `commandName`. This field is written each time a skill is invoked, capturing all invocations regardless of trigger method (slash command or natural language).

```
~/.claude/projects/
  └── -project-name/
        └── <session-id>.jsonl   ← scanned here
```

Installed skills are discovered by listing directories under `~/.claude/skills/`.

---

## Known limitations

- **Plugins not counted** — skills installed via `~/.claude/plugins/` are not included in the installed set.
- **No date filtering** — stats are all-time; no "last 30 days" view.
- **No last-used date** — shows how many times, not when.
- **Plugin deletion is manual** — cleanup of `installed_plugins.json` + plugin cache is not automated.

---

## Requirements

- Python 3.6+
- Claude Code with session history in `~/.claude/projects/`

---

## License

MIT
