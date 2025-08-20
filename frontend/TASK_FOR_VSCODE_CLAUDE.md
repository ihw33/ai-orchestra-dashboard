# 🎯 VSCode Claude 작업 지시서

## GitHub Issue #6: Frontend - 프로젝트 선택기 및 통합 대시보드 UI

### 즉시 구현할 컴포넌트

#### 1. ProjectSelector.tsx
```tsx
// 3개 프로젝트를 선택할 수 있는 컴포넌트
// 위치: frontend/src/components/ProjectSelector.tsx
```

#### 2. ProjectCard.tsx
```tsx
// 각 프로젝트 정보를 보여주는 카드
// 위치: frontend/src/components/ProjectCard.tsx
// Props: project (iwl-v5 | ai-engine | calligraphy)
```

#### 3. UnifiedMetrics.tsx
```tsx
// 3개 프로젝트 통합 메트릭스
// 위치: frontend/src/components/UnifiedMetrics.tsx
// 표시할 데이터: Total Issues, Active PRs, AI Sessions
```

### 프로젝트 설정
이미 생성된 설정 파일 사용:
`frontend/src/config/projects.ts`

### 색상 가이드
- IWL v5: Blue (#3B82F6) 📚
- AI Engine: Green (#10B981) 🤖  
- Calligraphy: Purple (#8B5CF6) 🎨

### 작업 순서
1. ProjectCard 컴포넌트 생성
2. ProjectSelector로 3개 카드 배치
3. UnifiedMetrics로 통합 지표 표시
4. app/page.tsx에 통합

---
**시작해주세요!**