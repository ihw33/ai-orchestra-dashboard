# 🧑‍💼 PM Guide - AI Orchestra

## 1. 기본 운영 원칙
- PM-CLI는 **팀원-CLI의 유일한 실행 트리거**  
- 팀원은 GitHub 이슈/PR만 확인하며, 반드시 **PM 프롬프트 지시를 받아야 실행**  
- 모든 중간 결정은 반드시 **상혁님 CLI에서 컨펌**  
- 팀원은 **추가 제안/독자적 판단 불가** → 지시만 수행  
- 라운드는 스프린트 단위: **이슈 묶음 → 실행 → 보고서/회고**

---

## 2. 실행 알고리즘
1. 상혁님이 PM에게 지시 전달  
2. PM이 이슈 생성 및 파싱  
3. 상혁님 컨펌 후, 팀원 프롬프트에 지시 입력  
4. 팀원은 실행 후 이슈 코멘트(`[REPORT]`, `[DONE]`) 작성  
5. PM이 확인 → 상혁님 보고  
6. 라운드 종료 → `round-report.md` 생성 및 CLI 보고

👉 상세 순서도: [AI_Orchestra_Flow.md](./AI_Orchestra_Flow.md)

---

## 3. GitHub 활용 규칙
- **이슈 (Issue)** = 작업 정의  
- **PR (Pull Request)** = 산출물  
- PR에는 반드시 `Fixes #이슈번호` 포함  
- 코멘트 시그널:
  - `[ACK]` → 작업 확인
  - `[START]` → 시작
  - `[REPORT]` → 중간 보고
  - `[DONE]` (#PR 번호 포함) → 완료 보고

---

## 4. Project 뷰 (3종)
- **Kanban**: To Do / In Progress / Done
- **Roadmap**: 라운드 및 마일스톤 일정
- **Round List**: 테이블로 라운드별 이슈/담당/PR/상태

---

## 5. 자동화 패키지
GitHub Actions 최소 3개:
1. `validate-pr-link.yml`  
   - PR에 `Fixes #이슈번호` 없으면 fail  
2. `done-comment-guard.yml`  
   - `[DONE]` 코멘트에 PR 번호 없으면 fail  
3. `round-report.yml`  
   - 라운드 종료 시 자동 보고서 생성 (`docs/rounds/round-XXX-report.md`)

---

## 6. 보고 체계
- 팀원 → GitHub 이슈 코멘트  
- PM → 상혁님 CLI 보고  
- 라운드 종료 시 → `docs/rounds/`에 보고서 자동 저장

---

## 7. 이슈 생성 원칙
- **작업 순서대로** 이슈 번호 부여 (의존성 고려)
- 팀원 배정은 이슈 생성 후 결정
- 각 이슈는 독립적으로 실행 가능해야 함