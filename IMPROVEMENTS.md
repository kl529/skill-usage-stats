# Improvement Notes

## 버그 / 정확성 문제

### 1. 플러그인 스킬이 "삭제됐지만 사용됨"으로 잘못 분류됨

**현상:** 마켓플레이스로 설치한 스킬(`~/.claude/plugins/`)은 `commandName`에 기록되지만,
`get_installed_skills()`는 `~/.claude/skills/`만 스캔함.
→ 사용 기록은 있는데 설치 목록엔 없으니 "삭제됐지만 사용된 스킬"로 오분류됨.

**수정:** `installed_plugins.json`을 읽어서 플러그인 스킬도 설치 목록에 포함시켜야 함.

```python
PLUGINS_DIR = Path.home() / ".claude" / "plugins"
INSTALLED_PLUGINS_JSON = Path.home() / ".claude" / "installed_plugins.json"

def get_installed_plugins():
    try:
        data = json.loads(INSTALLED_PLUGINS_JSON.read_text())
        return {entry["name"] for entry in data}  # 실제 구조 확인 필요
    except (FileNotFoundError, KeyError, json.JSONDecodeError):
        return set()
```

### 2. README와 실제 동작 불일치

README의 "What it does" 5번: `Removes unused skills on your confirmation (including plugins)`
→ 실제로는 플러그인 삭제가 자동화되지 않음. 문구 수정 필요 (현재 README에는 이미 수정됨).

---

## 기능 개선

### 3. 마지막 사용일 추가

지금은 횟수만 보임. `.jsonl` 파일의 타임스탬프나 파일명에서 날짜를 추출하면
"마지막 사용: 2025-11-03" 같은 정보를 붙일 수 있음.

→ 오래 전에 많이 썼던 스킬과, 최근에 자주 쓰는 스킬을 구분하는 데 실질적으로 유용.

### 4. 날짜 범위 필터

전체 기간 통계만 있어서, 오래 전에 많이 썼던 스킬이 지금도 중요한 것처럼 보임.

```bash
python3 analyze.py --since 30d   # 최근 30일
python3 analyze.py --since 2025-01-01
```

### 5. 스킬 설명 출력

삭제 후보를 볼 때 스킬 이름만으로는 판단이 어려움.
`~/.claude/skills/<name>/skill.yml`의 `description` 필드를 읽어서 옆에 표시하면
Claude가 prompt.md에서 더 나은 삭제 이유를 제안할 수 있음.

```
  - autoplan          "자동으로 플래닝 단계를 생성"
  - brand-guidelines  "브랜드 가이드라인 체크"
```

### 6. 플러그인 삭제 자동화

`prompt.md` Step 3에서 플러그인 정리가 필요하다고만 안내하고 실제로는 안 함.
`analyze.py`에 `--delete <skill-name>` 플래그를 추가하거나,
별도 `cleanup.py`를 만들어서 아래를 처리:

1. `~/.claude/skills/<name>/` 디렉토리 삭제
2. `~/.claude/plugins/<name>/` 디렉토리 삭제
3. `installed_plugins.json`에서 해당 항목 제거

---

## 코드 품질

### 7. `commandName` 매칭의 잠재적 오탐

```python
if '"commandName"' not in line:
    continue
```

빠른 pre-filter로는 좋은 패턴이지만, 채팅 내용 중에 `"commandName"`이라는 문자열이 포함된 메시지가 있으면 JSON 파싱까지 진행됨. 실제로는 영향 거의 없지만, 필요하다면 `toolUseResult` 포함 여부도 같이 체크하는 게 더 정확:

```python
if '"commandName"' not in line or '"toolUseResult"' not in line:
    continue
```

### 8. `skill.yml` description이 한국어 전용

마켓플레이스 검색 가능성을 위해 영어 설명 추가를 고려:

```yaml
description: "Analyzes Claude Code session history to report skill usage frequency and suggest unused skills for cleanup. Triggers: '스킬 통계', 'skill stats', 'skill usage'."
```

---

## 우선순위 요약

| 우선순위 | 항목 |
|----------|------|
| 높음 | #1 플러그인 오분류 버그 |
| 높음 | #3 마지막 사용일 |
| 중간 | #5 스킬 설명 출력 |
| 중간 | #6 플러그인 삭제 자동화 |
| 낮음 | #4 날짜 필터 |
| 낮음 | #7 commandName 매칭 개선 |
| 낮음 | #8 skill.yml 영문 설명 |
