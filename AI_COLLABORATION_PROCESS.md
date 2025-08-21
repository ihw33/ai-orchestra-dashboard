# 🎭 AI Orchestra - GitHub 중심 협업 프로세스

## 📋 전체 협업 구조

```
GitHub (중앙 허브)
    ↓
PM Claude (오케스트라 지휘자)
    ↓
┌─────────┬──────────┬──────────┬──────────┐
│ Gemini  │  Codex   │ Claude2  │ ChatGPT  │
│(기획/UX)│(백엔드)  │(프론트)  │(리뷰/QA) │
└─────────┴──────────┴──────────┴──────────┘
```

## 🔄 협업 워크플로우

### 1️⃣ 작업 시작 (GitHub Issue 기반)
```bash
# PM Claude가 실행
1. GitHub Issues 확인
2. 우선순위 판단
3. 작업 할당 결정
```

### 2️⃣ 작업 할당 프로세스
```
PM → Gemini: "Issue #21 분석하고 기획서 작성해줘"
PM → Codex: "Issue #22 백엔드 API 구현해줘"
PM → Claude2: "Issue #23 UI 컴포넌트 만들어줘"
```

### 3️⃣ 실제 통신 방법
- **AppleScript**: iTerm2 세션 간 직접 메시지 전송
- **GitHub Comments**: 작업 결과 공유
- **File System**: 코드/문서 공유
- **Chrome Tabs**: 실시간 모니터링

## 🛠 구체적인 실행 시나리오

### 시나리오 1: 새 기능 개발
```
1. PM이 GitHub에서 새 Issue 발견
   → "사용자 프로필 기능 추가 #24"

2. PM이 작업 분배:
   → Gemini: "사용자 스토리와 UI 설계 작성"
   → Codex: "User 모델과 API 엔드포인트 구현"
   → Claude2: "프로필 페이지 컴포넌트 개발"

3. 각 AI가 작업 진행:
   → 브랜치 생성
   → 코드 작성
   → 커밋 & 푸시

4. PM이 진행상황 모니터링:
   → GitHub PR 상태 확인
   → Chrome 탭으로 각 AI 작업 확인
   → 필요시 추가 지시

5. ChatGPT가 코드 리뷰:
   → PR 리뷰 코멘트
   → 개선사항 제안

6. PM이 최종 머지 결정
```

### 시나리오 2: 버그 수정
```
1. GitHub에 버그 리포트 Issue 생성됨
2. PM이 Codex에게 즉시 할당
3. Codex가 디버깅 후 수정
4. ChatGPT가 빠른 리뷰
5. PM이 핫픽스 배포 승인
```

## 💻 기술적 구현

### A. PM Master Control 명령어
```bash
# 상태 확인
./pm_control status

# 작업 할당
./pm_control assign gemini "Issue #24 기획해줘"
./pm_control assign codex "API 구현 시작"

# 모니터링
./pm_control monitor

# GitHub 동기화
./pm_control sync-github
```

### B. 자동화 스크립트 구조
```applescript
-- 1. GitHub Issue 체크
tell Chrome tab (GitHub)
    execute javascript "check new issues"
    
-- 2. AI에게 작업 할당
tell iTerm session (Gemini)
    write text "새 작업: Issue #24"
    
-- 3. 진행상황 추적
tell all sessions
    check status
```

### C. 통신 채널
1. **명령 전달**: AppleScript → iTerm2 write text
2. **상태 확인**: iTerm2 session status
3. **결과 수집**: GitHub API / File system
4. **시각화**: Chrome 대시보드

## 📊 모니터링 대시보드

```
┌─────────────────────────────────────┐
│      AI Orchestra Dashboard         │
├─────────────────────────────────────┤
│ GitHub Issues                       │
│ ✅ #21 - Assigned to Gemini        │
│ 🔄 #22 - In Progress (Codex)       │
│ 📝 #23 - Ready for Review          │
├─────────────────────────────────────┤
│ Team Status                         │
│ Gemini  - 🟢 Available              │
│ Codex   - 🟡 Working on #22        │
│ Claude2 - 🟢 Available              │
│ ChatGPT - 🔵 Reviewing PR #45      │
└─────────────────────────────────────┘
```

## 🚀 다음 단계

1. **Phase 1**: 기본 통신 구현 ✅
   - AppleScript로 메시지 전송
   - Chrome 탭 제어

2. **Phase 2**: GitHub 통합 (현재)
   - Issue 자동 할당
   - PR 상태 추적
   - 코멘트 자동화

3. **Phase 3**: 지능형 자동화
   - AI가 스스로 다음 작업 판단
   - 자동 에러 처리
   - 성능 최적화

## 🎯 핵심 이점

1. **중앙 집중식 관리**: PM Claude가 모든 것을 조율
2. **투명한 협업**: GitHub에 모든 작업 기록
3. **실시간 모니터링**: Chrome 대시보드로 한눈에
4. **자동화**: 반복 작업 최소화
5. **확장 가능**: 새 AI 추가 용이

## 🔧 필요한 도구

- iTerm2 (분할 세션)
- Chrome (GitHub, AI 웹 인터페이스)
- AppleScript (자동화)
- GitHub CLI (gh 명령어)
- 각 AI CLI (claude, gemini, codex 등)