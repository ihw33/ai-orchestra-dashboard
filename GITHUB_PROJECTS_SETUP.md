# 🎯 GitHub Projects 설정 가이드

## 📊 추천 Project 구성

### 1️⃣ **Main Orchestra Board** (칸반 보드)
**목적**: 현재 진행 중인 작업의 실시간 추적
**뷰 타입**: Board (칸반)

#### 컬럼 구성:
- **📥 Backlog**: 다음 라운드 대기 중
- **🎯 Ready**: 이번 라운드 작업 준비 완료
- **👀 Assigned**: 팀원 할당됨
- **🚀 In Progress**: 작업 진행 중
- **🔍 In Review**: 리뷰/테스트 중
- **✅ Done**: 완료

#### 필터 & 그룹:
- **Group by**: Assignee (팀원별)
- **Filter**: Current Round (현재 라운드만)
- **Sort**: Priority (P0 → P1 → P2)

---

### 2️⃣ **Round Roadmap** (로드맵 보드)
**목적**: 전체 프로젝트 진행 상황 조망
**뷰 타입**: Roadmap (타임라인)

#### 설정:
- **Date field**: Round (커스텀 필드)
- **Group by**: Round Number
- **Timeline**: Round 1 → Round 7
- **Markers**: 
  - 🏁 Round Start
  - 🎯 Mid-point Check
  - ✅ Round Complete

#### 커스텀 필드:
```yaml
Round: 
  - Round 0 (Complete)
  - Round 1 (Current)
  - Round 2
  - Round 3
  - Round 4
  - Round 5
  - Round 6
  - Round 7
```

---

### 3️⃣ **Team Workload** (테이블 뷰)
**목적**: 팀원별 작업 부하 관리
**뷰 타입**: Table

#### 컬럼:
- Issue Number
- Title
- Assignee
- Round
- Status
- Priority
- Estimated Hours
- Actual Hours
- Completion %

#### 필터 옵션:
- By Assignee (Codex, Gemini, Claude, Cursor)
- By Status
- By Round
- By Priority

---

### 4️⃣ **Release Dashboard** (대시보드 뷰)
**목적**: 릴리즈별 진행 상황 추적
**뷰 타입**: Dashboard (차트 & 메트릭)

#### 위젯 구성:
1. **Progress Chart** (도넛 차트)
   - To Do / In Progress / Done

2. **Burndown Chart** (라인 차트)
   - Issues 남은 수 vs 시간

3. **Team Velocity** (바 차트)
   - 팀원별 완료 Issue 수

4. **Round Progress** (프로그레스 바)
   - 각 라운드별 완료율

5. **Blockers** (리스트)
   - 블로킹 이슈 목록

6. **Recent Activity** (타임라인)
   - 최근 24시간 활동

---

## 🏷️ 라벨 시스템

### Round 라벨 (자동 적용)
- `round-1` ~ `round-7`

### 팀원 라벨
- `codex`
- `gemini`
- `claude`
- `cursor`

### 우선순위 라벨
- `P0-critical` 🔴
- `P1-important` 🟡
- `P2-nice-to-have` 🟢

### 상태 라벨
- `blocked` 🚫
- `needs-review` 👀
- `bug` 🐛
- `enhancement` ✨
- `documentation` 📚

### 작업 타입
- `backend`
- `frontend`
- `data`
- `design`
- `devops`
- `testing`

---

## 🎯 Milestones 설정

### Major Milestones
1. **M1: Foundation Complete** (Round 1)
   - Due: Round 1 완료 시
   - Issues: 27개

2. **M2: Real-time Ready** (Round 2)
   - Due: Round 2 완료 시
   - Issues: 20개

3. **M3: Intelligence Enabled** (Round 3)
   - Due: Round 3 완료 시
   - Issues: 20개

4. **M4: Collaboration Live** (Round 4)
   - Due: Round 4 완료 시
   - Issues: 19개

5. **M5: Scaled Platform** (Round 5)
   - Due: Round 5 완료 시
   - Issues: 21개

6. **M6: Production Ready** (Round 6)
   - Due: Round 6 완료 시
   - Issues: 19개

7. **M7: Public Launch** (Round 7)
   - Due: Round 7 완료 시
   - Issues: 24개

---

## 🔄 자동화 설정

### GitHub Actions 자동화
```yaml
# .github/workflows/project-automation.yml
name: Project Automation

on:
  issues:
    types: [opened, assigned, closed]
  issue_comment:
    types: [created]

jobs:
  auto-move:
    runs-on: ubuntu-latest
    steps:
      - name: Move to In Progress
        if: contains(github.event.comment.body, '작업 시작')
        uses: actions/github-script@v6
        with:
          script: |
            # Issue를 In Progress로 이동

      - name: Move to Review
        if: contains(github.event.comment.body, '리뷰 요청')
        uses: actions/github-script@v6
        with:
          script: |
            # Issue를 In Review로 이동
```

### 자동 할당 규칙
- `backend` 라벨 → Codex 자동 할당
- `data` 라벨 → Gemini 자동 할당
- `frontend` 라벨 → Claude 자동 할당
- `design` 라벨 → Cursor 자동 할당

---

## 📈 추천 View 조합

### 🎬 PM용 (Thomas & PM Claude)
1. **Main Orchestra Board** - 실시간 작업 상황
2. **Round Roadmap** - 전체 진행 상황
3. **Release Dashboard** - 메트릭 & 분석

### 👨‍💻 개발팀용 (AI 팀원들)
1. **Main Orchestra Board** (필터: 자신의 작업만)
2. **Team Workload** (테이블 뷰)
3. **My Tasks** (커스텀 뷰: 자신에게 할당된 것만)

### 📊 이해관계자용
1. **Release Dashboard** - 진행 상황 한눈에
2. **Round Roadmap** - 타임라인 확인
3. **Milestone Progress** - 주요 목표 달성도

---

## 🚀 구현 단계

### Step 1: Project 생성
```bash
# GitHub CLI로 프로젝트 생성
gh project create "AI Orchestra Dashboard" \
  --owner ihw33 \
  --title "AI Orchestra Dashboard" \
  --body "AI 팀원 협업 관리 시스템"
```

### Step 2: 커스텀 필드 추가
- Round (Single Select)
- Priority (Single Select)
- Estimated Hours (Number)
- Team Member (Single Select)
- Completion % (Number)

### Step 3: View 생성
1. Board View 생성
2. Roadmap View 생성
3. Table View 생성
4. Dashboard 위젯 설정

### Step 4: 자동화 규칙 설정
- Issue 생성 시 자동 Backlog 추가
- 할당 시 Assigned 컬럼 이동
- 댓글 기반 상태 변경

---

## 💡 Best Practices

### 1. 일일 운영
- 매일 아침 Board View 확인
- Blocked 이슈 우선 해결
- 진행률 업데이트

### 2. 라운드 전환
- 이전 라운드 회고
- 다음 라운드 Issue 준비
- Milestone 업데이트

### 3. 보고
- 주간 Dashboard 스크린샷
- Roadmap 진행 상황 공유
- Velocity 트렌드 분석

---

**작성일**: 2025-08-19
**작성자**: PM Claude
**추천**: Main Orchestra Board (칸반) + Round Roadmap (로드맵) + Release Dashboard (대시보드) 조합