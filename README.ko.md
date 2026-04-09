# skill-usage-stats

> Claude Code 세션 히스토리를 분석해서 실제로 쓰는 스킬이 뭔지 파악하고, 안 쓰는 스킬을 정리해주는 도구.

**[English version →](README.md)**

---

## 뭘 하는 도구인가

| 단계 | 동작 |
|------|------|
| 1. 스캔 | `~/.claude/projects/` 안의 모든 세션 파일 읽기 |
| 2. 리포트 | 스킬별 호출 횟수를 빈도순으로 출력 |
| 3. 하이라이트 | 설치는 됐지만 한 번도 안 쓴 스킬 목록 표시 |
| 4. 제안 | 삭제 후보를 이유와 함께 추천 |
| 5. 삭제 | 확인 후 미사용 스킬 제거 |

---

## 설치

**플러그인 마켓플레이스:**
```bash
/plugin marketplace add kl529/skill-usage-stats
/plugin install skill-usage-stats@kl529
```

**수동 설치:**
```bash
cp -r skills/skill-usage-stats ~/.claude/skills/
```

---

## 사용법

아래 중 하나로 호출:

```
스킬 통계
어떤 스킬 썼어
skill stats
skill usage
```

---

## 출력 예시

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

리포트 출력 후, Claude가 삭제 후보를 한 줄 이유와 함께 제안하고, 확인을 받은 뒤 삭제를 진행합니다.

---

## 동작 원리

`analyze.py`가 `~/.claude/projects/` 아래의 모든 `.jsonl` 파일에서 `commandName` 필드를 찾습니다. 이 필드는 스킬이 호출될 때마다 기록되므로, 슬래시 커맨드든 자연어 트리거든 방법에 관계없이 모든 호출을 잡아냅니다.

```
~/.claude/projects/
  └── -project-name/
        └── <session-id>.jsonl   ← 여기를 스캔
```

설치된 스킬은 `~/.claude/skills/` 아래의 디렉토리 목록으로 파악합니다.

---

## 현재 한계

- **플러그인 미집계** — `~/.claude/plugins/`에 설치된 스킬은 설치 목록에 포함되지 않음
- **날짜 필터 없음** — 전체 기간 통계만 제공, "최근 30일" 같은 필터 없음
- **마지막 사용일 없음** — 몇 번 썼는지는 알 수 있지만 언제 썼는지는 모름
- **플러그인 삭제 미자동화** — `installed_plugins.json` 수정 + 캐시 정리는 자동으로 처리되지 않음

---

## 요구사항

- Python 3.6+
- `~/.claude/projects/`에 세션 히스토리가 있는 Claude Code

---

## 라이선스

MIT
