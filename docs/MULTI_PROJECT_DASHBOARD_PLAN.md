# 🎯 AI Orchestra 멀티 프로젝트 대시보드 기획안

## 1. 프로젝트 개요

### 목적
3개의 AI 기반 개발 프로젝트를 통합 모니터링하고 관리하는 대시보드 구축

### 대상 프로젝트
| 프로젝트 | 설명 | 특징 | 팀 규모 |
|---------|------|------|---------|
| **IWL v5 Rebuild** | 8×4 매트릭스 학습 플랫폼 | Phase 기반 개발 | 5명 |
| **AI Engine Hub** | 공유 AI 인프라 | Ollama 모델 관리 | 3명 |
| **Calligraphy Coach v2** | 서예 학습 앱 | 모노레포 구조 | 4명 |

## 2. 핵심 기능

### 🏠 홈 화면 (통합 뷰)
```
┌────────────────────────────────────────────────┐
│             AI Orchestra Dashboard             │
│                                                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │ IWL v5   │  │AI Engine │  │Calligraphy│    │
│  │ 📚 12/5  │  │ 🤖 8/2   │  │ 🎨 15/3   │    │
│  │ Phase A  │  │ 20b Ready│  │ Round 1-2 │    │
│  └──────────┘  └──────────┘  └──────────┘    │
│                                                │
│  총 Issues: 35 | PRs: 10 | AI Sessions: 9     │
│  이번 주 완료: 42 | 진행중: 18 | 블로커: 2    │
└────────────────────────────────────────────────┘
```

### 📊 프로젝트별 상세 대시보드

#### IWL v5 전용 기능
- **8×4 매트릭스 진행률**: 32개 모듈 시각화
- **Stage 트래커**: 현재 Stage 4/8
- **Wiki 문서 상태**: 작성 완료/검토 중/대기
- **Issue 우선순위**: P0-P3 분류

#### AI Engine Hub 전용 기능  
- **모델 상태**: gpt-oss:20b (13GB), llama3.2 (2GB)
- **리소스 모니터**: RAM 사용량, GPU 상태
- **API 헬스체크**: 응답시간, 에러율
- **벤치마크**: 모델별 성능 비교

#### Calligraphy Coach 전용 기능
- **Round 진행**: 1-2 진행중 (70%)
- **Storybook**: 컴포넌트 12개 배포
- **CI/CD 상태**: 빌드/테스트/배포
- **모노레포 패키지**: apps/, services/, packages/

### 🤖 AI 팀원 모니터링
```javascript
// 실시간 AI 활동 상태
{
  "PM Claude": {
    status: "active",
    currentTask: "Issue #31 리뷰",
    projects: ["IWL v5", "Calligraphy"],
    lastActivity: "2분 전"
  },
  "Cursor (ChatGPT-5)": {
    status: "working",
    currentTask: "Stage 4 작성",
    projects: ["IWL v5", "Calligraphy"],
    lastActivity: "방금"
  },
  "Gemini": {
    status: "idle",
    currentTask: null,
    projects: ["모든 프로젝트"],
    lastActivity: "15분 전"
  }
}
```

## 3. 화면 구성

### 3.1 네비게이션 구조
```
메인 탭:
├── 🏠 Overview (통합)
├── 📚 IWL v5
├── 🤖 AI Engine  
├── 🎨 Calligraphy
├── 👥 AI Team
├── 📈 Analytics
└── ⚙️ Settings
```

### 3.2 프로젝트 전환 방식
- **탭 방식**: 상단 탭으로 빠른 전환
- **드롭다운**: 헤더에 프로젝트 선택기
- **사이드바**: 왼쪽 고정 프로젝트 리스트

## 4. 데이터 연동

### GitHub API 통합
```typescript
// 3개 레포지토리 동시 모니터링
const repos = [
  'ihw33/iwl-v5-rebuild',
  'ihw33/ai-engine-hub',
  'ihw33/calligraphy-coach-v2'
]

// 통합 데이터 수집
async function fetchAllProjectData() {
  return Promise.all(repos.map(repo => fetchGitHubData(repo)))
}
```

### iTerm 세션 연동
```applescript
-- 3개 탭 모니터링
Tab 1: IWL v5 (PM + Gemini + Codex)
Tab 2: AI Engine (Gemini + Codex + Claude)  
Tab 3: Calligraphy (PM + Gemini + Codex + Claude)
```

### 실시간 업데이트
- WebSocket으로 변경사항 즉시 반영
- 5초마다 GitHub 데이터 폴링
- iTerm 세션 10초마다 체크

## 5. UI/UX 디자인

### 색상 테마
| 프로젝트 | 메인 색상 | 보조 색상 |
|---------|----------|----------|
| IWL v5 | Blue (#3B82F6) | Sky (#0EA5E9) |
| AI Engine | Green (#10B981) | Emerald (#34D399) |
| Calligraphy | Purple (#8B5CF6) | Violet (#A78BFA) |

### 반응형 레이아웃
- **Desktop**: 3열 그리드, 전체 정보
- **Tablet**: 2열 그리드, 주요 정보
- **Mobile**: 1열, 프로젝트 선택 후 상세

### 다크모드
- 기존 다크모드 지원 유지
- 프로젝트 색상도 다크모드 대응

## 6. 주요 컴포넌트

### 통합 컴포넌트
```typescript
<ProjectOverview />      // 3개 프로젝트 요약 카드
<UnifiedMetrics />       // 통합 지표
<TeamActivityFeed />     // 모든 팀원 활동
<CrossProjectTimeline /> // 통합 타임라인
```

### 프로젝트별 컴포넌트
```typescript
// IWL v5
<MatrixGrid />          // 8×4 매트릭스
<StageProgress />       // Stage 진행률
<WikiDocStatus />       // Wiki 문서 상태

// AI Engine
<ModelManager />        // 모델 관리
<ResourceMonitor />     // 리소스 모니터
<APIHealthCheck />      // API 상태

// Calligraphy  
<RoundTracker />        // Round 진행
<StorybookViewer />     // Storybook 연동
<MonorepoStatus />      // 패키지 상태
```

## 7. 구현 우선순위

### Phase 1: 기본 구조 (오늘)
1. ✅ 프로젝트 설정 파일 생성
2. ✅ 라우팅 구조 설정
3. ✅ 프로젝트 선택기 구현

### Phase 2: 데이터 연동 (내일)
1. GitHub API 멀티 레포 연동
2. 통합 메트릭스 계산
3. 실시간 업데이트 구현

### Phase 3: UI 구현 (2일차)
1. 프로젝트별 대시보드
2. 통합 대시보드
3. AI 팀원 뷰

### Phase 4: 고급 기능 (3일차)
1. iTerm 세션 모니터링
2. 알림 시스템
3. 분석/리포트

## 8. 기술 스택

### Frontend
- Next.js 15.4 (기존)
- React 19 (기존)
- Tailwind CSS (기존)
- Recharts (차트)
- Lucide Icons (아이콘)

### Backend
- FastAPI (기존)
- WebSocket (기존)
- Redis (캐싱)
- GitHub API v4

### 모니터링
- AppleScript (iTerm 제어)
- Python (브릿지 스크립트)

## 9. 예상 화면

### 메인 대시보드
```
┌─────────────────────────────────────────────────┐
│ AI Orchestra  [🌙] [한국어▼] [@Thomas]          │
├─────────────────────────────────────────────────┤
│ Overview | IWL v5 | AI Engine | Calligraphy | AI Team │
├─────────────────────────────────────────────────┤
│                                                 │
│  📊 Today's Summary                            │
│  ┌─────────┬─────────┬─────────┐              │
│  │ Commits │ Issues  │ PRs     │              │
│  │   42    │   35    │   10    │              │
│  └─────────┴─────────┴─────────┘              │
│                                                 │
│  🔥 Active Now                                 │
│  • PM Claude: Reviewing Issue #31              │
│  • Cursor: Writing Stage 4-2                   │
│  • Codex: Implementing API endpoints           │
│                                                 │
│  📈 Weekly Progress                            │
│  [████████████░░░░░░] 65% Complete            │
│                                                 │
└─────────────────────────────────────────────────┘
```

## 10. 성공 지표

### 정량적 지표
- 3개 프로젝트 동시 모니터링
- 5초 이내 데이터 업데이트
- 모든 GitHub 이벤트 캐치

### 정성적 지표
- 한눈에 전체 상황 파악
- 프로젝트 간 전환 용이
- AI 팀원 활동 추적 가능

## 11. 리스크 및 대응

| 리스크 | 대응 방안 |
|--------|----------|
| GitHub API 제한 | 캐싱, 배치 요청 |
| 실시간 동기화 지연 | WebSocket 재연결 로직 |
| 3개 프로젝트 복잡도 | 필터링, 우선순위 표시 |

## 12. 다음 단계

1. **즉시**: 프로젝트 설정 파일 생성
2. **30분 내**: 기본 라우팅 구현
3. **1시간 내**: 프로젝트 선택기 완성
4. **오늘 중**: Phase 1 완료

---

**작성일**: 2025-08-19
**작성자**: PM Claude
**승인 필요**: Thomas