# 🎼 AI Orchestra Q&A 정리 (풀버전)

## 1. 모델 관련

**Q. Qwen3 coder는 직접 엔진을 설치해야 하나요?**
A. 네, 로컬에서 사용하려면 엔진 설치 필요. Hugging Face 배포판을 받아 실행 가능.

**Q. 내 맥북(M4 Max)에서 실행 가능할까요?**
A. Qwen3-7B 정도는 충분히 실행 가능. Qwen3-72B나 ChatOSS-120B는 GPU 서버 필요.

**Q. 20B와 120B 모델 차이는?**
A. 매개변수 크기와 추론 성능 차이. 20B는 경량·개인 연구에 적합, 120B는 범용 고성능 추론용.

**Q. 120B 모델은 학습 전 성능이 어느 정도인가요?**
A. GPT-4 이전 세대 수준. 파인튜닝으로 도메인 성능 강화 가능.

---

## 2. 환경/설치

**Q. Claude Code 같은 AI CLI를 쓰려면 무엇이 필요한가요?**
A. Node.js 설치 필수. (`brew install node`) → npm 기반 설치 가능.

**Q. brew install node가 안 될 때?**
A. Xcode Command Line Tools가 먼저 설치되어야 함. `xcode-select --install` 실행 후 재시도.

**Q. 설치 후 환경은?**
A. Node.js + npm 환경에서 AI CLI (예: Claude Code, Codex CLI) 설치 → GitHub Connector 연동.

---

## 3. PM & 팀원 협업 구조

**Q. 개발 PM의 역할은 무엇인가요?**
A. 
- 마일스톤을 라운드 단위로 쪼개기
- 이슈 배분 및 라벨링
- 팀원 상태 확인 (작업 중/Allow 요청/대기)
- 완료 보고 취합 및 회고 작성
- 모든 지시를 GitHub Issue/PR로 통제

**Q. 팀원 AI는 어떻게 일하나요?**
A.
- 이슈 확인 즉시 작업 실행
- 중간 제안 없이 지시된 작업만 수행
- 완료 후 이슈에 보고 댓글 작성

**Q. PM과 나는 어떻게 다른가요?**
A.
- PM은 중간 컨펌을 내게 받아야만 다음 단계 진행
- 팀원은 컨펌 없이 즉시 실행
- 나는 PM의 상위 관리자(Owner)로, 전략과 승인권 보유

**Q. 라운드와 회고는 어떻게 하나요?**
A.
- 라운드 = 하나의 묶음 작업
- 라운드 종료 시 모든 이슈 완료 보고를 취합 → PM이 MD 문서로 정리 → 나에게 제출 → 회고 진행

---

## 4. GitHub & 자동화

**Q. GitHub에서 API로 할 수 있는 것은?**
A. Issue/PR 생성, 라벨링, 프로젝트 칸반/로드맵 관리, 상태 확인. JSON 포맷으로 응답.

**Q. API를 정기적으로 호출하려면?**
A. cron job, GitHub Actions, Probot(Webhook 기반) 사용.

**Q. Probot은 무엇인가요?**
A. GitHub App 프레임워크. 자동 라벨링, 알림, 보고 정리 같은 PL(Progress Leader) Bot 역할 가능.

---

## 5. iTerm2 & tmux

**Q. iTerm2 세션 네임/Title/ID의 차이는?**
A.
- ID: 내부 고유 식별자 (자동 생성)
- Title: 탭 상단에 표시되는 이름
- Session Name: 스크립트/자동화 접근용 논리 이름

**Q. iTerm2에서 입력창 전체 지우기?**
A. Cmd + U (커서 앞 삭제), Ctrl + C 후 clear, 단축키 매핑 가능.

**Q. tmux 세션을 챗봇이 직접 조작할 수 있나요?**
A. 직접 불가. 외부 스크립트가 tmux를 관리해야 함. 챗봇은 tmux pane 내부 프로세스로만 동작.

---

## 6. SaaS & 솔루션화

**Q. GitHub + iTerm2 기반 협업을 SaaS로 만들 수 있나요?**
A. 가능. 웹 대시보드에서 챗봇 개수·종류 설정 → 백엔드에서 GitHub API + iTerm2 제어 → 상태 모니터링.

**Q. 챗봇이 Allow 요청(bash command 실행 허가) 시 알림 가능?**
A. 가능. GitHub Issue 이벤트 + Slack/메일/Webhook으로 알림 발송.

**Q. 챗봇이 멈추거나 thinking이 길어질 때?**
A. 상태 모니터링 Bot(PL Bot) 추가 → 타임아웃 감지, 강제 중단, 진행 상태 요약 보고 가능.

---

## 7. 라이선스/오픈소스

**Q. iTerm2는 오픈소스인가요?**
A. 네, GPLv2 라이선스. 수정 후 사내에서 사용 가능. 외부 배포 시 오픈소스 공개 의무 있음.

**Q. GitHub는 오픈소스인가요?**
A. 아니요, 플랫폼 자체는 상용. 다만 REST API, Probot 프레임워크 등은 공개되어 자유롭게 활용 가능.

---

## 8. 확장/상품화 전략

**Q. 현재 솔루션을 어떻게 상품화할 수 있나요?**
A.
- 1차: AI 협업 PM 솔루션 (GitHub 중심)
- 2차: 개발팀과 타부서 협업 의사결정 솔루션 (투명한 공유)
- 확장: Notion, Asana, Monday, n8n, Google Workspace와 연동 → 범용 그룹웨어 솔루션

**Q. 추가 기능은?**
A.
- 현황 파악 및 보고만 담당하는 PL Bot 도입
- 프로젝트 전체 대시보드 (진행률, 병목, 라운드별 완료율 시각화)
- 자동 보고서 생성 → GitHub Pages 또는 SaaS 대시보드에서 확인

---

## 핵심 정리

- **PM AI** = 이슈 관리 + 중간 컨펌 + 보고
- **팀원 AI** = 즉시 실행 + 결과 보고
- **Owner(나)** = PM의 상위 승인자
- **GitHub Issue/PR/Project** = 협업의 중심
- **iTerm2/tmux** = 세션 제어 & 자동화 엔진
- **SaaS 확장 시** PL Bot과 알림 체계로 안정성 확보
- **상품화 전략** = AI 협업 도구 → 개발팀 전용 → 타부서 확장 → SaaS 그룹웨어

---

## 우리 프로젝트에 적용할 개선점

### 1. PL Bot (Progress Leader Bot) 도입
- 현재 문제: PM이 모든 팀원 상태를 수동으로 확인
- 해결책: PL Bot이 자동으로 상태 모니터링 및 보고
- 구현: GitHub Actions + Probot 프레임워크

### 2. Allow 요청 알림 시스템
- 현재 문제: bash command 실행 허가 요청 시 놓치기 쉬움
- 해결책: Webhook 기반 즉시 알림 (Slack/Discord/메일)
- 구현: GitHub Issue 이벤트 + 알림 서비스 연동

### 3. 타임아웃 감지 시스템
- 현재 문제: AI가 thinking 중이거나 멈췄을 때 감지 어려움
- 해결책: 정기적 헬스체크 + 타임아웃 감지
- 구현: iTerm2 세션 모니터링 + 상태 대시보드

### 4. 자동 회고 시스템
- 현재 문제: 라운드 종료 시 수동으로 보고서 작성
- 해결책: 이슈/PR 데이터 자동 수집 → MD 보고서 생성
- 구현: GitHub Actions workflow

---

**작성일**: 2025-08-20
**작성자**: PM Claude
**출처**: 외부 챗봇 대화 정리 + AI Orchestra 프로젝트 적용 방안