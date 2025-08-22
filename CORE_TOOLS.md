# 🛠️ AI Orchestra 핵심 도구 10개

> 경량화 전략에 따라 핵심 도구만 유지
> 최종 업데이트: 2025-08-21

## 📡 통신 (2개)
1. **unified_ai_communicator.py** - 모든 AI 통신 통합
2. **smart_prompt_sender.py** - 엔터 문제 해결, 재시도 로직

## 📊 모니터링 (2개)
3. **pl-bot/pl-bot-v3.py** - Progress Leader Bot
4. **round5/real_kpi_tracker.py** - 실제 KPI 측정

## 🖥️ 세션 관리 (2개)
5. **iterm_session_manager.py** - iTerm2 세션 관리
6. **iterm_sessions.json** - 세션 구조 정의

## 📚 문서 (4개)
7. **COMPLETE_WORKFLOW_PROCESSES.md** - 모든 워크플로우
8. **PROJECT_DOCUMENTATION_INDEX.md** - 문서 인덱스
9. **ENHANCED_TASK_BREAKDOWN_R4-R10.md** - 마스터 플랜
10. **CLAUDE.md** - PM 지침 및 도구 위치

## ⚠️ 사용 규칙
- 새 기능 필요 시 → 먼저 이 10개에서 찾기
- 없으면 → 기존 도구 확장
- 절대 중복 생성 금지

## 🔍 빠른 참조
```python
# 통신
from unified_ai_communicator import UnifiedAICommunicator
from smart_prompt_sender import SmartPromptSender

# 모니터링
from pl_bot.pl_bot_v3 import PLBotV3
from round5.real_kpi_tracker import RealKPITracker

# 세션
from iterm_session_manager import ITermSessionManager
```