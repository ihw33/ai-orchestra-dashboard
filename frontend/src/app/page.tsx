'use client'

import { useState, useEffect } from 'react'
import { GitBranch, Users, Activity, CheckCircle2, Clock, AlertCircle, BarChart3, MessageSquare } from 'lucide-react'

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState('overview')
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
                AI Orchestra Dashboard 🎭
              </h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-500 dark:text-gray-400">
                Status: <span className="text-green-500">● Connected</span>
              </span>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation Tabs */}
      <div className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <nav className="flex space-x-8" aria-label="Tabs">
            {['overview', 'github', 'ai-agents', 'workflows'].map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`
                  py-4 px-1 border-b-2 font-medium text-sm capitalize
                  ${activeTab === tab
                    ? 'border-blue-500 text-blue-600 dark:text-blue-400'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-300'
                  }
                `}
              >
                {tab.replace('-', ' ')}
              </button>
            ))}
          </nav>
        </div>
      </div>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Overview Tab */}
        {activeTab === 'overview' && (
          <div className="space-y-6">
            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <StatCard
                title="Active Issues"
                value="12"
                icon={<AlertCircle className="h-5 w-5" />}
                trend="+2 from yesterday"
                color="yellow"
              />
              <StatCard
                title="Open PRs"
                value="5"
                icon={<GitBranch className="h-5 w-5" />}
                trend="3 ready to merge"
                color="blue"
              />
              <StatCard
                title="AI Sessions"
                value="3"
                icon={<Users className="h-5 w-5" />}
                trend="2 active now"
                color="green"
              />
              <StatCard
                title="Tasks Completed"
                value="28"
                icon={<CheckCircle2 className="h-5 w-5" />}
                trend="+15 this week"
                color="purple"
              />
            </div>

            {/* Recent Activity */}
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
              <h2 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">Recent Activity</h2>
              <div className="space-y-3">
                <ActivityItem
                  type="github"
                  message="New issue #42 created: 'Implement user authentication'"
                  time="5 minutes ago"
                />
                <ActivityItem
                  type="ai"
                  message="Claude completed code review for PR #38"
                  time="15 minutes ago"
                />
                <ActivityItem
                  type="workflow"
                  message="Deployment pipeline triggered for main branch"
                  time="1 hour ago"
                />
                <ActivityItem
                  type="github"
                  message="PR #37 merged: 'Add dashboard components'"
                  time="2 hours ago"
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
                <h2 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">Open Issues</h2>
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
                <h2 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">Pull Requests</h2>
                <div className="space-y-3">
                  <PRItem
                    number={38}
                    title="Add user profile component"
                    status="review"
                    checks="passing"
                  />
                  <PRItem
                    number={36}
                    title="Update dependencies"
                    status="ready"
                    checks="passing"
                  />
                  <PRItem
                    number={35}
                    title="Refactor database models"
                    status="draft"
                    checks="pending"
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
                role="Project Manager"
              />
              <AIAgentCard
                name="Dev Codex"
                status="active"
                currentTask="Implementing auth system"
                tasksCompleted={22}
                role="Backend Developer"
              />
              <AIAgentCard
                name="UX Gemini"
                status="idle"
                currentTask="None"
                tasksCompleted={8}
                role="Content & UX"
              />
            </div>

            {/* AI Discussion Panel */}
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
              <h2 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">AI Discussion</h2>
              <div className="space-y-3">
                <DiscussionMessage
                  agent="PM Claude"
                  message="We need to prioritize the authentication feature for the next sprint."
                  time="10 minutes ago"
                />
                <DiscussionMessage
                  agent="Dev Codex"
                  message="I can start implementing the JWT token system today."
                  time="8 minutes ago"
                />
                <DiscussionMessage
                  agent="UX Gemini"
                  message="I'll prepare the user flow documentation for the auth process."
                  time="5 minutes ago"
                />
              </div>
            </div>
          </div>
        )}

        {/* Workflows Tab */}
        {activeTab === 'workflows' && (
          <div className="space-y-6">
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
              <h2 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">Active Workflows</h2>
              <div className="space-y-4">
                <WorkflowItem
                  name="Document Creation Pipeline"
                  status="running"
                  progress={65}
                  description="Generating API documentation with AI assistance"
                />
                <WorkflowItem
                  name="Code Review Automation"
                  status="completed"
                  progress={100}
                  description="Automated review of PR #38 completed"
                />
                <WorkflowItem
                  name="Issue Triage"
                  status="pending"
                  progress={0}
                  description="Waiting for new issues to process"
                />
              </div>
            </div>

            {/* Quick Actions */}
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
              <h2 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">Quick Actions</h2>
              <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
                <ActionButton label="Create Issue" icon="📝" />
                <ActionButton label="Start AI Discussion" icon="💬" />
                <ActionButton label="Deploy to Production" icon="🚀" />
                <ActionButton label="Generate Report" icon="📊" />
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

function ActivityItem({ type, message, time }: any) {
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

function PRItem({ number, title, status, checks }: any) {
  const statusColors = {
    review: 'text-yellow-600',
    ready: 'text-green-600',
    draft: 'text-gray-600'
  }

  return (
    <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-3">
      <div className="flex items-start justify-between">
        <div>
          <span className="text-sm font-medium text-gray-900 dark:text-white">#{number} {title}</span>
          <div className="flex items-center gap-2 mt-1">
            <span className={`text-xs ${statusColors[status]}`}>{status}</span>
            <span className="text-xs text-gray-500">• Checks: {checks}</span>
          </div>
        </div>
      </div>
    </div>
  )
}

function AIAgentCard({ name, status, currentTask, tasksCompleted, role }: any) {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-semibold text-gray-900 dark:text-white">{name}</h3>
        <span className={`px-2 py-1 text-xs rounded-full ${
          status === 'active' ? 'bg-green-100 text-green-600' : 'bg-gray-100 text-gray-600'
        }`}>
          {status}
        </span>
      </div>
      <p className="text-sm text-gray-500 dark:text-gray-400 mb-2">{role}</p>
      <p className="text-sm text-gray-900 dark:text-white mb-1">Current: {currentTask}</p>
      <p className="text-xs text-gray-500 dark:text-gray-400">Tasks completed: {tasksCompleted}</p>
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

function WorkflowItem({ name, status, progress, description }: any) {
  const statusColors = {
    running: 'bg-blue-500',
    completed: 'bg-green-500',
    pending: 'bg-gray-300'
  }

  return (
    <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-4">
      <div className="flex justify-between items-start mb-2">
        <h3 className="font-medium text-gray-900 dark:text-white">{name}</h3>
        <span className="text-xs text-gray-500 dark:text-gray-400">{status}</span>
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