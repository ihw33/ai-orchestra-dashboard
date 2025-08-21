# 🔔 Allow 요청 자동 처리 시스템

## 1. 핵심 문제
- PM Claude가 Allow 요청을 받아서 판단해야 함
- 정상 진행 vs 위험한 명령 구분 필요
- 응답 옵션: 1(Yes), 2(No), 3(상세 확인)

## 2. Allow 요청 분류

### ✅ 자동 승인 가능 (Auto-Yes)
```yaml
safe_commands:
  - npm install
  - npm run dev/build/test
  - git status/diff/log
  - ls/cd/pwd
  - cat/grep (프로젝트 내)
  - gh issue/pr list
  - python -m pytest
```

### ⚠️ 검토 필요 (Review)
```yaml
review_commands:
  - git push (브랜치 확인)
  - npm publish
  - docker run
  - curl/wget (외부 URL)
  - pip install (보안 체크)
```

### 🚫 자동 거부 (Auto-No)
```yaml
dangerous_commands:
  - rm -rf (특히 /)
  - sudo (시스템 변경)
  - 환경변수 변경 (PATH 등)
  - 민감 파일 접근 (/etc, ~/.ssh)
  - 외부 스크립트 실행
```

## 3. PM Claude 프롬프트 메시지 형식

### 3.1 표준 Allow 알림 형식
```
[ALLOW_REQUEST]
FROM: {cli_name}
TAB: {tab_number}
COMMAND: {command}
CONTEXT: {last_task}
RISK_LEVEL: {LOW|MEDIUM|HIGH}
SUGGESTED_ACTION: {1|2|3}
TIMESTAMP: {time}
[/ALLOW_REQUEST]
```

### 3.2 예시
```
[ALLOW_REQUEST]
FROM: Gemini
TAB: 4-3
COMMAND: npm install axios
CONTEXT: Issue #27 - API 클라이언트 구현
RISK_LEVEL: LOW
SUGGESTED_ACTION: 1
TIMESTAMP: 2025-08-20 15:30:45
[/ALLOW_REQUEST]
```

## 4. PM Claude 응답 로직

### 4.1 자동 판단 알고리즘
```python
def process_allow_request(request):
    # 1. 위험도 평가
    if request.risk_level == "LOW" and is_safe_command(request.command):
        return auto_approve()  # 1 입력
    
    # 2. 컨텍스트 확인
    if request.risk_level == "MEDIUM":
        if matches_current_issue(request.context):
            return approve_with_log()  # 1 입력
        else:
            return request_details()  # 3 입력
    
    # 3. 위험 명령 차단
    if request.risk_level == "HIGH":
        return auto_reject()  # 2 입력
```

### 4.2 응답 템플릿
```markdown
## Allow 요청 처리

**판단**: [승인/거부/확인필요]
**이유**: {판단 근거}
**액션**: 
- 승인(1): 작업 진행
- 거부(2): 대안 제시
- 확인(3): Thomas 컨펌 요청
```

## 5. 구현 아키텍처

### 5.1 시스템 흐름
```mermaid
AI CLI → Allow 요청 발생
    ↓
AppleScript 감지
    ↓
Python 브릿지 (분류/위험도 평가)
    ↓
PM Claude 프롬프트에 [ALLOW_REQUEST] 삽입
    ↓
PM Claude 자동 판단
    ↓
응답 (1/2/3) 자동 입력
    ↓
AI CLI 작업 계속/중단
```

### 5.2 Python 브릿지 코드
```python
import re
import subprocess
from typing import Dict, Tuple

class AllowRequestHandler:
    def __init__(self):
        self.safe_patterns = [
            r'^npm (install|run|test)',
            r'^git (status|diff|log|branch)',
            r'^ls|pwd|cd',
            r'^cat|grep|find',
            r'^gh (issue|pr)',
        ]
        
        self.dangerous_patterns = [
            r'^rm -rf',
            r'^sudo',
            r'~/\.ssh',
            r'/etc/',
            r'export PATH',
        ]
    
    def evaluate_risk(self, command: str) -> Tuple[str, int]:
        """명령어 위험도 평가"""
        # 안전한 명령
        for pattern in self.safe_patterns:
            if re.match(pattern, command):
                return "LOW", 1  # 자동 승인 제안
        
        # 위험한 명령
        for pattern in self.dangerous_patterns:
            if re.search(pattern, command):
                return "HIGH", 2  # 자동 거부 제안
        
        # 그 외 검토 필요
        return "MEDIUM", 3
    
    def send_to_pm_claude(self, request: Dict):
        """PM Claude 프롬프트에 메시지 삽입"""
        message = f"""
[ALLOW_REQUEST]
FROM: {request['cli_name']}
TAB: {request['tab']}
COMMAND: {request['command']}
CONTEXT: {request['context']}
RISK_LEVEL: {request['risk_level']}
SUGGESTED_ACTION: {request['suggested_action']}
TIMESTAMP: {request['timestamp']}
[/ALLOW_REQUEST]
"""
        # AppleScript로 PM Claude에게 전송
        subprocess.run(['osascript', '-e', f'''
            tell application "iTerm2"
                tell current session of current window
                    write text "{message}"
                end tell
            end tell
        '''])
```

## 6. 특수 케이스 처리

### 6.1 git push/merge
- 브랜치 확인 필수
- master/main 직접 push → 거부
- PR 통한 merge → 승인

### 6.2 파일 삭제
- 프로젝트 내 임시 파일 → 승인
- 소스 코드 삭제 → Thomas 확인

### 6.3 외부 API 호출
- 신뢰할 수 있는 도메인 → 승인
- 알 수 없는 도메인 → 확인

## 7. 모니터링 & 로깅

### 7.1 Allow 요청 로그
```json
{
  "timestamp": "2025-08-20T15:30:45",
  "cli": "Gemini",
  "command": "npm install axios",
  "risk_level": "LOW",
  "pm_action": "APPROVED",
  "response_time": "2.3s"
}
```

### 7.2 대시보드 표시
- 일일 Allow 요청 수
- 승인/거부 비율
- 평균 응답 시간
- 위험 명령 차단 횟수

## 8. 설정 파일

### allow_config.yaml
```yaml
auto_approve:
  enabled: true
  patterns:
    - "npm install"
    - "git status"
    - "pytest"
  
auto_reject:
  enabled: true
  patterns:
    - "rm -rf /"
    - "sudo"
    
notification:
  high_risk_alert: true
  webhook_url: "discord://..."
  
pm_claude:
  auto_response: true
  confirmation_required:
    - "production deployment"
    - "database migration"
```

## 9. 예상 효과

| 지표 | 현재 | 개선 후 |
|------|------|---------|
| Allow 응답 시간 | 5-10분 | 10초 |
| 놓친 요청 | 30% | 0% |
| 잘못된 승인 | 가끔 | 거의 없음 |
| PM 개입 필요 | 100% | 20% |

---

**작성일**: 2025-08-20
**작성자**: PM Claude
**구현 난이도**: ⭐⭐⭐
**예상 소요 시간**: 4시간