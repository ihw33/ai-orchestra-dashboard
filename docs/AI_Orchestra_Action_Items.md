# 🎯 AI Orchestra 실행 가능한 개선 방안

## 1. iTerm2 활용 강화

### 1.1 세션 관리 자동화
- **문제**: 수동으로 탭/세션 찾아가며 작업
- **해결**: AppleScript로 세션 자동 탐색 및 명령 전송
```applescript
-- 세션명으로 자동 찾기
tell application "iTerm2"
  tell current window
    repeat with aTab in tabs
      tell aTab
        repeat with aSession in sessions
          if name of aSession contains "gemini" then
            tell aSession to write text "작업 명령"
          end if
        end repeat
      end tell
    end repeat
  end tell
end tell
```

### 1.2 세션 상태 모니터링
- **구현**: Python 스크립트로 정기적 체크
- **활용**: AI 멈춤/thinking 감지

## 2. GitHub Bot (Probot) 도입

### 2.1 PL Bot (Progress Leader Bot)
- **역할**: 팀원 상태 자동 모니터링
- **기능**:
  - Issue 진행률 자동 업데이트
  - PR 자동 라벨링
  - 블로커 감지 및 알림
  - 일일 보고서 자동 생성

### 2.2 설치 및 설정
```bash
# Probot 설치
npm install -g create-probot-app
create-probot-app ai-orchestra-bot

# 주요 이벤트 핸들러
module.exports = (app) => {
  // Issue 생성시 자동 라벨
  app.on('issues.opened', async context => {
    await context.octokit.issues.addLabels({
      labels: ['pending', 'round-2']
    })
  })
  
  // PR에 'Fixes #' 없으면 경고
  app.on('pull_request.opened', async context => {
    const body = context.payload.pull_request.body
    if (!body.includes('Fixes #')) {
      await context.octokit.issues.createComment({
        body: '⚠️ PR에 `Fixes #이슈번호`를 포함해주세요'
      })
    }
  })
}
```

## 3. Allow 요청 알림 시스템

### 3.1 Webhook 기반 즉시 알림
```python
# Discord/Slack 알림 전송
import requests

def send_allow_notification(cli_name, command):
    webhook_url = "YOUR_WEBHOOK_URL"
    payload = {
        "content": f"🔔 **{cli_name}** Allow 요청\n```{command}```",
        "username": "AI Orchestra Bot"
    }
    requests.post(webhook_url, json=payload)
```

### 3.2 GitHub Issue 자동 생성
- bash 명령 실행 요청시 자동으로 Issue 생성
- Owner가 승인하면 자동 실행

## 4. 타임아웃 감지 시스템

### 4.1 AI 상태 체크
```python
# 5분마다 AI 상태 확인
import time
import subprocess

def check_ai_status(session_name):
    script = f'''
    tell application "iTerm2"
      tell current session of current window
        if name contains "{session_name}" then
          return is at shell prompt
        end if
      end tell
    end tell
    '''
    
    result = subprocess.run(['osascript', '-e', script], 
                          capture_output=True, text=True)
    
    if "false" in result.stdout:
        # AI가 thinking 중
        return "thinking"
    return "ready"

# 10분 이상 thinking이면 알림
if thinking_duration > 600:
    send_timeout_alert(session_name)
```

## 5. 자동 회고 시스템

### 5.1 GitHub Actions Workflow
```yaml
name: Round Report Generator

on:
  workflow_dispatch:
    inputs:
      round_number:
        description: 'Round number'
        required: true

jobs:
  generate-report:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Collect Round Data
        run: |
          gh issue list --label "round-${{ inputs.round_number }}" \
            --state all --json number,title,state,assignee > issues.json
          
          gh pr list --label "round-${{ inputs.round_number }}" \
            --state all --json number,title,state,mergedAt > prs.json
      
      - name: Generate Report
        run: python scripts/generate_round_report.py
      
      - name: Create Report PR
        run: |
          git add docs/rounds/round-${{ inputs.round_number }}-report.md
          git commit -m "Round ${{ inputs.round_number }} 회고 보고서"
          gh pr create --title "Round ${{ inputs.round_number }} Report"
```

## 6. 실시간 대시보드 강화

### 6.1 WebSocket 기반 실시간 업데이트
```typescript
// AI 상태 실시간 모니터링
const aiStatusSocket = new WebSocket('ws://localhost:8001/ws/ai-status')

aiStatusSocket.onmessage = (event) => {
  const status = JSON.parse(event.data)
  updateAIStatusUI(status)
}
```

### 6.2 통합 메트릭스
- 3개 프로젝트 동시 모니터링
- AI 팀원별 작업 시간 추적
- 병목 구간 자동 감지

## 7. CLI 브릿지 강화

### 7.1 명령 큐잉 시스템
```python
# 명령 대기열 관리
import queue
import threading

command_queue = queue.Queue()

def process_commands():
    while True:
        cmd = command_queue.get()
        if needs_approval(cmd):
            request_approval(cmd)
        else:
            execute_command(cmd)
        command_queue.task_done()

# 백그라운드 스레드로 실행
threading.Thread(target=process_commands, daemon=True).start()
```

## 8. 즉시 실행 가능한 작업

### Phase 1 (오늘)
1. ✅ PL Bot 기본 구조 생성
2. ✅ iTerm2 세션 모니터링 스크립트
3. ✅ Allow 요청 알림 설정

### Phase 2 (내일)
1. Probot 앱 배포
2. GitHub Actions 자동 회고
3. 타임아웃 감지 시스템

### Phase 3 (모레)
1. 실시간 대시보드 WebSocket
2. 통합 메트릭스 구현
3. CLI 브릿지 큐잉 시스템

## 9. 예상 효과

| 문제 | 현재 | 개선 후 |
|------|------|---------|
| AI 상태 파악 | 수동 확인 | 자동 모니터링 |
| Allow 요청 | 놓치기 쉬움 | 즉시 알림 |
| 회고 작성 | 30분 소요 | 자동 생성 |
| 팀원 관리 | PM 수동 | PL Bot 자동 |
| 병목 감지 | 사후 발견 | 실시간 감지 |

---

**작성일**: 2025-08-20
**작성자**: PM Claude
**상태**: 실행 대기