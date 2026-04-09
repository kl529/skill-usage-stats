# Improvement Notes

## Remaining

### 1. No date filtering

Stats cover all time. There is no way to filter by recency (e.g. "last 30 days").
A skill used heavily six months ago looks the same as one used last week.

```bash
python3 analyze.py --since 30d
python3 analyze.py --since 2025-01-01
```

### 2. `commandName` pre-filter could produce false positives

```python
if '"commandName"' not in line:
    continue
```

This skips most lines cheaply, but will proceed to JSON parsing if a chat message
happens to contain the string `"commandName"`. Adding a second guard is more precise:

```python
if '"commandName"' not in line or '"toolUseResult"' not in line:
    continue
```

In practice this has negligible impact, but worth noting.

---

## Implemented

| # | Item | Status |
|---|------|--------|
| 1 | Plugin skills misclassified as "deleted but used" | Fixed — `installed_plugins.json` parsed, sub-skill IDs always use `plugin:sub` format |
| 2 | Last-used date | Done — `timestamp` field extracted from each session entry |
| 3 | Skill descriptions shown next to never-used list | Done — reads `description` from `skill.yml` / `SKILL.md` |
| 4 | Plugin deletion not automated | Done — `--delete` flag handles `installed_plugins.json` cleanup + cache removal |
