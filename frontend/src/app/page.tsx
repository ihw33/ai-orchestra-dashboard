'use client'

import { useState, useEffect } from 'react'
import { GitBranch, Users, Activity, CheckCircle2, Clock, AlertCircle, BarChart3, MessageSquare, Globe } from 'lucide-react'
import { useLanguage } from '@/contexts/LanguageContext'
import PMControl from '@/components/PMControl'
import ProjectSelector from '@/components/ProjectSelector'
import ProjectCard from '@/components/ProjectCard'
import UnifiedMetrics from '@/components/UnifiedMetrics'
import { PROJECT_LIST } from '@/config/projects'

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState('projects')
  const [selectedProject, setSelectedProject] = useState<string>('')
  const { language, setLanguage, t } = useLanguage()
  const [githubData, setGithubData] = useState({
    issues: [],
    pullRequests: [],
    milestones: []
  })
  const [aiStatus, setAiStatus] = useState({
    activeSessions: 0,
    completedTasks: 0,
    pendingTasks: 0
  })

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <header className="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
                {t.header.title}
              </h1>
            </div>
            <div className="flex items-center space-x-4">
              <ProjectSelector 
                selectedProject={selectedProject}
                onProjectSelect={setSelectedProject}
              />
              {/* Language Toggle Button */}
              <button
                onClick={() => setLanguage(language === 'ko' ? 'en' : 'ko')}
                className="flex items-center gap-2 px-3 py-1.5 text-sm bg-gray-100 dark:bg-gray-700 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
              >
                <Globe className="h-4 w-4" />
                {language === 'ko' ? 'EN' : '한국어'}
              </button>
              <span className="text-sm text-gray-500 dark:text-gray-400">
                {t.header.status}: <span className="text-green-500">● {t.header.connected}</span>
              </span>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation Tabs */}
      <div className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <nav className="flex space-x-8" aria-label="Tabs">
            {Object.entries({
              projects: 'Projects',
              overview: t.tabs.overview,
              github: t.tabs.github,
              'ai-agents': t.tabs.aiAgents,
              workflows: t.tabs.workflows,
              'pm-control': t.tabs.pmControl
            }).map(([key, label]) => (
              <button
                key={key}
                onClick={() => setActiveTab(key)}
                className={`
                  py-4 px-1 border-b-2 font-medium text-sm
                  ${activeTab === key
                    ? 'border-blue-500 text-blue-600 dark:text-blue-400'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-300'
                  }
                `}
              >
                {label}
              </button>
            ))}
          </nav>
        </div>
      </div>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Projects Tab */}
        {activeTab === 'projects' && (
          <div className="space-y-6">
            <div>
              <h2 className="text-xl font-semibold mb-4">All Projects</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {PROJECT_LIST.map((project) => (
                  <ProjectCard 
                    key={project.id} 
                    project={project}
                    metrics={{
                      issues: { open: 12, closed: 45 },
                      pulls: { open: 3, merged: 18 },
                      commits: 87,
                      lastActivity: '2 mins ago',
                      status: project.id === 'iwl-v5' ? 'active' : project.id === 'ai-engine' ? 'idle' : undefined
                    }}
                  />
                ))}
              </div>
            </div>
            <UnifiedMetrics />
          </div>
        )}

        {/* Overview Tab */}
        {activeTab === 'overview' && (
          <div className="space-y-6">
            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <StatCard
                title={t.overview.stats.activeIssues}
                value="12"
                icon={<AlertCircle className="h-5 w-5" />}
                trend={`+2 ${t.common.from} ${t.common.yesterday}`}
                color="yellow"
              />
              <StatCard
                title={t.overview.stats.openPRs}
                value="5"
                icon={<GitBranch className="h-5 w-5" />}
                trend={`3 ${t.common.readyToMerge}`}
                color="blue"
              />
              <StatCard
                title={t.overview.stats.aiSessions}
                value="3"
                icon={<Users className="h-5 w-5" />}
                trend={`2 ${t.common.activeNow}`}
                color="green"
              />
              <StatCard
                title={t.overview.stats.tasksCompleted}
                value="28"
                icon={<CheckCircle2 className="h-5 w-5" />}
                trend={`+15 ${t.common.thisWeek}`}
                color="purple"
              />
            </div>

            {/* Recent Activity */}
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
              <h2 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">{t.overview.recentActivity}</h2>
              <div className="space-y-3">
                <ActivityItem
                  type="github"
                  message={`${t.overview.activities.newIssue}: #42 'Implement user authentication'`}
                  time={`5 ${t.common.minutesAgo}`}
                  t={t}
                />
                <ActivityItem
                  type="ai"
                  message={`Claude ${t.overview.activities.prReview} #38`}
                  time={`15 ${t.common.minutesAgo}`}
                  t={t}
                />
                <ActivityItem
                  type="workflow"
                  message={t.overview.activities.deployment}
                  time={`1 ${language === 'ko' ? '시간 전' : 'hour ago'}`}
                  t={t}
                />
                <ActivityItem
                  type="github"
                  message={`${t.overview.activities.prMerged}: #37 'Add dashboard components'`}
                  time={`2 ${t.common.hoursAgo}`}
                  t={t}
                />
              </div>
            </div>
          </div>
        )}

        {/* GitHub Tab */}
        {activeTab === 'github' && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Issues List */}
              <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
                <h2 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">{t.github.openIssues}</h2>
                <div className="space-y-3">
                  <IssueItem
                    number={42}
                    title="Implement user authentication"
                    labels={['enhancement', 'priority-high']}
                    assignee="AI-Claude"
                  />
                  <IssueItem
                    number={41}
                    title="Fix responsive design on mobile"
                    labels={['bug']}
                    assignee="AI-Codex"
                  />
                  <IssueItem
                    number={40}
                    title="Add documentation for API endpoints"
                    labels={['documentation']}
                    assignee="AI-Gemini"
                  />
                </div>
              </div>

              {/* Pull Requests */}
              <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
                <h2 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">{t.github.pullRequests}</h2>
                <div className="space-y-3">
                  <PRItem
                    number={38}
                    title="Add user profile component"
                    status="review"
                    checks="passing"
                    t={t}
                  />
                  <PRItem
                    number={36}
                    title="Update dependencies"
                    status="ready"
                    checks="passing"
                    t={t}
                  />
                  <PRItem
                    number={35}
                    title="Refactor database models"
                    status="draft"
                    checks="pending"
                    t={t}
                  />
                </div>
              </div>
            </div>
          </div>
        )}

        {/* AI Agents Tab */}
        {activeTab === 'ai-agents' && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <AIAgentCard
                name="PM Claude"
                status="active"
                currentTask="Reviewing PR #38"
                tasksCompleted={15}
                role={t.aiAgents.roles.pm}
                t={t}
              />
              <AIAgentCard
                name="Dev Codex"
                status="active"
                currentTask="Implementing auth system"
                tasksCompleted={22}
                role={t.aiAgents.roles.backend}
                t={t}
              />
              <AIAgentCard
                name="UX Gemini"
                status="idle"
                currentTask={t.common.none}
                tasksCompleted={8}
                role={t.aiAgents.roles.ux}
                t={t}
              />
            </div>

            {/* AI Discussion Panel */}
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
              <h2 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">{t.aiAgents.discussion}</h2>
              <div className="space-y-3">
                <DiscussionMessage
                  agent="PM Claude"
                  message={language === 'ko' 
                    ? "다음 스프린트를 위해 인증 기능을 우선순위로 두어야 합니다."
                    : "We need to prioritize the authentication feature for the next sprint."}
                  time={`10 ${t.common.minutesAgo}`}
                />
                <DiscussionMessage
                  agent="Dev Codex"
                  message={language === 'ko'
                    ? "오늘 JWT 토큰 시스템 구현을 시작할 수 있습니다."
                    : "I can start implementing the JWT token system today."}
                  time={`8 ${t.common.minutesAgo}`}
                />
                <DiscussionMessage
                  agent="UX Gemini"
                  message={language === 'ko'
                    ? "인증 프로세스를 위한 사용자 플로우 문서를 준비하겠습니다."
                    : "I'll prepare the user flow documentation for the auth process."}
                  time={`5 ${t.common.minutesAgo}`}
                />
              </div>
            </div>
          </div>
        )}

        {/* PM Control Tab */}
        {activeTab === 'pm-control' && (
          <PMControl />
        )}

        {/* Workflows Tab */}
        {activeTab === 'workflows' && (
          <div className="space-y-6">
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
              <h2 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">{t.workflows.active}</h2>
              <div className="space-y-4">
                <WorkflowItem
                  name={language === 'ko' ? "문서 생성 파이프라인" : "Document Creation Pipeline"}
                  status="running"
                  progress={65}
                  description={language === 'ko' 
                    ? "AI 지원으로 API 문서 생성 중"
                    : "Generating API documentation with AI assistance"}
                  t={t}
                />
                <WorkflowItem
                  name={language === 'ko' ? "코드 리뷰 자동화" : "Code Review Automation"}
                  status="completed"
                  progress={100}
                  description={language === 'ko'
                    ? "PR #38 자동 리뷰 완료"
                    : "Automated review of PR #38 completed"}
                  t={t}
                />
                <WorkflowItem
                  name={language === 'ko' ? "이슈 분류" : "Issue Triage"}
                  status="pending"
                  progress={0}
                  description={language === 'ko'
                    ? "새 이슈 처리 대기 중"
                    : "Waiting for new issues to process"}
                  t={t}
                />
              </div>
            </div>

            {/* Quick Actions */}
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
              <h2 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">{t.workflows.quickActions}</h2>
              <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
                <ActionButton label={t.workflows.actions.createIssue} icon="📝" />
                <ActionButton label={t.workflows.actions.startDiscussion} icon="💬" />
                <ActionButton label={t.workflows.actions.deploy} icon="🚀" />
                <ActionButton label={t.workflows.actions.generateReport} icon="📊" />
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

// Component definitions
function StatCard({ title, value, icon, trend, color }: any) {
  const colorClasses = {
    yellow: 'bg-yellow-100 text-yellow-600 dark:bg-yellow-900 dark:text-yellow-400',
    blue: 'bg-blue-100 text-blue-600 dark:bg-blue-900 dark:text-blue-400',
    green: 'bg-green-100 text-green-600 dark:bg-green-900 dark:text-green-400',
    purple: 'bg-purple-100 text-purple-600 dark:bg-purple-900 dark:text-purple-400'
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
      <div className="flex items-center justify-between mb-2">
        <span className="text-sm font-medium text-gray-500 dark:text-gray-400">{title}</span>
        <span className={`p-2 rounded-lg ${colorClasses[color]}`}>{icon}</span>
      </div>
      <div className="text-2xl font-bold text-gray-900 dark:text-white">{value}</div>
      <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">{trend}</p>
    </div>
  )
}

function ActivityItem({ type, message, time, t }: any) {
  const icons = {
    github: <GitBranch className="h-4 w-4" />,
    ai: <Users className="h-4 w-4" />,
    workflow: <Activity className="h-4 w-4" />
  }

  return (
    <div className="flex items-start space-x-3">
      <div className="flex-shrink-0 mt-1">{icons[type]}</div>
      <div className="flex-1 min-w-0">
        <p className="text-sm text-gray-900 dark:text-white">{message}</p>
        <p className="text-xs text-gray-500 dark:text-gray-400">{time}</p>
      </div>
    </div>
  )
}

function IssueItem({ number, title, labels, assignee }: any) {
  return (
    <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-3">
      <div className="flex items-start justify-between">
        <div>
          <span className="text-sm font-medium text-gray-900 dark:text-white">#{number} {title}</span>
          <div className="flex gap-2 mt-1">
            {labels.map((label: string) => (
              <span key={label} className="text-xs px-2 py-1 bg-gray-100 dark:bg-gray-700 rounded">
                {label}
              </span>
            ))}
          </div>
        </div>
        <span className="text-xs text-gray-500 dark:text-gray-400">{assignee}</span>
      </div>
    </div>
  )
}

function PRItem({ number, title, status, checks, t }: any) {
  const statusColors = {
    review: 'text-yellow-600',
    ready: 'text-green-600',
    draft: 'text-gray-600'
  }

  const statusText = {
    review: t.github.status.review,
    ready: t.github.status.ready,
    draft: t.github.status.draft
  }

  return (
    <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-3">
      <div className="flex items-start justify-between">
        <div>
          <span className="text-sm font-medium text-gray-900 dark:text-white">#{number} {title}</span>
          <div className="flex items-center gap-2 mt-1">
            <span className={`text-xs ${statusColors[status]}`}>{statusText[status]}</span>
            <span className="text-xs text-gray-500">• {t.github.checks}: {checks}</span>
          </div>
        </div>
      </div>
    </div>
  )
}

function AIAgentCard({ name, status, currentTask, tasksCompleted, role, t }: any) {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-semibold text-gray-900 dark:text-white">{name}</h3>
        <span className={`px-2 py-1 text-xs rounded-full ${
          status === 'active' ? 'bg-green-100 text-green-600' : 'bg-gray-100 text-gray-600'
        }`}>
          {status === 'active' ? t.aiAgents.status.active : t.aiAgents.status.idle}
        </span>
      </div>
      <p className="text-sm text-gray-500 dark:text-gray-400 mb-2">{role}</p>
      <p className="text-sm text-gray-900 dark:text-white mb-1">{t.aiAgents.current}: {currentTask}</p>
      <p className="text-xs text-gray-500 dark:text-gray-400">{t.aiAgents.tasksCompleted}: {tasksCompleted}</p>
    </div>
  )
}

function DiscussionMessage({ agent, message, time }: any) {
  return (
    <div className="flex space-x-3">
      <div className="flex-shrink-0">
        <MessageSquare className="h-5 w-5 text-gray-400" />
      </div>
      <div className="flex-1">
        <div className="flex items-center gap-2">
          <span className="text-sm font-medium text-gray-900 dark:text-white">{agent}</span>
          <span className="text-xs text-gray-500 dark:text-gray-400">{time}</span>
        </div>
        <p className="text-sm text-gray-700 dark:text-gray-300 mt-1">{message}</p>
      </div>
    </div>
  )
}

function WorkflowItem({ name, status, progress, description, t }: any) {
  const statusColors = {
    running: 'bg-blue-500',
    completed: 'bg-green-500',
    pending: 'bg-gray-300'
  }

  const statusText = {
    running: t.workflows.status.running,
    completed: t.workflows.status.completed,
    pending: t.workflows.status.pending
  }

  return (
    <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-4">
      <div className="flex justify-between items-start mb-2">
        <h3 className="font-medium text-gray-900 dark:text-white">{name}</h3>
        <span className="text-xs text-gray-500 dark:text-gray-400">{statusText[status]}</span>
      </div>
      <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">{description}</p>
      <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
        <div className={`h-2 rounded-full ${statusColors[status]}`} style={{ width: `${progress}%` }} />
      </div>
    </div>
  )
}

function ActionButton({ label, icon }: any) {
  return (
    <button className="flex flex-col items-center justify-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors">
      <span className="text-2xl mb-2">{icon}</span>
      <span className="text-sm text-gray-700 dark:text-gray-300">{label}</span>
    </button>
  )
}