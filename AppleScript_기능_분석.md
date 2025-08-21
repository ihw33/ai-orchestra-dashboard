# 🎯 AppleScript 파일 기능 분석 및 통합 방안

## 📋 파일별 기능 분석

### 1. **pm_master_control.applescript** (메인 컨트롤러)
```
주요 기능:
- ✅ 명령어 기반 제어 시스템 (status, assign, monitor, web)
- ✅ 모든 iTerm 세션 상태 확인
- ✅ 특정 팀원(gemini, codex, claude2)에게 작업 할당
- ✅ 전체 시스템 모니터링 (iTerm + Chrome)
- ✅ GitHub 탭 새로고침 및 웹 제어

특징: 
- 파라미터 받아서 실행 가능
- 도움말 기능 포함
- 가장 체계적이고 완성도 높음
```

### 2. **auto_orchestra.applescript** (자동 작업 분배)
```
주요 기능:
- ✅ PM(세션1) → 팀원들(세션2,3,4) 일괄 작업 할당
- ✅ 순차적 딜레이로 안정적 실행
- ✅ 완료 알림 표시

특징:
- 하드코딩된 작업 내용
- 간단한 일괄 실행용
```

### 3. **real_workflow.applescript** (전체 개발 프로세스)
```
주요 기능:
- ✅ Claude Desktop → Cursor → iTerm CLI들 → VSCode → GitHub 통합
- ✅ 5단계 전체 워크플로우 자동화
- ✅ 실제 개발 시나리오 구현 (장바구니 예시)
- ✅ 각 단계 알림 표시

특징:
- 가장 복잡하고 실제적인 워크플로우
- 여러 애플리케이션 연동
```

### 4. **chrome_control.applescript** (웹 브라우저 관리)
```
주요 기능:
- ✅ GitHub, Claude, ChatGPT 탭 자동 열기
- ✅ JavaScript로 페이지 정보 추출
- ✅ 각 탭 상태 모니터링
- ✅ 리포트 생성 및 파일 저장

특징:
- 웹 대시보드 역할
- JavaScript 실행으로 동적 정보 수집
```

### 5. **iterm_test.applescript** (iTerm 탭 제어)
```
주요 기능:
- ✅ iTerm 탭 간 전환
- ✅ System Events로 키보드 입력
- ✅ 각 탭에 메시지 전송

특징:
- 가장 기본적인 기능
- 테스트용으로 적합
```

---

## 🔧 통합 방안

### 방안 1: **모듈화 통합** (추천 ✅)
```applescript
-- ai_orchestra_master.applescript
-- 모든 기능을 모듈로 통합한 마스터 스크립트

property modules : {¬
    terminal: "iterm_control.scpt",¬
    browser: "chrome_control.scpt",¬
    workflow: "workflow_control.scpt"¬
}

on run argv
    if (count of argv) = 0 then
        return showMainMenu()
    end if
    
    set command to item 1 of argv
    
    -- 기능별 라우팅
    if command = "pm" then
        -- pm_master_control 기능들
    else if command = "workflow" then
        -- real_workflow 기능들
    else if command = "web" then
        -- chrome_control 기능들
    else if command = "auto" then
        -- auto_orchestra 기능들
    end if
end run
```

### 방안 2: **단일 파일 통합**
```applescript
-- 모든 기능을 하나의 파일에 통합
-- 장점: 관리 편함, 한 파일에서 모든 제어
-- 단점: 파일이 너무 커짐 (500줄 이상)
```

### 방안 3: **현재 구조 유지 + 마스터 스크립트**
```applescript
-- master.applescript (새로 생성)
-- 기존 파일들을 그대로 두고 호출만 하는 방식

on run argv
    set scriptPath to "/Users/m4_macbook/Projects/ai-orchestra-dashboard/"
    
    if command = "pm" then
        do shell script "osascript " & scriptPath & "pm_master_control.applescript " & args
    else if command = "workflow" then
        do shell script "osascript " & scriptPath & "real_workflow.applescript"
    -- ...
end run
```

---

## 💡 추천 구조

### **계층적 구조로 재구성**
```
ai-orchestra-dashboard/
├── master.applescript           # 메인 진입점
├── modules/
│   ├── terminal_control.scpt   # iTerm 제어 (iterm_test 기반)
│   ├── browser_control.scpt    # Chrome 제어 (chrome_control 기반)
│   ├── pm_functions.scpt       # PM 기능들 (pm_master_control 기반)
│   └── workflow_automation.scpt # 워크플로우 (real_workflow 기반)
└── workflows/
    ├── daily_standup.scpt      # 일일 스탠드업 자동화
    ├── issue_management.scpt   # 이슈 관리 자동화
    └── deployment.scpt         # 배포 자동화
```

### **통합 실행 명령어**
```bash
# PM 기능
osascript master.applescript pm status
osascript master.applescript pm assign gemini "Issue #13 작업"

# 워크플로우
osascript master.applescript workflow daily
osascript master.applescript workflow deploy

# 웹 모니터링
osascript master.applescript web dashboard
osascript master.applescript web refresh

# 자동화
osascript master.applescript auto full
```

---

## 🎯 결론

### **즉시 실행 가능한 통합안**
1. `pm_master_control.applescript`를 베이스로 사용
2. 다른 스크립트들의 핵심 기능을 함수로 추가
3. 명령어 기반 인터페이스 유지
4. 모듈화로 유지보수 용이성 확보

### **장점**
- ✅ 하나의 진입점으로 모든 기능 제어
- ✅ 파라미터로 세밀한 제어 가능
- ✅ 기존 코드 재사용
- ✅ 확장 가능한 구조

### **구현 우선순위**
1. **1단계**: pm_master_control + chrome_control 통합
2. **2단계**: real_workflow 기능 추가
3. **3단계**: 새로운 워크플로우 추가 (daily, deploy 등)