export const translations = {
  en: {
    header: {
      title: "AI Orchestra Dashboard 🎭",
      status: "Status",
      connected: "Connected",
      disconnected: "Disconnected"
    },
    tabs: {
      overview: "Overview",
      github: "GitHub",
      aiAgents: "AI Agents",
      workflows: "Workflows",
      pmControl: "PM Control"
    },
    overview: {
      stats: {
        activeIssues: "Active Issues",
        openPRs: "Open PRs",
        aiSessions: "AI Sessions",
        tasksCompleted: "Tasks Completed"
      },
      recentActivity: "Recent Activity",
      activities: {
        newIssue: "New issue created",
        prReview: "completed code review for PR",
        deployment: "Deployment pipeline triggered for main branch",
        prMerged: "PR merged"
      }
    },
    github: {
      openIssues: "Open Issues",
      pullRequests: "Pull Requests",
      status: {
        review: "review",
        ready: "ready",
        draft: "draft"
      },
      checks: "Checks"
    },
    aiAgents: {
      title: "AI Agents",
      discussion: "AI Discussion",
      status: {
        active: "active",
        idle: "idle"
      },
      current: "Current",
      tasksCompleted: "Tasks completed",
      roles: {
        pm: "Project Manager",
        backend: "Backend Developer",
        ux: "Content & UX"
      }
    },
    workflows: {
      active: "Active Workflows",
      quickActions: "Quick Actions",
      status: {
        running: "running",
        completed: "completed",
        pending: "pending"
      },
      actions: {
        createIssue: "Create Issue",
        startDiscussion: "Start AI Discussion",
        deploy: "Deploy to Production",
        generateReport: "Generate Report"
      }
    },
    common: {
      from: "from",
      yesterday: "yesterday",
      readyToMerge: "ready to merge",
      activeNow: "active now",
      thisWeek: "this week",
      minutesAgo: "minutes ago",
      hoursAgo: "hours ago",
      none: "None"
    }
  },
  ko: {
    header: {
      title: "AI 오케스트라 대시보드 🎭",
      status: "상태",
      connected: "연결됨",
      disconnected: "연결 끊김"
    },
    tabs: {
      overview: "개요",
      github: "깃허브",
      aiAgents: "AI 에이전트",
      workflows: "워크플로우",
      pmControl: "PM 제어"
    },
    overview: {
      stats: {
        activeIssues: "활성 이슈",
        openPRs: "열린 PR",
        aiSessions: "AI 세션",
        tasksCompleted: "완료된 작업"
      },
      recentActivity: "최근 활동",
      activities: {
        newIssue: "새 이슈 생성됨",
        prReview: "PR 코드 리뷰 완료",
        deployment: "메인 브랜치 배포 파이프라인 실행",
        prMerged: "PR 병합됨"
      }
    },
    github: {
      openIssues: "열린 이슈",
      pullRequests: "풀 리퀘스트",
      status: {
        review: "리뷰 중",
        ready: "준비됨",
        draft: "초안"
      },
      checks: "검사"
    },
    aiAgents: {
      title: "AI 에이전트",
      discussion: "AI 토론",
      status: {
        active: "활동 중",
        idle: "대기 중"
      },
      current: "현재 작업",
      tasksCompleted: "완료된 작업",
      roles: {
        pm: "프로젝트 매니저",
        backend: "백엔드 개발자",
        ux: "콘텐츠 & UX"
      }
    },
    workflows: {
      active: "활성 워크플로우",
      quickActions: "빠른 작업",
      status: {
        running: "실행 중",
        completed: "완료됨",
        pending: "대기 중"
      },
      actions: {
        createIssue: "이슈 생성",
        startDiscussion: "AI 토론 시작",
        deploy: "프로덕션 배포",
        generateReport: "보고서 생성"
      }
    },
    common: {
      from: "부터",
      yesterday: "어제",
      readyToMerge: "병합 준비됨",
      activeNow: "현재 활동 중",
      thisWeek: "이번 주",
      minutesAgo: "분 전",
      hoursAgo: "시간 전",
      none: "없음"
    }
  }
}

export type Language = 'en' | 'ko'
export type TranslationKey = typeof translations.en