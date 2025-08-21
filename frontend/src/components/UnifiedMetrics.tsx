'use client'

import { useEffect, useState } from 'react'

interface MetricCardProps {
  title: string
  value: number | string
  trend?: 'up' | 'down' | 'stable'
  trendValue?: string
  icon?: string
  color?: string
}

function MetricCard({ title, value, trend, trendValue, icon, color = '#3B82F6' }: MetricCardProps) {
  const [animatedValue, setAnimatedValue] = useState(0)
  
  useEffect(() => {
    if (typeof value === 'number') {
      const timer = setTimeout(() => {
        setAnimatedValue(value)
      }, 100)
      return () => clearTimeout(timer)
    }
  }, [value])

  const displayValue = typeof value === 'number' ? animatedValue : value

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-6 hover:shadow-lg transition-all">
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          {icon && <span className="text-2xl">{icon}</span>}
          <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400">{title}</h3>
        </div>
        {trend && (
          <div className={`flex items-center gap-1 text-sm ${
            trend === 'up' ? 'text-green-600' : 
            trend === 'down' ? 'text-red-600' : 
            'text-gray-600'
          }`}>
            {trend === 'up' && (
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 10l7-7m0 0l7 7m-7-7v18" />
              </svg>
            )}
            {trend === 'down' && (
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 14l-7 7m0 0l-7-7m7 7V3" />
              </svg>
            )}
            {trendValue && <span>{trendValue}</span>}
          </div>
        )}
      </div>
      
      <div 
        className="text-3xl font-bold transition-all duration-500"
        style={{ color: typeof value === 'number' && animatedValue > 0 ? color : undefined }}
      >
        {displayValue}
      </div>
    </div>
  )
}

interface UnifiedMetricsProps {
  metrics?: {
    totalIssues?: number
    activePRs?: number
    aiSessions?: number
    totalCommits?: number
    activeContributors?: number
    completionRate?: number
  }
}

export default function UnifiedMetrics({ metrics }: UnifiedMetricsProps) {
  const defaultMetrics = {
    totalIssues: metrics?.totalIssues ?? 35,
    activePRs: metrics?.activePRs ?? 10,
    aiSessions: metrics?.aiSessions ?? 9,
    totalCommits: metrics?.totalCommits ?? 247,
    activeContributors: metrics?.activeContributors ?? 6,
    completionRate: metrics?.completionRate ?? 68
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-semibold mb-4">Unified Metrics</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <MetricCard
            title="Total Issues"
            value={defaultMetrics.totalIssues}
            icon="📋"
            trend="up"
            trendValue="+12%"
            color="#3B82F6"
          />
          <MetricCard
            title="Active PRs"
            value={defaultMetrics.activePRs}
            icon="🔄"
            trend="stable"
            color="#10B981"
          />
          <MetricCard
            title="AI Sessions"
            value={defaultMetrics.aiSessions}
            icon="🤖"
            trend="up"
            trendValue="+3"
            color="#8B5CF6"
          />
          <MetricCard
            title="Total Commits"
            value={defaultMetrics.totalCommits}
            icon="💾"
            trend="up"
            trendValue="+28"
            color="#F59E0B"
          />
          <MetricCard
            title="Active Contributors"
            value={defaultMetrics.activeContributors}
            icon="👥"
            trend="stable"
            color="#EF4444"
          />
          <MetricCard
            title="Completion Rate"
            value={`${defaultMetrics.completionRate}%`}
            icon="✅"
            trend="up"
            trendValue="+5%"
            color="#10B981"
          />
        </div>
      </div>

      <div>
        <h3 className="text-lg font-semibold mb-3">Quick Stats</h3>
        <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-6">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">3</div>
              <div className="text-sm text-gray-600 dark:text-gray-400">Active Projects</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">12</div>
              <div className="text-sm text-gray-600 dark:text-gray-400">Open Tasks</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-purple-600">4</div>
              <div className="text-sm text-gray-600 dark:text-gray-400">In Review</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-orange-600">85%</div>
              <div className="text-sm text-gray-600 dark:text-gray-400">Sprint Progress</div>
            </div>
          </div>
        </div>
      </div>

      <div>
        <h3 className="text-lg font-semibold mb-3">Activity Timeline</h3>
        <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-6">
          <div className="space-y-4">
            <ActivityItem
              time="2 mins ago"
              action="PR merged"
              description="feat: Add multi-project support"
              project="iwl-v5"
              color="#3B82F6"
            />
            <ActivityItem
              time="15 mins ago"
              action="Issue closed"
              description="#142: Fix dashboard layout"
              project="ai-engine"
              color="#10B981"
            />
            <ActivityItem
              time="1 hour ago"
              action="Commit pushed"
              description="Update calligraphy round 1-2"
              project="calligraphy"
              color="#8B5CF6"
            />
            <ActivityItem
              time="2 hours ago"
              action="AI session started"
              description="Gemini working on data collection"
              project="ai-engine"
              color="#10B981"
            />
          </div>
        </div>
      </div>
    </div>
  )
}

function ActivityItem({ 
  time, 
  action, 
  description, 
  project, 
  color 
}: { 
  time: string
  action: string
  description: string
  project: string
  color: string
}) {
  return (
    <div className="flex items-start gap-3">
      <div 
        className="w-2 h-2 rounded-full mt-2"
        style={{ backgroundColor: color }}
      />
      <div className="flex-1">
        <div className="flex items-center gap-2 text-sm">
          <span className="font-medium">{action}</span>
          <span className="text-gray-500">•</span>
          <span className="text-gray-600 dark:text-gray-400">{time}</span>
        </div>
        <div className="text-sm text-gray-700 dark:text-gray-300 mt-1">
          {description}
        </div>
        <div className="text-xs text-gray-500 mt-1">
          Project: {project}
        </div>
      </div>
    </div>
  )
}