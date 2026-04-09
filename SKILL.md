---
name: skill-usage-stats
description: Analyze Claude Code session history to see which skills you actually use. Shows invocation counts, last-used dates, highlights never-used skills, and suggests deletion candidates. Handles both local skills and plugins. Trigger with "skill stats", "skill usage", "스킬 통계", or "어떤 스킬 썼어".
license: MIT
metadata:
  version: 1.0.0
  author: kl529
compatibility: Requires Python 3.x
---

# Skill Usage Stats

Analyze Claude Code session history to show skill usage statistics and help clean up unused skills.

## Step 1: Run the analyzer

```bash
python3 ~/.claude/skills/skill-usage-stats/analyze.py
```

Print the output as-is.

## Step 2: Suggest deletion candidates

From the "never used" list, identify candidates using these criteria:
- Unrelated to the user's current work environment
- Duplicates — multiple skills with overlapping functionality
- Names that clearly suggest no practical use case

For each candidate, show the skill name and a short one-line reason for deletion.

## Step 3: Delete confirmed skills

Once the user confirms which skills to delete, run:

```bash
python3 ~/.claude/skills/skill-usage-stats/analyze.py --delete skill1 skill2 ...
```

This handles everything automatically — both local skills (`~/.claude/skills/`) and plugins
(`installed_plugins.json` entry removal + cache directory deletion). Print the output as-is.
