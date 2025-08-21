# 🎯 PM 운영 가이드

## 📋 PM 필수 체크리스트

### 1️⃣ 새 팀원 온보딩
새로운 AI CLI 팀원이 참가하면 반드시 다음을 수행:

```applescript
# 1. 팀원 초기 설정 메시지
"안녕하세요 [팀원명]님! 
프로젝트: /Users/m4_macbook/Projects/ai-orchestra-dashboard
GitHub: ihw33/ai-orchestra-dashboard
역할: [담당 업무]
도구: GitHub CLI (gh) 설치됨

필독: TEAM_MEMBER_GUIDE.md 파일을 확인하세요
위치: /Users/m4_macbook/Projects/ai-orchestra-dashboard/TEAM_MEMBER_GUIDE.md"

# 2. 가이드 확인 지시
"cat /Users/m4_macbook/Projects/ai-orchestra-dashboard/TEAM_MEMBER_GUIDE.md 명령으로 팀원 가이드를 숙지하세요"
```

### 2️⃣ 팀원별 세션 관리

#### iTerm Tab 4 구성
- **Session 1**: Claude (AI 모드)
- **Session 2**: Gemini (Shell/AI 모드 전환 필요)
- **Session 3**: zsh (일반 쉘)
- **Session 4**: Codex (AI 모드)

#### 독립 앱
- **Cursor**: VS Code 기반 AI 에디터 (Cmd+K로 AI Chat 접근)

#### 세션 확인 명령어
```bash
# 세션 목록 확인
osascript -e 'tell app "iTerm" to tell tab 4 to get name of sessions'

# 특정 세션 상태 확인
osascript -e 'tell app "iTerm" to tell tab 4 to tell session X to get is at shell prompt'
```

### 3️⃣ AppleScript 표준 패턴

```applescript
tell application "iTerm"
    activate
    tell window 1
        tell tab 4
            select
            tell session [번호]
                select
                write text "메시지"
            end tell
        end tell
    end tell
end tell

delay 0.5

tell application "System Events"
    tell process "iTerm2"
        keystroke return
    end tell
end tell
```

### 4️⃣ Gemini 특별 관리

Gemini CLI는 두 가지 모드가 있음:
- **Shell 모드 (`$`)**: bash 명령어로 해석
- **AI 모드 (`>`)**: AI 대화로 해석

#### 모드 전환
```applescript
# Shell → AI 모드 전환
write text "!"
keystroke return

# AI → Shell 모드 전환 (다시 !)
write text "!"
keystroke return
```

### 5️⃣ Issue 작업 할당 프로세스

#### 1. Issue 생성
```bash
gh issue create -R ihw33/ai-orchestra-dashboard \
  --title "[작업명]" \
  --body "## 작업 내용
[상세 설명]

## 보고 절차
1. 확인 즉시: gh issue comment X --body '[팀원명] 확인 완료, 진행 가능'
2. 진행 중 (30분마다): gh issue comment X --body '[팀원명] 진행률: X%'
3. 완료 후: gh issue comment X --body '[팀원명] 작업 완료: [결과]'

담당: [팀원명]"
```

#### 2. 팀원에게 알림
```applescript
write text "Issue #X이 할당되었습니다. 확인하세요: gh issue view X -R ihw33/ai-orchestra-dashboard"
```

### 6️⃣ 모니터링 체크리스트

#### 5분마다 확인
- [ ] Issue 댓글 확인: `gh issue view X --comments | tail -10`
- [ ] 파일 변경 확인: `find . -name "*.py" -o -name "*.ts" -mmin -5`
- [ ] 팀원 응답 확인

#### 30분마다 확인
- [ ] 진행 보고 여부
- [ ] 블로커 발생 여부
- [ ] 작업 진척도

### 7️⃣ Cursor 통신 가이드

#### Cursor AI Chat 접근
```applescript
tell application "Cursor"
    activate
end tell

delay 1

tell application "System Events"
    tell process "Cursor"
        -- Cmd+K to open AI chat
        keystroke "k" using command down
        delay 1
        
        -- Type message
        keystroke "메시지 내용"
        delay 0.5
        
        -- Send message
        keystroke return
    end tell
end tell
```

#### 주의사항
- 손쉬운 사용(Accessibility)에 Cursor 추가 필요
- Cmd+K가 AI Chat 단축키
- Cursor는 독립 앱으로 iTerm과 별개

### 8️⃣ 문제 해결 가이드

| 문제 | 원인 | 해결 |
|------|------|------|
| 메시지 전달 안 됨 | 세션 번호 틀림 | 세션 목록 재확인 |
| 엔터키 안 먹음 | 포커스 문제 | `tell process "iTerm2"` 추가 |
| Gemini bash 에러 | Shell 모드 | `!`로 AI 모드 전환 |
| Cursor 메시지 안 감 | 단축키 틀림 | Cmd+K 사용 |
| 팀원 무응답 | 지시 불명확 | 구체적 명령어 제공 |

### 9️⃣ 팀원 관리 규칙

- **30분 무보고**: 경고 메시지
- **1시간 무보고**: 작업 재할당
- **2시간 무보고**: CLI 재시작

### 🔟 일일 운영 플로우

1. **오전 시작**
   - 각 팀원 상태 확인
   - 당일 작업 Issue 생성
   - 팀원별 작업 할당

2. **작업 중**
   - 5분마다 모니터링
   - 30분마다 진행 보고 확인
   - 블로커 즉시 대응

3. **일일 마감**
   - 완료 작업 정리
   - 미완료 작업 이월
   - 다음날 계획 수립

---

**최종 업데이트**: 2025-08-19
**작성자**: PM Claude