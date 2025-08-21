# 📋 AI Orchestra 완전 워크플로우 프로세스 가이드

> 최종 업데이트: 2025-08-21
> **중요**: 모든 작업 시작 전 이 문서를 확인하세요!

---

## 🚀 1. 프로젝트 시작 워크플로우

### 1.1 세션 시작 (매일 아침)
```bash
# Step 1: 문서 확인
cat PROJECT_DOCUMENTATION_INDEX.md

# Step 2: 세션 상태 확인
python3 iterm_session_manager.py

# Step 3: PL Bot 시작
python3 pl-bot/pl-bot-v3.py &

# Step 4: 통신 테스트
python3 unified_ai_communicator.py

# Step 5: GitHub 상태 확인
gh issue list -R ihw33/ai-orchestra-dashboard --state open
gh pr list -R ihw33/ai-orchestra-dashboard --state open
```

### 1.2 Daily Standup (09:00)
```markdown
1. [ ] PROJECT_DOCUMENTATION_INDEX.md 확인
2. [ ] TEAM_COLLABORATION_CHECKLIST.md 오픈
3. [ ] GitHub Issue에 Daily Standup 코멘트 작성
4. [ ] 각 AI 상태 체크 (PL Bot 확인)
5. [ ] 오늘의 작업 할당
```

---

## 📝 2. 새 기능 개발 워크플로우

### 2.1 계획 단계
```bash
# Step 1: 마스터 플랜 확인
cat ENHANCED_TASK_BREAKDOWN_R4-R10.md | grep "Round X"

# Step 2: 새 브랜치 생성
git checkout -b feature/round-X-feature-name

# Step 3: Issue 생성
gh issue create \
  --title "[Round X] 기능명" \
  --body "## 설명\n\n## 작업 목록\n- [ ] Task 1\n- [ ] Task 2" \
  --assignee @me
```

### 2.2 개발 단계
```python
# Step 1: TodoWrite 사용
from todo_manager import TodoWrite
todos = [
    {"content": "기능 설계", "status": "in_progress"},
    {"content": "코드 작성", "status": "pending"},
    {"content": "테스트", "status": "pending"},
    {"content": "PR 생성", "status": "pending"}
]
TodoWrite(todos)

# Step 2: AI 작업 할당
from unified_ai_communicator import UnifiedAICommunicator
comm = UnifiedAICommunicator()
comm.send_task_assignment("Gemini", "Frontend", "컴포넌트 개발")
comm.send_task_assignment("Codex", "Backend", "API 구현")

# Step 3: 실시간 모니터링
# PL Bot이 자동으로 추적
```

### 2.3 커밋 & PR 워크플로우
```bash
# Step 1: 변경사항 확인
git status
git diff

# Step 2: 커밋 (Thomas 규칙)
git add .
git commit -m "feat(round-5): KPI 시스템 구현

- 실제 측정 가능한 KPI 추가
- AI 통신 로그 기록
- 대시보드 업데이트

🤖 Generated with Claude Code"

# Step 3: PR 생성
gh pr create \
  --title "[Round 5] KPI 시스템 구현" \
  --body "## 변경사항\n- KPI 측정\n- 통신 로그\n\n## 테스트\n- [ ] 단위 테스트\n- [ ] 통합 테스트"

# Step 4: 리뷰 요청
gh pr edit PR_NUMBER --add-reviewer thomas,codex-ai
```

---

## 🤖 3. AI 통신 워크플로우

### 3.1 개별 AI 통신
```python
# Step 1: 세션 확인
from iterm_session_manager import ITermSessionManager
manager = ITermSessionManager()
session_info = manager.get_session_by_id('ORCH_CLAUDE')
print(f"위치: Tab {session_info['tab']}, Session {session_info['session']}")

# Step 2: 메시지 전송
import subprocess
script = f'''
tell application "iTerm2"
    tell current window
        tell tab {tab_number}
            tell session {session_number}
                write text "{message}"
            end tell
        end tell
    end tell
end tell
'''
subprocess.run(['osascript', '-e', script])
```

### 3.2 팀 브로드캐스트
```python
# 전체 공지
comm = UnifiedAICommunicator()
comm.broadcast_message(
    "📢 Round 5 시작: KPI 시스템 구현",
    exclude=["Claude"]  # PM 제외
)
```

---

## 📊 4. KPI 측정 워크플로우

### 4.1 실시간 KPI 추적
```python
# Step 1: KPI 트래커 시작
from round5.real_kpi_tracker import RealKPITracker
tracker = RealKPITracker()

# Step 2: 작업 할당 및 추적
tracker.send_task_to_ai("Gemini", 2, "Frontend 작업")
tracker.send_task_to_ai("Codex", 3, "Backend 작업")

# Step 3: GitHub 상태 체크
tracker.check_github_pr(61)

# Step 4: 리포트 생성
tracker.save_report("round5/kpi_report.json")
```

### 4.2 성과 분석
```bash
# KPI 리포트 확인
cat round5/kpi_report.json | jq '.summary'

# 70% 미달 시 롤백
if [ success_rate -lt 70 ]; then
    git checkout main
    git branch -D feature/round-X
    echo "⚠️ 롤백: 목표 미달성"
fi
```

---

## 🔄 5. 회고 워크플로우

### 5.1 Round 종료 회고
```markdown
## Round X 회고 템플릿

### 📊 정량 지표
- 계획 작업: X개
- 완료 작업: Y개
- 성공률: Z%
- 평균 응답 시간: N초

### ✅ 잘한 점
- 

### ❌ 개선 필요
- 

### 💡 다음 Round 제안
- 

### 팀원 피드백
- Gemini: 
- Codex:
- Claude:
- Cursor:
```

### 5.2 회고 프로세스
```bash
# Step 1: 회고 문서 생성
cat > roundX_retrospective.md << EOF
# Round X 회고
날짜: $(date)
참석: 전체 팀
EOF

# Step 2: KPI 데이터 추가
cat round5/kpi_report.json >> roundX_retrospective.md

# Step 3: GitHub Discussion 생성
gh issue create \
  --title "[회고] Round X" \
  --label "retrospective" \
  --body-file roundX_retrospective.md
```

---

## 🚨 6. 문제 해결 워크플로우

### 6.1 AI 응답 없음
```bash
# Step 1: PL Bot 상태 확인
cat pl-bot-report.json | jq '.team_status'

# Step 2: 개별 AI 체크
osascript -e 'tell application "iTerm2"
    tell current window
        tell tab 4
            tell session 1
                write text "echo STATUS_CHECK"
            end tell
        end tell
    end tell
end tell'

# Step 2-1: 엔터 미전송 문제 확인 (메시지는 보이나 실행 안됨)
# 증상: 프롬프트에 메시지는 있으나 엔터가 없어 실행되지 않음
osascript -e '
tell application "iTerm2"
    tell current window
        tell tab 4
            tell session 1
                if is at shell prompt then
                    return "엔터 필요"
                else if is processing then
                    return "처리 중"
                end if
            end tell
        end tell
    end tell
end tell'

# Step 2-2: 엔터 재전송 (기존 대책 활용)
# 방법 1: 직접 엔터 전송
osascript -e '
tell application "iTerm2"
    tell current window
        tell tab 4
            tell session 1
                write text ""  # 빈 텍스트 = 엔터
            end tell
        end tell
    end tell
end tell'

# 방법 2: Smart Prompt Sender 사용
python3 -c "
from smart_prompt_sender import SmartPromptSender
sender = SmartPromptSender()
sender.send_enter_key('ORCH_CLAUDE')  # 세션 ID에 엔터 전송
"

# Step 3: 백업 AI 활성화
python3 -c "
from pl_bot_v3 import PLBotV3
bot = PLBotV3()
bot._activate_backup('Codex')  # Codex 백업 활성화
"
```

### 6.2 프로세스 위반 감지
```python
# PL Bot이 자동 감지
violations = [
    "main 브랜치에서 직접 작업",
    "PR 없이 머지",
    "테스트 미실행",
    "리뷰 없이 머지"
]

# 리마인드 전송
for ai in ["Gemini", "Codex", "Claude"]:
    send_reminder(ai, "프로세스 준수: PR 생성 필수")
```

---

## 📁 7. 문서 관리 워크플로우

### 7.1 문서 업데이트
```bash
# Step 1: 인덱스 확인
cat PROJECT_DOCUMENTATION_INDEX.md

# Step 2: 문서 수정
vim DOCUMENT_NAME.md

# Step 3: 커밋
git add DOCUMENT_NAME.md
git commit -m "docs: 문서 업데이트 - 변경내용"
```

### 7.2 새 문서 생성
```bash
# Step 1: 템플릿 사용
cp templates/DOCUMENT_TEMPLATE.md NEW_DOCUMENT.md

# Step 2: 인덱스 업데이트
echo "- [NEW_DOCUMENT.md](./NEW_DOCUMENT.md)" >> PROJECT_DOCUMENTATION_INDEX.md

# Step 3: 커밋
git add .
git commit -m "docs: 새 문서 추가 - NEW_DOCUMENT"
```

---

## ⚡ 8. 긴급 상황 워크플로우

### 8.1 프로덕션 이슈
```bash
# Step 1: 롤백
git revert HEAD
git push origin main

# Step 2: 핫픽스 브랜치
git checkout -b hotfix/issue-name

# Step 3: 긴급 회의
python3 -c "
from unified_ai_communicator import UnifiedAICommunicator
comm = UnifiedAICommunicator()
comm.broadcast_message('🚨 긴급: 프로덕션 이슈 발생')
"
```

### 8.2 AI 전체 다운
```bash
# Manual fallback mode
echo "⚠️ Manual Mode Activated"
echo "1. GitHub에서 직접 작업"
echo "2. 로컬 개발 환경 사용"
echo "3. Thomas에게 즉시 보고"
```

---

## 📌 9. 체크리스트

### 매일 체크
- [ ] PROJECT_DOCUMENTATION_INDEX.md 확인
- [ ] PL Bot 실행 중
- [ ] 통신 시스템 정상
- [ ] GitHub Issue/PR 확인

### 작업 시작 전
- [ ] 브랜치 생성
- [ ] Issue 생성
- [ ] TodoWrite 설정
- [ ] AI 할당

### 작업 완료 후
- [ ] 테스트 실행
- [ ] 커밋 메시지 규칙
- [ ] PR 생성
- [ ] 리뷰 요청

### Round 종료 시
- [ ] KPI 리포트
- [ ] 회고 문서
- [ ] 70% 체크
- [ ] 다음 Round 계획

---

## 🔗 빠른 참조

- **메인 문서**: PROJECT_DOCUMENTATION_INDEX.md
- **협업 체크리스트**: TEAM_COLLABORATION_CHECKLIST.md
- **마스터 플랜**: ENHANCED_TASK_BREAKDOWN_R4-R10.md
- **세션 가이드**: iterm_session_quick_guide.md
- **통신 가이드**: CLI_CONNECTION_GUIDE.md

---

*"천천히 하더라도 확실하게 하자" - Thomas*
*"회고는 같이 해야지" - Thomas*
*"진짜로 쓸 수 있어야 해" - Thomas*