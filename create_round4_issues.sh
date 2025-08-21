#!/bin/bash

# 🎯 Round 4 상세 작업 이슈 생성 스크립트
# Task Master가 작성한 상세 작업 분할을 GitHub Issue로 자동 생성

set -e

REPO="ihw33/ai-orchestra-dashboard"
ROUND="Round 4"
MILESTONE="Round 4: Auto-Onboarding System"

echo "🚀 $ROUND 상세 작업 이슈 생성 시작..."
echo "Repository: $REPO"
echo ""

# Round 4 Epic Issue 생성
echo "📋 Epic Issue 생성 중..."
gh issue create -R $REPO \
  --title "[$ROUND] Auto-Onboarding System Epic" \
  --label "epic,round-4,p0" \
  --body "$(cat <<'EOF'
# 🎯 Round 4: Auto-Onboarding System Epic

## 목표
5분 안에 프로젝트 시작 가능한 자동 온보딩 시스템 구축

## 주요 산출물
- `setup-wizard.py` - 프로젝트 마법사
- `team-builder.py` - AI 팀 구성기  
- `auto-config.sh` - 자동 설정 스크립트

## 성공 메트릭
- Setup time: 30min → **5min**
- Manual steps: 20 → **1**
- Success rate: > **95%**

## Sprint 기간
- **Week 1** (5일)
- **팀**: 전체 6명 (PM Claude, Codex, Gemini, Cursor, Claude, Task Master)

## 하위 작업 목록
- [ ] #[생성될 번호]: 아키텍처 설계
- [ ] #[생성될 번호]: UI/UX 와이어프레임
- [ ] #[생성될 번호]: 핵심 로직 구현
- [ ] #[생성될 번호]: 통합 테스트
- [ ] #[생성될 번호]: 문서화

## Sprint Planning
- **일정**: 매주 월요일 09:00-10:00
- **중간 체크포인트**: 수요일 12:00 빌드 검증
- **Sprint Review**: 금요일 14:00-16:00
- **Retrospective**: 금요일 16:00-17:00

---
📝 *Task Master가 생성한 상세 작업 분할에 따라 자동 생성됨*
EOF
)"

echo "✅ Epic Issue 생성 완료"
echo ""

# Day 1 작업들 생성
echo "📅 Day 1 (월요일) 작업 이슈 생성 중..."

# Task 4.1: 아키텍처 설계
gh issue create -R $REPO \
  --title "[$ROUND-4.1] Auto-onboarding 아키텍처 설계" \
  --label "round-4,codex,p0,architecture" \
  --assignee "ihw33" \
  --body "$(cat <<'EOF'
# Task 4.1: Auto-onboarding 아키텍처 설계

## 📋 작업 개요
- **담당**: Codex
- **예상시간**: 4h
- **선행작업**: 없음
- **마감**: Day 1 (월요일) 16:00

## 🎯 작업 내용
### 1. 시스템 구조도 작성
- 컴포넌트 다이어그램
- 데이터 플로우 정의
- 모듈 간 의존성 분석

### 2. API 엔드포인트 설계
- RESTful API 스펙 정의
- 요청/응답 스키마 설계
- 에러 핸들링 전략

### 3. 데이터베이스 스키마
- 프로젝트 메타데이터 구조
- AI 팀 구성 정보 스키마
- 설정 템플릿 저장 구조

## 📊 산출물
- [ ] 시스템 아키텍처 다이어그램 (Mermaid)
- [ ] API 스펙 문서 (OpenAPI)
- [ ] 데이터베이스 ERD
- [ ] 기술 스택 선정 및 근거

## ✅ Definition of Done
- [ ] 아키텍처 문서 PR 생성
- [ ] 팀 리뷰 완료 (16:00 체크포인트)
- [ ] Thomas 승인 (Level 2)

## 🔄 일일 체크포인트
- **16:00**: 설계 리뷰 (전체 팀)
- **17:00**: 의견 수렴 및 조정

---
**시작 시 댓글**: `[Codex] 🚀 Task 4.1 작업 시작`  
**완료 시 댓글**: `[Codex] ✅ Task 4.1 완료: [산출물 링크]`
EOF
)"

# Task 4.2: UI/UX 와이어프레임
gh issue create -R $REPO \
  --title "[$ROUND-4.2] UI/UX 와이어프레임 설계" \
  --label "round-4,cursor,p0,design" \
  --assignee "ihw33" \
  --body "$(cat <<'EOF'
# Task 4.2: UI/UX 와이어프레임 설계

## 📋 작업 개요
- **담당**: Cursor
- **예상시간**: 3h
- **선행작업**: 없음
- **마감**: Day 1 (월요일) 16:00

## 🎯 작업 내용
### 1. 사용자 여정 맵핑
- 5분 온보딩 플로우 설계
- 사용자 페르소나 정의
- 터치포인트 분석

### 2. 와이어프레임 설계
- Setup Wizard 화면 구성
- Team Builder 인터페이스
- 진행률 표시 컴포넌트

### 3. 인터랙션 프로토타입
- 사용자 입력 플로우
- 에러 상태 처리
- 성공/실패 피드백

## 📊 산출물
- [ ] 사용자 여정 맵 (User Journey Map)
- [ ] 와이어프레임 (Figma/Sketch)
- [ ] 인터랙션 프로토타입
- [ ] 컴포넌트 라이브러리 초안

## ✅ Definition of Done
- [ ] 디자인 파일 공유 (Figma 링크)
- [ ] 팀 피드백 반영
- [ ] 기술 구현 가능성 검증

## 🎨 디자인 원칙
- **속도**: 5분 이내 완료 가능
- **직관성**: 설명 없이 사용 가능
- **신뢰성**: 에러 상황 명확 안내
- **접근성**: 키보드만으로 조작 가능

---
**시작 시 댓글**: `[Cursor] 🚀 Task 4.2 작업 시작`  
**완료 시 댓글**: `[Cursor] ✅ Task 4.2 완료: [Figma 링크]`
EOF
)"

# Task 4.3: 프로젝트 템플릿 분석
gh issue create -R $REPO \
  --title "[$ROUND-4.3] 프로젝트 템플릿 분석" \
  --label "round-4,gemini,p0,analysis" \
  --assignee "ihw33" \
  --body "$(cat <<'EOF'
# Task 4.3: 프로젝트 템플릿 분석

## 📋 작업 개요
- **담당**: Gemini
- **예상시간**: 3h
- **선행작업**: 없음
- **마감**: Day 1 (월요일) 16:00

## 🎯 작업 내용
### 1. 기존 프로젝트 패턴 분석
- 성공한 AI 프로젝트 템플릿 수집
- 공통 설정 패턴 식별
- 의존성 관리 전략 분석

### 2. 템플릿 카테고리 정의
- 프로젝트 타입별 분류
- AI 팀 구성 패턴 매트릭스
- 기술 스택별 템플릿

### 3. 설정 자동화 요구사항 도출
- 환경 변수 관리
- 패키지 의존성 자동 설치
- 개발 도구 설정 자동화

## 📊 산출물
- [ ] 프로젝트 패턴 분석 보고서
- [ ] 템플릿 카테고리 정의서
- [ ] AI 팀 매칭 알고리즘 설계안
- [ ] 자동화 요구사항 명세서

## 📈 분석 데이터
- **수집 대상**: GitHub top 100 AI projects
- **분석 항목**: 폴더 구조, 설정 파일, 의존성
- **카테고리**: Web, API, ML, Data, Full-stack

## ✅ Definition of Done
- [ ] 분석 데이터 시각화 완료
- [ ] 템플릿 우선순위 설정
- [ ] 팀 매칭 로직 검증

---
**시작 시 댓글**: `[Gemini] 🚀 Task 4.3 작업 시작`  
**완료 시 댓글**: `[Gemini] ✅ Task 4.3 완료: [분석 보고서 링크]`
EOF
)"

echo "✅ Day 1 작업 이슈 생성 완료"
echo ""

# Day 2 작업들 생성
echo "📅 Day 2 (화요일) 작업 이슈 생성 중..."

# Task 4.4: setup-wizard.py 핵심 로직
gh issue create -R $REPO \
  --title "[$ROUND-4.4] setup-wizard.py 핵심 로직 구현" \
  --label "round-4,codex,p0,backend" \
  --assignee "ihw33" \
  --body "$(cat <<'EOF'
# Task 4.4: setup-wizard.py 핵심 로직 구현

## 📋 작업 개요
- **담당**: Codex
- **예상시간**: 6h
- **선행작업**: Task 4.1 (아키텍처 설계)
- **마감**: Day 2 (화요일) 17:00

## 🎯 작업 내용
### 1. 대화형 프롬프트 시스템
```python
# 사용자 인터페이스 예시
def interactive_setup():
    project_type = prompt_select("프로젝트 타입", options)
    team_size = prompt_number("팀 크기", min=1, max=10)
    tech_stack = prompt_multiselect("기술 스택", stack_options)
```

### 2. 프로젝트 타입 감지
- 기존 코드 분석 로직
- package.json, requirements.txt 파싱
- 자동 카테고리 분류

### 3. 의존성 관리 로직
- 패키지 매니저별 처리
- 버전 충돌 감지
- 자동 해결 제안

## 📊 산출물
- [ ] `setup_wizard.py` 모듈
- [ ] 설정 템플릿 엔진
- [ ] 의존성 관리 유틸리티
- [ ] 단위 테스트 코드

## 🔧 기술 스택
- **언어**: Python 3.9+
- **라이브러리**: Click, Inquirer, Jinja2
- **테스트**: pytest, mock

## ✅ Definition of Done
- [ ] 핵심 로직 구현 완료
- [ ] 단위 테스트 80% 이상 커버리지
- [ ] 코드 리뷰 통과 (Claude)
- [ ] 기본 시나리오 동작 검증

## 🧪 테스트 시나리오
1. **새 프로젝트 생성**: Next.js + TypeScript
2. **기존 프로젝트 감지**: Python FastAPI
3. **에러 복구**: 잘못된 설정 자동 수정

---
**시작 시 댓글**: `[Codex] 🚀 Task 4.4 작업 시작`  
**중간 보고** (12:00): `[Codex] 📊 진행률: X%`  
**완료 시 댓글**: `[Codex] ✅ Task 4.4 완료: [PR 링크]`
EOF
)"

# Task 4.5: team-builder.py AI 팀 매칭
gh issue create -R $REPO \
  --title "[$ROUND-4.5] team-builder.py AI 팀 매칭 알고리즘" \
  --label "round-4,gemini,p0,algorithm" \
  --assignee "ihw33" \
  --body "$(cat <<'EOF'
# Task 4.5: team-builder.py AI 팀 매칭 알고리즘

## 📋 작업 개요
- **담당**: Gemini
- **예상시간**: 5h
- **선행작업**: Task 4.3 (프로젝트 템플릿 분석)
- **마감**: Day 2 (화요일) 17:00

## 🎯 작업 내용
### 1. AI 역할별 전문성 매트릭스
```python
AI_SKILLS_MATRIX = {
    "codex": {"backend": 0.9, "api": 0.95, "database": 0.8},
    "cursor": {"frontend": 0.95, "ui": 0.9, "react": 0.9},
    "gemini": {"data": 0.9, "analysis": 0.95, "ml": 0.8},
    "claude": {"review": 0.95, "docs": 0.9, "qa": 0.9}
}
```

### 2. 프로젝트 요구사항 분석
- 기술 스택 매핑
- 복잡도 평가 알고리즘
- 역할별 워크로드 계산

### 3. 자동 팀 구성 로직
- 매칭 스코어 계산
- 팀 밸런스 최적화
- 대안 팀 구성 제안

## 📊 산출물
- [ ] `team_builder.py` 모듈
- [ ] AI 스킬 매트릭스 DB
- [ ] 매칭 알고리즘 엔진
- [ ] 팀 구성 검증 로직

## 🧮 알고리즘 설계
### 매칭 스코어 공식
```
score = Σ(skill_match × weight × availability)
team_balance = min(role_coverage) × diversity_bonus
final_score = score × team_balance
```

## ✅ Definition of Done
- [ ] 매칭 알고리즘 구현 완료
- [ ] 다양한 프로젝트 타입 검증
- [ ] 성능 테스트 (< 1초 응답)
- [ ] 팀 구성 품질 검증

## 🎯 검증 시나리오
1. **웹 프로젝트**: Frontend + Backend + Database
2. **AI 프로젝트**: ML + Data + API
3. **풀스택**: All-around + Specialist mix

---
**시작 시 댓글**: `[Gemini] 🚀 Task 4.5 작업 시작`  
**중간 보고** (12:00): `[Gemini] 📊 진행률: X%`  
**완료 시 댓글**: `[Gemini] ✅ Task 4.5 완료: [알고리즘 데모 링크]`
EOF
)"

echo "✅ Day 2 작업 이슈 생성 완료"
echo ""

# Day 3-5 요약 이슈들
echo "📅 Day 3-5 작업 이슈 생성 중..."

# 통합 테스트 이슈
gh issue create -R $REPO \
  --title "[$ROUND-4.9] 통합 테스트 케이스 작성" \
  --label "round-4,claude,p1,testing" \
  --assignee "ihw33" \
  --body "$(cat <<'EOF'
# Task 4.9: 통합 테스트 케이스 작성

## 📋 작업 개요
- **담당**: Claude
- **예상시간**: 4h
- **선행작업**: Task 4.6 (프론트엔드 컴포넌트)
- **일정**: Day 3 (수요일)

## 🎯 E2E 테스트 시나리오
1. **완전 자동 온보딩**: 5분 시나리오
2. **에러 복구**: 잘못된 입력 처리
3. **성능 벤치마크**: 응답시간 측정

## 📊 산출물
- [ ] E2E 테스트 스위트
- [ ] 성능 벤치마크
- [ ] 에러 핸들링 검증

---
**완료 시 댓글**: `[Claude] ✅ 통합 테스트 완료`
EOF
)"

# 최종 문서화 이슈
gh issue create -R $REPO \
  --title "[$ROUND-4.13] 최종 배포 및 문서화" \
  --label "round-4,task-master,p0,documentation" \
  --assignee "ihw33" \
  --body "$(cat <<'EOF'
# Task 4.13: 최종 배포 및 문서화

## 📋 작업 개요
- **담당**: PM Claude + Task Master
- **예상시간**: 4h
- **일정**: Day 5 (금요일) 09:00-13:00

## 🎯 작업 내용
### 1. 프로덕션 배포
- 최종 빌드 & 패키징
- 환경 설정 검증
- 배포 스크립트 실행

### 2. Release Notes 작성
- 주요 기능 설명
- 사용법 가이드
- 알려진 이슈 및 제한사항

### 3. 다음 Round 준비
- Round 5 준비사항 점검
- 팀 피드백 정리
- 개선점 식별

## 📊 산출물
- [ ] Production Build
- [ ] Release Notes v1.0
- [ ] 사용자 가이드
- [ ] Round 5 준비 체크리스트

---
**완료 시 댓글**: `[Task Master] ✅ Round 4 배포 완료`
EOF
)"

echo "✅ 모든 Round 4 이슈 생성 완료"
echo ""

# 스프린트 관리 이슈 생성
echo "📅 Sprint 관리 이슈 생성 중..."

gh issue create -R $REPO \
  --title "[$ROUND] Sprint Management & Review" \
  --label "round-4,pm-claude,p0,process" \
  --assignee "ihw33" \
  --body "$(cat <<'EOF'
# Round 4: Sprint Management & Review

## 📅 Sprint Schedule
### Sprint Planning
- **일정**: 매주 월요일 09:00-10:00
- **참석**: 전체 팀 (6명)
- **진행**: PM Claude

### 중간 체크포인트
- **수요일 12:00**: 빌드 검증 #2
- **수요일 15:00**: 크로스 컴포넌트 검증
- **수요일 17:00**: 팀 의견 수렴 세션

### Sprint Review & Retrospective
- **금요일 14:00-16:00**: Sprint Review
- **금요일 16:00-17:00**: Retrospective

## 🎯 성공 메트릭 추적
- [ ] Setup time: 30min → 5min
- [ ] Manual steps: 20 → 1
- [ ] Success rate: > 95%
- [ ] 팀 만족도: > 4.5/5

## 📋 Daily Standup 체크리스트
### 매일 09:00 (15분)
- 어제 완료한 것
- 오늘 계획
- 블로커 및 도움 요청

## 🔄 회고 항목 (금요일)
1. **What went well?**
2. **What could be improved?**
3. **Action items for Round 5**

---
**PM Claude 책임 하에 진행**
EOF
)"

echo ""
echo "🎉 Round 4 GitHub Issue 생성 완료!"
echo ""
echo "📊 생성된 이슈 목록:"
echo "- Epic Issue: Auto-Onboarding System"
echo "- Task 4.1: 아키텍처 설계 (Codex)"
echo "- Task 4.2: UI/UX 와이어프레임 (Cursor)"
echo "- Task 4.3: 프로젝트 템플릿 분석 (Gemini)"
echo "- Task 4.4: setup-wizard.py 구현 (Codex)"
echo "- Task 4.5: team-builder.py 구현 (Gemini)"
echo "- Task 4.9: 통합 테스트 (Claude)"
echo "- Task 4.13: 최종 배포 (Task Master)"
echo "- Sprint Management (PM Claude)"
echo ""
echo "✅ 다음 단계:"
echo "1. PM Claude가 팀원들에게 작업 할당"
echo "2. 월요일 Sprint Planning 진행"
echo "3. Daily Standup 시작"
echo ""
echo "🎯 Thomas 검토 대기 중..."