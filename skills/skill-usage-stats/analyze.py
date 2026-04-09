#!/usr/bin/env python3
"""
Claude Code Skill Usage Analyzer
~/.claude/projects/ 의 모든 세션 파일을 분석해서 스킬 사용 통계를 출력합니다.
"""

import json
import os
import sys
from collections import Counter
from pathlib import Path
from datetime import datetime

PROJECTS_DIR = Path.home() / ".claude" / "projects"
SKILLS_DIR = Path.home() / ".claude" / "skills"


def get_installed_skills():
    if not SKILLS_DIR.exists():
        return set()
    return {d.name for d in SKILLS_DIR.iterdir() if d.is_dir()}


def get_skill_usage():
    usage = Counter()
    if not PROJECTS_DIR.exists():
        return usage

    for jsonl_file in PROJECTS_DIR.rglob("*.jsonl"):
        try:
            with open(jsonl_file, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    if '"commandName"' not in line:
                        continue
                    try:
                        data = json.loads(line)
                        cmd = data.get("toolUseResult", {}).get("commandName")
                        if cmd:
                            usage[cmd] += 1
                    except (json.JSONDecodeError, AttributeError):
                        continue
        except (IOError, OSError):
            continue

    return usage


def main():
    installed = get_installed_skills()
    usage = get_skill_usage()

    # 설치된 스킬 중 사용된 것
    used = {k: v for k, v in usage.items() if k in installed}
    # 사용됐지만 이미 삭제된 것
    deleted_but_used = {k: v for k, v in usage.items() if k not in installed}
    # 설치됐지만 한 번도 안 쓴 것
    never_used = installed - set(usage.keys())

    print(f"# Claude Skill Usage Stats")
    print(f"분석일: {datetime.now().strftime('%Y-%m-%d')}\n")

    print(f"## 사용 기록 있는 스킬 ({len(used)}개)\n")
    if used:
        print(f"{'횟수':>6}  스킬")
        print("-" * 30)
        for skill, count in sorted(used.items(), key=lambda x: -x[1]):
            print(f"{count:>6}회  {skill}")
    else:
        print("(없음)")

    print(f"\n## 한 번도 안 쓴 스킬 ({len(never_used)}개)\n")
    for skill in sorted(never_used):
        print(f"  - {skill}")

    if deleted_but_used:
        print(f"\n## 삭제됐지만 사용 기록 있었던 스킬 ({len(deleted_but_used)}개)\n")
        for skill, count in sorted(deleted_but_used.items(), key=lambda x: -x[1]):
            print(f"  {count:>4}회  {skill}")

    print(f"\n---")
    print(f"설치된 스킬: {len(installed)}개 | 사용한 스킬: {len(used)}개 | 미사용: {len(never_used)}개")


if __name__ == "__main__":
    main()
