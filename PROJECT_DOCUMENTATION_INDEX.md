# 📚 AI Orchestra Dashboard - 프로젝트 문서 인덱스

> 최종 업데이트: 2025-08-21
> 작성자: PM Claude

## 🎯 프로젝트 개요

**AI Orchestra Dashboard**는 7개 AI가 협업하는 완전 자동화 개발 플랫폼입니다.

### 핵심 목표
- **Round 4-10** (12주): Tool → Framework → Platform → Ecosystem 진화
- **7개 AI 통합**: PM Claude, Codex, Gemini, Cursor, Claude, Task Master, FigmaMake
- **완전 자동화**: Auto-onboarding, 실시간 모니터링, 자동 작업 분배

---

## 📖 문서 구조

### 1️⃣ 핵심 문서 (Core Documents)

#### [TEAM_COLLABORATION_CHECKLIST.md](./TEAM_COLLABORATION_CHECKLIST.md)
- **용도**: 일일/주간 협업 체크리스트
- **핵심**: Daily Standup, PR 리뷰, 회고 프로세스
- **Thomas 요구사항**: "중간 리뷰", "빌드 확인", "의견 수렴" 완벽 반영
- **상태**: ✅ 활용 중

#### [ENHANCED_TASK_BREAKDOWN_R4-R10.md](./ENHANCED_TASK_BREAKDOWN_R4-R10.md)
- **용도**: Round 4-10 마스터 플랜 (12주)
- **핵심**: 각 Round별 상세 태스크, 담당 AI, 일정
- **특징**: 가장 최신 버전, 구체적 실행 계획 포함
- **상태**: ✅ 메인 계획서

#### [CLI_CONNECTION_GUIDE.md](./CLI_CONNECTION_GUIDE.md)
- **용도**: AI CLI 연결 가이드
- **핵심**: Gemini, Codex, Claude, Cursor 연결 방법
- **중요**: AppleScript 통신 코드 포함
- **상태**: ✅ 검증됨

#### [iterm_session_quick_guide.md](./iterm_session_quick_guide.md)
- **용도**: iTerm2 세션 구성 참조
- **핵심**: Tab 4 Orchestra Board 세션 매핑
- **데이터**: iterm_sessions.json 구조 설명
- **상태**: ✅ 활용 중

### 2️⃣ 설정 문서 (Setup Documents)

#### [SETUP_GUIDE.md](./SETUP_GUIDE.md)
- **용도**: 초기 환경 설정
- **내용**: Python, Node.js, iTerm2 설정
- **상태**: ⚠️ task_master_setup.md와 통합 필요

#### [task_master_setup.md](./task_master_setup.md)
- **용도**: Task Master 설정
- **내용**: GitHub 권한, 환경변수
- **상태**: ⚠️ SETUP_GUIDE.md와 통합 필요

### 3️⃣ 참조 문서 (Reference)

#### [round5_retrospective.md](./round5_retrospective.md)
- **용도**: Round 5 실패 분석
- **교훈**: 가짜 KPI 문제, 실제 통신 필요
- **상태**: ✅ 학습 완료

#### [TASK_BREAKDOWN_R4-R10.md](./TASK_BREAKDOWN_R4-R10.md)
- **용도**: 초기 계획 (구버전)
- **상태**: ❌ ENHANCED 버전으로 대체됨 (삭제 권장)

---

## 🗂️ 핵심 코드 파일

### 통신 시스템
- `iterm_session_manager.py` - iTerm2 세션 관리
- `smart_prompt_sender.py` - AI 메시지 전송
- `unified_ai_communicator.py` - 통합 통신 시스템

### 모니터링
- `pl-bot/pl-bot-v3.py` - Progress Leader Bot
- `real_kpi_tracker.py` - 실제 KPI 측정

### 자동화
- `auto-onboarding/` - 5분 온보딩 시스템
- `scripts/cli_automation_bridge.py` - CLI 자동화

---

## 🔄 통합 제안

### 1. 마스터 플랜 통합
```bash
# 기존
TASK_BREAKDOWN_R4-R10.md (구버전)
ENHANCED_TASK_BREAKDOWN_R4-R10.md (신버전)

# 통합 후
MASTER_PLAN_R4-R10.md (통합본)
```

### 2. 설정 가이드 통합
```bash
# 기존
SETUP_GUIDE.md
task_master_setup.md

# 통합 후
COMPLETE_SETUP_GUIDE.md
```

---

## 🚀 Quick Start

### 1. 프로젝트 시작
```bash
# 세션 확인
python3 iterm_session_manager.py

# PL Bot 시작
python3 pl-bot/pl-bot-v3.py

# 통신 테스트
python3 unified_ai_communicator.py
```

### 2. Round 5 재시작
```bash
# KPI 시스템 실행
python3 round5/real_kpi_tracker.py

# AI 작업 할당
python3 assign_round5_tasks.py
```

---

## ⚠️ 주의사항

1. **세션 구조 준수**: Tab 4에 4개 세션 (Claude, Terminal, Gemini, Codex)
2. **통신 확인**: AppleScript write text 사용 (엔터 자동 포함)
3. **프로세스 준수**: PR 생성 → 리뷰 → 머지
4. **회고 필수**: 매 Round 종료 시 팀 회고

---

## 📊 현재 상태 (2025-08-21)

- **Round 4**: ✅ 완료
- **Round 5**: 🔄 재시작 중 (실제 KPI 구현)
- **문서 정리**: ✅ 완료
- **통신 시스템**: ✅ 검증됨
- **PL Bot**: ✅ v3 개발 완료

---

## 💡 다음 단계

1. **즉시**: Round 5 롤백 후 재시작
2. **오늘**: 실제 작업 할당 및 KPI 측정
3. **이번 주**: Round 5 완료 및 회고
4. **다음 주**: Round 6 시작 (Framework 단계)

---

*"천천히 하더라도 확실하게 하자" - Thomas*