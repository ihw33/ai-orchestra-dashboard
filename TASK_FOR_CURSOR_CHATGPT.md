# 🎨 Cursor ChatGPT-5 작업 지시서

## GitHub Issue #7: Design - 멀티 프로젝트 대시보드 UX/UI 디자인

### 즉시 작업할 디자인

#### 1. 통합 대시보드 레이아웃
```
┌─────────────────────────────────────────────────┐
│                   Header                        │
│  [Logo] AI Orchestra    [🌙] [한국어▼] [@User]  │
├─────────────────────────────────────────────────┤
│              Project Cards (3-col)              │
│  ┌──────┐      ┌──────┐      ┌──────┐         │
│  │ IWL  │      │ AI   │      │ Calli │         │
│  │  📚  │      │  🤖  │      │  🎨   │         │
│  └──────┘      └──────┘      └──────┘         │
├─────────────────────────────────────────────────┤
│           Unified Metrics Dashboard             │
│  Issues: 35 | PRs: 10 | AI Sessions: 9         │
└─────────────────────────────────────────────────┘
```

#### 2. 프로젝트 카드 디자인
- Hover effect: scale(1.05) + shadow
- Status indicator: 우측 상단 점 (🟢 active, 🟡 idle)
- 메인 색상 그라디언트 배경
- 하단에 주요 지표 3개

#### 3. 색상 시스템
```css
/* Light Mode */
--iwl-primary: #3B82F6;
--iwl-bg: #EFF6FF;

--engine-primary: #10B981;
--engine-bg: #F0FDF4;

--calli-primary: #8B5CF6;
--calli-bg: #FAF5FF;

/* Dark Mode */
--iwl-dark: #1E40AF;
--engine-dark: #047857;
--calli-dark: #6B21A8;
```

#### 4. 반응형 브레이크포인트
- Desktop: 1280px+ (3 columns)
- Tablet: 768px-1279px (2 columns)
- Mobile: <768px (1 column)

### 컴포넌트 스타일링
Tailwind CSS 클래스 사용:
- Cards: `rounded-xl shadow-lg hover:shadow-2xl transition-all`
- Metrics: `bg-gradient-to-r from-blue-500 to-purple-500`
- Animations: `animate-pulse`, `animate-bounce`

### Figma 파일 구조 (선택사항)
```
Orchestra Dashboard/
├── 📁 Components
│   ├── ProjectCard
│   ├── MetricCard
│   └── Navigation
├── 📁 Layouts
│   ├── Desktop
│   ├── Tablet
│   └── Mobile
└── 📁 Design Tokens
    ├── Colors
    ├── Typography
    └── Spacing
```

---
**디자인 작업을 시작해주세요!**