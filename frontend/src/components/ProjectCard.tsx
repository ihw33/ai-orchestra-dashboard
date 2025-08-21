'use client'

import { useState, useEffect } from 'react'
import { Project, PROJECT_METRICS } from '@/config/projects'
import Link from 'next/link'

interface ProjectCardProps {
  project: Project
  metrics?: {
    issues?: { open: number; closed: number }
    pulls?: { open: number; merged: number }
    commits?: number
    lastActivity?: string
    status?: 'active' | 'idle' | 'maintenance'
  }
}

export default function ProjectCard({ project, metrics }: ProjectCardProps) {
  const customMetrics = PROJECT_METRICS[project.id as keyof typeof PROJECT_METRICS]
  const [isLive, setIsLive] = useState(false)
  const [pulseAnimation, setPulseAnimation] = useState(false)

  // Simulate real-time status updates
  useEffect(() => {
    const checkStatus = () => {
      // Simulate activity check
      const hasRecentActivity = Math.random() > 0.7
      setIsLive(hasRecentActivity)
      if (hasRecentActivity) {
        setPulseAnimation(true)
        setTimeout(() => setPulseAnimation(false), 1000)
      }
    }

    checkStatus()
    const interval = setInterval(checkStatus, 10000) // Check every 10 seconds
    return () => clearInterval(interval)
  }, [])

  // Determine project status
  const getStatusColor = () => {
    if (metrics?.status === 'maintenance') return 'bg-yellow-500'
    if (isLive) return 'bg-green-500'
    return 'bg-gray-400'
  }

  const getStatusText = () => {
    if (metrics?.status === 'maintenance') return 'Maintenance'
    if (isLive) return 'Active'
    return 'Idle'
  }
  
  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-6 hover:shadow-lg transition-all relative overflow-hidden">
      {/* Live Activity Indicator */}
      {isLive && (
        <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-transparent via-green-500 to-transparent animate-pulse" />
      )}
      
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className="relative">
            <span className="text-3xl">{project.icon}</span>
            {pulseAnimation && (
              <div className="absolute -inset-1 rounded-full bg-green-400 opacity-75 animate-ping" />
            )}
          </div>
          <div>
            <h3 className="font-semibold text-lg">{project.name}</h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">{project.description}</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <div className={`px-2 py-1 rounded-full text-xs font-medium flex items-center gap-1 ${
            isLive ? 'bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-300' :
            metrics?.status === 'maintenance' ? 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900 dark:text-yellow-300' :
            'bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-300'
          }`}>
            <div className={`w-2 h-2 rounded-full ${getStatusColor()} ${isLive ? 'animate-pulse' : ''}`} />
            {getStatusText()}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4 mb-4">
        <div className="bg-gray-50 dark:bg-gray-900 rounded-lg p-3">
          <div className="text-sm text-gray-600 dark:text-gray-400">Issues</div>
          <div className="text-xl font-semibold">
            {metrics?.issues ? (
              <>
                <span className="text-green-600">{metrics.issues.open}</span>
                <span className="text-gray-400 text-sm ml-1">/ {metrics.issues.closed}</span>
              </>
            ) : (
              <span className="text-gray-400">--</span>
            )}
          </div>
        </div>
        <div className="bg-gray-50 dark:bg-gray-900 rounded-lg p-3">
          <div className="text-sm text-gray-600 dark:text-gray-400">PRs</div>
          <div className="text-xl font-semibold">
            {metrics?.pulls ? (
              <>
                <span className="text-blue-600">{metrics.pulls.open}</span>
                <span className="text-gray-400 text-sm ml-1">/ {metrics.pulls.merged}</span>
              </>
            ) : (
              <span className="text-gray-400">--</span>
            )}
          </div>
        </div>
      </div>

      {customMetrics && (
        <div className="border-t border-gray-200 dark:border-gray-700 pt-4 mb-4">
          {project.id === 'iwl-v5' && 'matrix' in customMetrics && (
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-gray-600 dark:text-gray-400">Matrix Progress</span>
                <span className="font-medium">
                  {customMetrics.matrix.completed}/{customMetrics.matrix.total}
                </span>
              </div>
              <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                <div
                  className="bg-blue-500 h-2 rounded-full transition-all"
                  style={{
                    width: `${(customMetrics.matrix.completed / customMetrics.matrix.total) * 100}%`
                  }}
                />
              </div>
              <div className="text-sm text-gray-600 dark:text-gray-400">
                Phase: {customMetrics.phase} | Stage {customMetrics.stage.current}/{customMetrics.stage.total}
              </div>
            </div>
          )}
          
          {project.id === 'ai-engine' && 'models' in customMetrics && (
            <div className="space-y-2">
              <div className="text-sm text-gray-600 dark:text-gray-400">Active Models</div>
              <div className="flex flex-wrap gap-1">
                {customMetrics.models.map((model) => (
                  <span
                    key={model}
                    className="text-xs px-2 py-1 bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-300 rounded"
                  >
                    {model}
                  </span>
                ))}
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-600 dark:text-gray-400">Memory</span>
                <span className="font-medium">
                  {customMetrics.memory.used}GB / {customMetrics.memory.total}GB
                </span>
              </div>
            </div>
          )}
          
          {project.id === 'calligraphy' && 'round' in customMetrics && (
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-gray-600 dark:text-gray-400">Round {customMetrics.round}</span>
                <span className="font-medium">{customMetrics.progress}%</span>
              </div>
              <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                <div
                  className="bg-purple-500 h-2 rounded-full transition-all"
                  style={{ width: `${customMetrics.progress}%` }}
                />
              </div>
              <div className="flex gap-2">
                <span className={`text-xs px-2 py-1 rounded ${
                  customMetrics.pipeline.build === 'passing'
                    ? 'bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-300'
                    : 'bg-red-100 dark:bg-red-900 text-red-700 dark:text-red-300'
                }`}>
                  Build: {customMetrics.pipeline.build}
                </span>
                <span className={`text-xs px-2 py-1 rounded ${
                  customMetrics.pipeline.test === 'passing'
                    ? 'bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-300'
                    : 'bg-red-100 dark:bg-red-900 text-red-700 dark:text-red-300'
                }`}>
                  Test: {customMetrics.pipeline.test}
                </span>
              </div>
            </div>
          )}
        </div>
      )}

      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="flex -space-x-2">
            {project.team.slice(0, 3).map((member) => (
              <div
                key={member}
                className="w-8 h-8 rounded-full bg-gray-200 dark:bg-gray-700 flex items-center justify-center text-xs font-medium border-2 border-white dark:border-gray-800"
                title={member}
              >
                {member[0]}
              </div>
            ))}
            {project.team.length > 3 && (
              <div className="w-8 h-8 rounded-full bg-gray-200 dark:bg-gray-700 flex items-center justify-center text-xs font-medium border-2 border-white dark:border-gray-800">
                +{project.team.length - 3}
              </div>
            )}
          </div>
          
          {/* Last Activity */}
          {metrics?.lastActivity && (
            <div className="flex items-center gap-1 text-xs text-gray-500 dark:text-gray-400">
              <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              {metrics.lastActivity}
            </div>
          )}
        </div>
        
        <Link
          href={`/project/${project.id}`}
          className="text-sm font-medium hover:underline flex items-center gap-1"
          style={{ color: project.color }}
        >
          View Details
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
          </svg>
        </Link>
      </div>
    </div>
  )
}