# Skill Usage Stats

Claude Code 히스토리를 분석해서 스킬 사용 통계를 보여주고, 미사용 스킬 정리를 도와줍니다.

## Step 1: 분석 실행

```bash
python3 ~/.claude/skills/skill-usage-stats/analyze.py
```

결과를 그대로 출력합니다.

## Step 2: 삭제 후보 제안

"한 번도 안 쓴 스킬" 목록에서 아래 기준으로 삭제 후보를 추려서 제안합니다:
- 용도가 현재 작업 환경과 관련 없어 보이는 것
- 비슷한 기능의 스킬이 여러 개 있는 것 (중복)
- 이름만 봐도 쓸 일이 없어 보이는 것

각 후보마다 한 줄 설명과 삭제 이유를 붙여서 보여줍니다.

## Step 3: 삭제 진행

사용자가 삭제할 스킬을 확인해주면:

1. `~/.claude/skills/<skill-name>/` 디렉토리 삭제
2. 삭제 완료 목록 출력

플러그인(`~/.claude/plugins/`)은 `installed_plugins.json` 수정 + 캐시 디렉토리 삭제가 필요하므로, 플러그인 정리도 원하는지 물어봅니다.
