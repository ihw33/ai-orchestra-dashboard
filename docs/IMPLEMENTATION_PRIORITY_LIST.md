# 🎯 AI Orchestra 구현 우선순위 리스트

## 🚨 즉시 구현 (오늘-내일)

### 1. Allow 요청 즉시 알림 시스템
- **문제**: bash 명령 실행 허가 요청을 놓쳐서 AI가 대기
- **해결**: Discord/Slack Webhook으로 즉시 알림
- **구현 시간**: 2시간
```python
# 간단한 webhook 알림
def send_allow_alert(cli_name, command):
    webhook.post(f"🔔 {cli_name} Allow 요청: {command}")
```

### 2. AI 상태 자동 모니터링
- **문제**: AI가 thinking 중인지 멈췄는지 모름
- **해결**: iTerm2 세션 상태 5분마다 체크
- **구현 시간**: 3시간
```applescript
-- iTerm2 세션 상태 확인
tell application "iTerm2"
  if session is at shell prompt then "ready"
  else "thinking"
end tell
```

### 3. GitHub Issue 자동 시그널 체크
- **문제**: 팀원들이 [ACK], [START], [DONE] 시그널 누락
- **해결**: GitHub Actions로 자동 체크 및 리마인더
- **구현 시간**: 2시간

---

## 📅 단기 구현 (이번 주)

### 4. PL Bot (Progress Leader Bot)
- **역할**: 팀원 상태 자동 추적 및 보고
- **기능**:
  - Issue 진행률 자동 업데이트
  - 블로커 감지 시 알림
  - 일일 진행 상황 요약
- **구현**: Probot 프레임워크 사용
- **예상 시간**: 1일

### 5. 멀티모델 라우터
- **목적**: 작업별로 최적 AI 모델 자동 선택
- **라우팅 규칙**:
  - 추론/전략 → PM Claude
  - 데이터/분석 → Gemini
  - 코딩 → Codex
  - 간단 작업 → 20B 모델
- **구현 시간**: 4시간

### 6. 자동 회고 시스템
- **문제**: 라운드 종료 시 수동 보고서 작성 30분 소요
- **해결**: GitHub Actions로 자동 생성
- **구현 시간**: 3시간
```yaml
name: Auto Round Report
on:
  workflow_dispatch:
jobs:
  generate:
    - collect issues/PRs
    - generate markdown report
    - create PR
```

---

## 🔄 중기 구현 (2주 내)

### 7. 턴 기반 Issue 워크플로우
- **개념**: 스무고개처럼 정해진 단계별 진행
- **구현**:
  ```json
  {
    "turns": [
      {"turn": 1, "task": "요구사항 정의", "assignee": "Gemini"},
      {"turn": 2, "task": "설계", "assignee": "Claude"},
      {"turn": 3, "task": "구현", "assignee": "Codex"},
      {"turn": 4, "task": "테스트", "assignee": "Claude"},
      {"turn": 5, "task": "배포", "assignee": "Gemini"}
    ]
  }
  ```

### 8. iTerm2 세션 오케스트레이터
- **기능**: 모든 AI 세션 중앙 관리
- **자동화**:
  - 세션별 작업 할당
  - 상태 모니터링
  - 명령 큐잉
- **구현**: Python + AppleScript

### 9. 실시간 대시보드 WebSocket
- **현재**: 5초마다 폴링
- **개선**: WebSocket으로 실시간 업데이트
- **표시 정보**:
  - AI별 현재 작업
  - 진행률
  - 블로커 알림

---

## 🚀 장기 구현 (1개월 내)

### 10. 20B 모델 로컬 파인튜닝
- **목적**: 프로젝트 전용 지식 학습
- **데이터**: 
  - GitHub 이슈/PR 히스토리
  - 프로젝트 문서
  - 코드베이스
- **방식**: LoRA/QLoRA

### 11. 가드레일 시스템
- **기능**: 범위 이탈 자동 감지
- **동작**:
  - 커리큘럼/프로젝트 범위 체크
  - 이탈 시 자동 리다이렉션
  - 2회 연속 이탈 시 알림

### 12. 명령 승인 큐 시스템
- **문제**: Allow 요청 관리 어려움
- **해결**: 
  - 모든 명령 큐에 저장
  - 웹 UI에서 일괄 승인/거부
  - 승인 패턴 학습

---

## 📊 구현 우선순위 매트릭스

| 항목 | 긴급도 | 중요도 | 난이도 | 효과 | 우선순위 |
|------|--------|--------|--------|------|----------|
| Allow 알림 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ | ⭐⭐⭐⭐⭐ | **1** |
| AI 상태 모니터링 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | **2** |
| Issue 시그널 체크 | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐ | ⭐⭐⭐ | **3** |
| PL Bot | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | **4** |
| 멀티모델 라우터 | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | **5** |

---

## ✅ 실행 체크리스트

### 오늘 (Day 1)
- [ ] Allow 알림 Webhook 설정
- [ ] iTerm2 상태 체크 스크립트 작성
- [ ] GitHub Actions 시그널 체커 배포

### 내일 (Day 2)
- [ ] PL Bot 기본 구조 생성
- [ ] 멀티모델 라우터 프로토타입

### 이번 주말
- [ ] 자동 회고 시스템 구현
- [ ] 턴 기반 워크플로우 설계

### 다음 주
- [ ] iTerm2 오케스트레이터 구현
- [ ] WebSocket 실시간 업데이트
- [ ] 가드레일 시스템 프로토타입

---

## 💡 Quick Wins (바로 효과 볼 수 있는 것들)

1. **Allow 알림** → 응답 시간 10분 → 30초
2. **AI 상태 표시** → 멈춤 감지 30분 → 5분
3. **자동 시그널** → 수동 확인 불필요
4. **PL Bot** → PM 부담 50% 감소
5. **멀티모델** → 비용 30% 절감

---

**작성일**: 2025-08-20
**작성자**: PM Claude
**승인 필요**: Thomas
**예상 ROI**: 팀 생산성 2배 향상