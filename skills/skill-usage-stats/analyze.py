#!/usr/bin/env python3
"""
Claude Code Skill Usage Analyzer
Scans ~/.claude/projects/ session files to report skill usage statistics.

Usage:
  python3 analyze.py                        # show stats
  python3 analyze.py --delete skill1 ...   # delete skills (supports plugins)
"""

import json
import re
import shutil
import sys
from collections import defaultdict
from pathlib import Path
from datetime import datetime

PROJECTS_DIR = Path.home() / ".claude" / "projects"
SKILLS_DIR = Path.home() / ".claude" / "skills"
PLUGINS_JSON = Path.home() / ".claude" / "plugins" / "installed_plugins.json"


# ---------------------------------------------------------------------------
# Discovery
# ---------------------------------------------------------------------------

def get_local_skills():
    if not SKILLS_DIR.exists():
        return set()
    return {d.name for d in SKILLS_DIR.iterdir() if d.is_dir()}


def get_installed_plugins():
    """
    Returns {skill_id: {"plugin_key": str, "install_path": str}}

    skill_id examples:
      "frontend-design"                     (single-skill plugin)
      "agent-architecture:bdi-mental-states" (multi-skill plugin)
    """
    result = {}
    if not PLUGINS_JSON.exists():
        return result

    try:
        data = json.loads(PLUGINS_JSON.read_text())
        for plugin_key, installs in data.get("plugins", {}).items():
            if not installs:
                continue
            base_name = plugin_key.split("@")[0]
            install_path = Path(installs[0]["installPath"])
            skills_subdir = install_path / "skills"

            if not skills_subdir.exists():
                result[base_name] = {"plugin_key": plugin_key, "install_path": str(install_path)}
                continue

            for sub in skills_subdir.iterdir():
                if not sub.is_dir():
                    continue
                skill_id = f"{base_name}:{sub.name}"
                result[skill_id] = {"plugin_key": plugin_key, "install_path": str(install_path)}

    except (json.JSONDecodeError, KeyError, IndexError):
        pass

    return result


def get_skill_description(skill_name, plugin_info=None):
    """Read the description field from skill.yml. Returns '' if not found."""
    yml_path = SKILLS_DIR / skill_name / "skill.yml"

    if not yml_path.exists() and plugin_info:
        sub = skill_name.split(":", 1)[1] if ":" in skill_name else skill_name.split(":")[0]
        yml_path = Path(plugin_info["install_path"]) / "skills" / sub / "skill.yml"

    if not yml_path.exists():
        return ""

    try:
        text = yml_path.read_text(encoding="utf-8")
        m = re.search(r'^description:\s*["\']?(.*?)["\']?\s*$', text, re.MULTILINE)
        if m:
            desc = m.group(1).strip()
            return (desc[:60] + "…") if len(desc) > 60 else desc
    except (IOError, OSError):
        pass
    return ""


# ---------------------------------------------------------------------------
# Usage stats
# ---------------------------------------------------------------------------

def get_skill_usage():
    """
    Returns {skill_name: {"count": int, "last_used": "YYYY-MM-DD"}}
    """
    usage = defaultdict(lambda: {"count": 0, "last_used": ""})
    if not PROJECTS_DIR.exists():
        return dict(usage)

    for jsonl_file in PROJECTS_DIR.rglob("*.jsonl"):
        try:
            with open(jsonl_file, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    line = line.strip()
                    if not line or '"commandName"' not in line:
                        continue
                    try:
                        data = json.loads(line)
                        cmd = data.get("toolUseResult", {}).get("commandName")
                        if not cmd:
                            continue
                        usage[cmd]["count"] += 1
                        ts = data.get("timestamp", "")
                        if ts:
                            date = ts[:10]  # "YYYY-MM-DD"
                            if date > usage[cmd]["last_used"]:
                                usage[cmd]["last_used"] = date
                    except (json.JSONDecodeError, AttributeError):
                        continue
        except (IOError, OSError):
            continue

    return dict(usage)


# ---------------------------------------------------------------------------
# Deletion
# ---------------------------------------------------------------------------

def delete_skills(names, plugin_map):
    """
    Delete skills by name. Handles both local skills and plugins.
    For plugins, removes the entry from installed_plugins.json and
    deletes the cache directory.
    """
    deleted = []
    errors = []
    plugin_keys_to_remove = {}  # {plugin_key: install_path}

    for name in names:
        skill_path = SKILLS_DIR / name
        if skill_path.exists():
            try:
                shutil.rmtree(skill_path)
                deleted.append(name)
            except OSError as e:
                errors.append(f"{name}: {e}")
        elif name in plugin_map:
            info = plugin_map[name]
            plugin_keys_to_remove[info["plugin_key"]] = info["install_path"]
            deleted.append(name)
        else:
            errors.append(f"{name}: not found in skills or plugins")

    if plugin_keys_to_remove and PLUGINS_JSON.exists():
        try:
            data = json.loads(PLUGINS_JSON.read_text())
            plugins = data.get("plugins", {})
            for pk, install_path in plugin_keys_to_remove.items():
                plugins.pop(pk, None)
                ip = Path(install_path)
                if ip.exists():
                    shutil.rmtree(ip)
            PLUGINS_JSON.write_text(json.dumps(data, indent=2, ensure_ascii=False))
        except (OSError, json.JSONDecodeError) as e:
            errors.append(f"plugin cleanup error: {e}")

    return deleted, errors


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if "--delete" in sys.argv:
        idx = sys.argv.index("--delete")
        to_delete = sys.argv[idx + 1:]
        if not to_delete:
            print("Usage: analyze.py --delete <skill1> <skill2> ...")
            sys.exit(1)
        plugin_map = get_installed_plugins()
        deleted, errors = delete_skills(to_delete, plugin_map)
        for name in deleted:
            print(f"Deleted: {name}")
        for err in errors:
            print(f"Error:   {err}")
        return

    local_skills = get_local_skills()
    plugin_map = get_installed_plugins()
    installed = local_skills | set(plugin_map.keys())
    usage = get_skill_usage()

    used = {k: v for k, v in usage.items() if k in installed}
    deleted_but_used = {k: v for k, v in usage.items() if k not in installed}
    never_used = installed - set(usage.keys())

    print("# Claude Skill Usage Stats")
    print(f"분석일: {datetime.now().strftime('%Y-%m-%d')}\n")

    # --- Used skills ---
    print(f"## 사용 기록 있는 스킬 ({len(used)}개)\n")
    if used:
        print(f"{'횟수':>6}  {'마지막 사용':12}  스킬")
        print("-" * 50)
        for skill, info in sorted(used.items(), key=lambda x: -x[1]["count"]):
            last = info["last_used"] or "-"
            print(f"{info['count']:>6}회  {last:12}  {skill}")
    else:
        print("(없음)")

    # --- Never used skills ---
    print(f"\n## 한 번도 안 쓴 스킬 ({len(never_used)}개)\n")
    for skill in sorted(never_used):
        tag = " [plugin]" if skill in plugin_map else ""
        desc = get_skill_description(skill, plugin_map.get(skill))
        desc_str = f"  # {desc}" if desc else ""
        print(f"  - {skill}{tag}{desc_str}")

    # --- Previously used but now deleted ---
    if deleted_but_used:
        print(f"\n## 삭제됐지만 사용 기록 있었던 스킬 ({len(deleted_but_used)}개)\n")
        for skill, info in sorted(deleted_but_used.items(), key=lambda x: -x[1]["count"]):
            print(f"  {info['count']:>4}회  {info['last_used'] or '-':12}  {skill}")

    plugin_count = len(plugin_map)
    print(f"\n---")
    print(
        f"설치된 스킬: {len(installed)}개 "
        f"(로컬 {len(local_skills)}개 + 플러그인 {plugin_count}개) | "
        f"사용한 스킬: {len(used)}개 | 미사용: {len(never_used)}개"
    )


if __name__ == "__main__":
    main()
