# skill-usage-stats

A Claude Code skill that analyzes your session history to show which skills you actually use — and helps you clean up the ones you don't.

## What it does

1. **Scans** all session files in `~/.claude/projects/`
2. **Reports** skill usage frequency (how many times each skill was invoked)
3. **Highlights** skills installed but never used
4. **Suggests** candidates for deletion with reasons
5. **Removes** unused skills on your confirmation (including plugins)

## Usage

Just say any of:
- `스킬 통계`
- `어떤 스킬 썼어`
- `skill stats`
- `skill usage`

## Installation

### Via plugin marketplace

```bash
/plugin marketplace add kl529/skill-usage-stats
/plugin install skill-usage-stats@kl529
```

### Manual

```bash
cp -r skills/skill-usage-stats ~/.claude/skills/
```

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
   ...

## 한 번도 안 쓴 스킬 (52개)

  - autoplan
  - brand-guidelines
  ...

설치된 스킬: 64개 | 사용한 스킬: 12개 | 미사용: 52개
```

## Requirements

- Python 3.6+
- Claude Code with session history in `~/.claude/projects/`

## License

MIT
