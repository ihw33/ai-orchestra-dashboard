'use client'

import { useState, useEffect } from 'react'
import { Bot, Send, Users, FileText, CheckCircle, AlertCircle, RefreshCw } from 'lucide-react'
import { useLanguage } from '@/contexts/LanguageContext'
import PingAnimation from './PingAnimation'

interface Issue {
  number: number
  title: string
  body: string
  state: string
  labels: string[]
}

interface TaskAssignment {
  cli: string
  task: string
  priority: string
  status: string
}

export default function PMControl() {
  const { language, t } = useLanguage()
  const [selectedIssue, setSelectedIssue] = useState<Issue | null>(null)
  const [taskAssignments, setTaskAssignments] = useState<TaskAssignment[]>([])
  const [pendingDecisions, setPendingDecisions] = useState<any[]>([])
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [collaborationTopic, setCollaborationTopic] = useState('')
  const [selectedTemplate, setSelectedTemplate] = useState('feature_planning')
  const [detectedCLIs, setDetectedCLIs] = useState<any>({})
  const [isDetecting, setIsDetecting] = useState(false)
  const [selectedCLIForTask, setSelectedCLIForTask] = useState<{[key: string]: string}>({})
  const [manualTaskDesc, setManualTaskDesc] = useState('')
  const [selectedManualCLI, setSelectedManualCLI] = useState('')
  const [isAssigning, setIsAssigning] = useState(false)
  const [pingingCLIs, setPingingCLIs] = useState<string[]>([])
  const [pingResults, setPingResults] = useState<{[key: string]: 'success' | 'pending' | 'error'}>({})
  const [showPingAnimation, setShowPingAnimation] = useState(false)
  const [pingAnimationTarget, setPingAnimationTarget] = useState<string>('')
  
  // 번역 텍스트
  const texts = {
    ko: {
      title: 'PM AI 제어 패널',
      selectIssue: '이슈 선택',
      analyzeAssign: '분석 및 할당',
      analyzing: '분석 중...',
      taskBreakdown: '업무 분해',
      assignedTo: '할당 대상',
      priority: '우선순위',
      status: '상태',
      pendingDecisions: '대기 중인 결정사항',
      approve: '승인',
      reject: '거부',
      requestRevision: '수정 요청',
      startCollaboration: '협업 시작',
      collaborationTopic: '협업 주제',
      template: '템플릿',
      participants: '참여자',
      allCLIs: '모든 CLI',
      sendCommand: 'CLI 명령 전송',
      broadcast: '전체 공지',
      monitoringPanel: '모니터링 패널',
      activeAssignments: '활성 할당',
      completedToday: '오늘 완료',
      pendingReview: '검토 대기',
      detectCLIs: 'CLI 감지',
      availableCLIs: '사용 가능한 CLI',
      detecting: '감지 중...',
      capabilities: '기능',
      selectCLI: 'CLI 선택',
      projectInfo: '프로젝트',
      pidInfo: 'PID',
      assignTo: '할당 대상 CLI'
    },
    en: {
      title: 'PM AI Control Panel',
      selectIssue: 'Select Issue',
      analyzeAssign: 'Analyze & Assign',
      analyzing: 'Analyzing...',
      taskBreakdown: 'Task Breakdown',
      assignedTo: 'Assigned To',
      priority: 'Priority',
      status: 'Status',
      pendingDecisions: 'Pending Decisions',
      approve: 'Approve',
      reject: 'Reject',
      requestRevision: 'Request Revision',
      startCollaboration: 'Start Collaboration',
      collaborationTopic: 'Collaboration Topic',
      template: 'Template',
      participants: 'Participants',
      allCLIs: 'All CLIs',
      sendCommand: 'Send CLI Command',
      broadcast: 'Broadcast',
      monitoringPanel: 'Monitoring Panel',
      activeAssignments: 'Active Assignments',
      completedToday: 'Completed Today',
      pendingReview: 'Pending Review',
      detectCLIs: 'Detect CLIs',
      availableCLIs: 'Available CLIs',
      detecting: 'Detecting...',
      capabilities: 'Capabilities',
      selectCLI: 'Select CLI',
      projectInfo: 'Project',
      pidInfo: 'PID',
      assignTo: 'Assign to CLI'
    }
  }
  
  const t_pm = texts[language]
  
  // 이슈 분석 및 할당
  const analyzeAndAssign = async () => {
    if (!selectedIssue) return
    
    setIsAnalyzing(true)
    
    try {
      const response = await fetch('http://localhost:8000/api/pm/analyze-issue', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          issue_number: selectedIssue.number,
          repo_name: 'ai-orchestra-dashboard',
          auto_assign: true,
          selected_clis: selectedCLIForTask  // 선택된 CLI 정보 전달
        })
      })
      
      const data = await response.json()
      
      if (data.assignments) {
        setTaskAssignments(data.assignments)
      }
    } catch (error) {
      console.error('Failed to analyze issue:', error)
    } finally {
      setIsAnalyzing(false)
    }
  }
  
  // 의사결정 처리
  const makeDecision = async (type: string, details: any = {}) => {
    try {
      const response = await fetch('http://localhost:8000/api/pm/make-decision', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          type,
          issue_number: selectedIssue?.number,
          repo_name: 'ai-orchestra-dashboard',
          details
        })
      })
      
      const data = await response.json()
      console.log('Decision made:', data)
      
      // 대기 중인 결정사항 새로고침
      fetchPendingDecisions()
    } catch (error) {
      console.error('Failed to make decision:', error)
    }
  }
  
  // 협업 시작
  const startCollaboration = async () => {
    if (!collaborationTopic) return
    
    try {
      const response = await fetch('http://localhost:8000/api/pm/start-collaboration', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          topic: collaborationTopic,
          template: selectedTemplate,
          participants: ['all'],
          repo_name: 'ai-orchestra-dashboard'
        })
      })
      
      const data = await response.json()
      console.log('Collaboration started:', data)
      
      setCollaborationTopic('')
    } catch (error) {
      console.error('Failed to start collaboration:', error)
    }
  }
  
  // CLI 감지
  const detectCLIs = async () => {
    setIsDetecting(true)
    try {
      const response = await fetch('http://localhost:8000/api/pm/detect-clis')
      const data = await response.json()
      setDetectedCLIs(data.detected || {})
    } catch (error) {
      console.error('Failed to detect CLIs:', error)
    } finally {
      setIsDetecting(false)
    }
  }
  
  // 대기 중인 결정사항 가져오기
  const fetchPendingDecisions = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/pm/pending-decisions')
      const data = await response.json()
      setPendingDecisions(data.pending || [])
    } catch (error) {
      console.error('Failed to fetch pending decisions:', error)
    }
  }
  
  useEffect(() => {
    fetchPendingDecisions()
    detectCLIs() // 초기 CLI 감지
    const interval = setInterval(fetchPendingDecisions, 10000) // 10초마다 새로고침
    return () => clearInterval(interval)
  }, [])
  
  return (
    <div className="space-y-6">
      {/* Connected CLI List */}
      <div className="bg-green-50 dark:bg-green-900/20 rounded-lg shadow p-4 mb-4">
        <h3 className="text-md font-semibold mb-2 text-green-700 dark:text-green-400">
          🟢 연결된 CLI 모니터
        </h3>
        <div className="flex flex-wrap gap-2">
          {detectedCLIs.active_clis && Object.entries(detectedCLIs.active_clis)
            .filter(([_, cli]: any) => cli.monitor_connected)
            .map(([name, cli]: any) => (
              <div key={name} className={`flex items-center gap-2 px-3 py-1 bg-white dark:bg-gray-800 rounded-full border transition-all ${
                pingingCLIs.includes(name) 
                  ? 'border-yellow-400 bg-yellow-50 dark:bg-yellow-900/20 animate-pulse' 
                  : 'border-green-300 dark:border-green-700'
              }`}>
                <span className={`w-2 h-2 rounded-full ${
                  pingingCLIs.includes(name)
                    ? 'bg-yellow-500 animate-ping'
                    : 'bg-green-500 animate-pulse'
                }`} />
                <span className="text-sm font-medium">{name.toUpperCase()}</span>
                <span className="text-xs text-gray-500">({cli.monitor_status})</span>
                {pingingCLIs.includes(name) && (
                  <span className="text-xs text-yellow-600 dark:text-yellow-400">🏓 Pinging...</span>
                )}
              </div>
            ))
          }
          {(!detectedCLIs.active_clis || Object.values(detectedCLIs.active_clis).filter((cli: any) => cli.monitor_connected).length === 0) && (
            <span className="text-sm text-gray-500">연결된 모니터가 없습니다</span>
          )}
        </div>
        <button
          onClick={async () => {
            setShowPingAnimation(true)
            setPingAnimationTarget('all')
            
            // 모든 연결된 CLI를 pinging 상태로 설정
            const connectedCLIs = Object.entries(detectedCLIs.active_clis || {})
              .filter(([_, cli]: any) => cli.monitor_connected)
              .map(([name]) => name)
            
            setPingingCLIs(connectedCLIs)
            
            try {
              const response = await fetch('http://localhost:8000/api/pm/ping-all', {
                method: 'POST'
              })
              const data = await response.json()
              
              // 성공 애니메이션
              setTimeout(() => {
                setPingingCLIs([])
                setShowPingAnimation(false)
                
                // 성공 메시지 표시
                const successDiv = document.createElement('div')
                successDiv.className = 'fixed top-4 right-4 bg-green-500 text-white px-4 py-2 rounded-lg shadow-lg z-50 animate-pulse'
                successDiv.innerHTML = `✅ Ping sent to ${data.pinged_count} CLIs!`
                document.body.appendChild(successDiv)
                
                setTimeout(() => successDiv.remove(), 3000)
              }, 1500)
            } catch (error) {
              console.error('Failed to ping:', error)
              setPingingCLIs([])
              setShowPingAnimation(false)
            }
          }}
          className="mt-2 px-3 py-1 text-sm bg-green-500 text-white rounded hover:bg-green-600 transition-all"
        >
          🏓 모든 CLI에 Ping 보내기
        </button>
      </div>
      
      {/* Ping Animation Overlay */}
      {showPingAnimation && pingAnimationTarget && (
        <div className="fixed inset-0 z-40 pointer-events-none">
          <PingAnimation 
            cliName={pingAnimationTarget} 
            onComplete={() => {
              setShowPingAnimation(false)
              setPingAnimationTarget('')
            }}
          />
        </div>
      )}
      
      {/* CLI Status Panel */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-lg font-semibold">{t_pm.availableCLIs}</h2>
          <button
            onClick={detectCLIs}
            disabled={isDetecting}
            className="px-3 py-1 text-sm bg-gray-100 dark:bg-gray-700 rounded hover:bg-gray-200 dark:hover:bg-gray-600"
          >
            {isDetecting ? t_pm.detecting : t_pm.detectCLIs}
          </button>
        </div>
        <div className="space-y-2">
          {detectedCLIs.active_clis && Object.entries(detectedCLIs.active_clis).map(([name, cli]: any) => {
            // 상태 아이콘 결정
            let statusIcon = '❌'
            let statusText = 'Not Running'
            let statusColor = 'bg-gray-100 text-gray-500'
            
            if (cli.available) {
              statusIcon = '✅'
              statusText = 'Monitor Connected'
              statusColor = 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400'
            } else if (cli.main_process) {
              statusIcon = '🟡'
              statusText = 'App Only (No Monitor)'
              statusColor = 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400'
            }
            
            return (
              <div key={name} className="border rounded-lg p-3 dark:border-gray-700">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-2">
                    <span className="text-lg">{statusIcon}</span>
                    <span className="font-semibold text-sm">{name.toUpperCase()}</span>
                    <span className={`px-2 py-0.5 text-xs rounded ${statusColor}`}>
                      {statusText}
                    </span>
                  </div>
                  {cli.monitor_connected && (
                    <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
                  )}
                </div>
                
                <div className="grid grid-cols-2 gap-2 text-xs">
                  <div>
                    <span className="text-gray-500">앱 실행:</span>
                    <span className="ml-2">{cli.main_process ? 'Yes' : 'No'}</span>
                  </div>
                  <div>
                    <span className="text-gray-500">모니터:</span>
                    <span className="ml-2">{cli.monitor_connected ? 'Connected' : 'Not Connected'}</span>
                  </div>
                  {cli.monitor_connected && (
                    <>
                      <div>
                        <span className="text-gray-500">상태:</span>
                        <span className="ml-2">{cli.monitor_status}</span>
                      </div>
                      <div>
                        <span className="text-gray-500">대기 작업:</span>
                        <span className="ml-2">{cli.pending_tasks || 0}</span>
                      </div>
                    </>
                  )}
                  {cli.completed_tasks > 0 && (
                    <div className="col-span-2">
                      <span className="text-gray-500">완료된 작업:</span>
                      <span className="ml-2">{cli.completed_tasks}</span>
                    </div>
                  )}
                </div>
                
                {!cli.monitor_connected && cli.main_process && (
                  <div className="mt-2 p-2 bg-yellow-50 dark:bg-yellow-900/20 rounded text-xs">
                    ⚠️ 모니터를 실행하세요:
                    <code className="block mt-1 font-mono bg-gray-100 dark:bg-gray-800 p-1 rounded">
                      python scripts/cli_monitor.py --cli {name}
                    </code>
                  </div>
                )}
              </div>
            )
          })}
        </div>
      </div>
      
      {/* Manual Task Assignment Section */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
          <Send className="h-5 w-5 text-purple-500" />
          수동 작업 할당
        </h3>
        
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium mb-2">작업 설명</label>
            <textarea 
              className="w-full p-2 border rounded-lg dark:bg-gray-700"
              rows={3}
              placeholder="예: Frontend 컴포넌트 리팩토링..."
              value={manualTaskDesc}
              onChange={(e) => setManualTaskDesc(e.target.value)}
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium mb-2">할당할 CLI 선택</label>
            <select 
              className="w-full p-2 border rounded-lg dark:bg-gray-700 mb-2"
              value={selectedManualCLI}
              onChange={(e) => setSelectedManualCLI(e.target.value)}
            >
              <option value="">연결된 CLI 선택...</option>
              {detectedCLIs.active_clis && Object.entries(detectedCLIs.active_clis).map(([name, cli]: any) => {
                // 모니터가 연결된 것만 표시
                if (!cli.monitor_connected) return null
                return (
                  <option key={name} value={name}>
                    ✅ {name.toUpperCase()} - {cli.monitor_status}
                  </option>
                )
              })}
              {/* 연결되지 않은 CLI는 비활성화 상태로 표시 */}
              {detectedCLIs.active_clis && Object.entries(detectedCLIs.active_clis).map(([name, cli]: any) => {
                if (!cli.main_process || cli.monitor_connected) return null
                return (
                  <option key={`disabled_${name}`} value="" disabled>
                    🟡 {name.toUpperCase()} - 모니터 실행 필요
                  </option>
                )
              })}
            </select>
            
            <button 
              className="w-full px-4 py-2 bg-purple-500 text-white rounded-lg hover:bg-purple-600 disabled:bg-gray-400"
              disabled={!manualTaskDesc || !selectedManualCLI || isAssigning}
              onClick={async () => {
                setIsAssigning(true)
                try {
                  const response = await fetch('http://localhost:8000/api/pm/manual-assign', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                      cli_name: selectedManualCLI,
                      description: manualTaskDesc,
                      priority: 'normal'
                    })
                  })
                  
                  const data = await response.json()
                  if (data.status === 'success') {
                    alert(`✅ 작업이 ${selectedManualCLI}에 할당되었습니다!`)
                    setManualTaskDesc('')
                    setSelectedManualCLI('')
                  }
                } catch (error) {
                  console.error('Failed to assign task:', error)
                  alert('작업 할당 실패')
                } finally {
                  setIsAssigning(false)
                }
              }}
            >
              {isAssigning ? '할당 중...' : '작업 할당'}
            </button>
          </div>
        </div>
      </div>
      
      {/* PM Control Header */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
          <Bot className="h-6 w-6 text-blue-500" />
          {t_pm.title}
        </h2>
        
        {/* Issue Analysis Section */}
        <div className="space-y-4">
          <div className="flex gap-4">
            <select 
              className="flex-1 p-2 border rounded-lg dark:bg-gray-700"
              onChange={(e) => {
                // In real app, fetch issue details
                setSelectedIssue({
                  number: parseInt(e.target.value),
                  title: `Issue #${e.target.value}`,
                  body: 'Issue content',
                  state: 'open',
                  labels: []
                })
              }}
            >
              <option value="">{t_pm.selectIssue}</option>
              <option value="42">#42 - Implement user authentication</option>
              <option value="41">#41 - Fix responsive design</option>
              <option value="40">#40 - Add API documentation</option>
            </select>
            
            <button
              onClick={analyzeAndAssign}
              disabled={!selectedIssue || isAnalyzing}
              className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-400 flex items-center gap-2"
            >
              {isAnalyzing ? (
                <>
                  <RefreshCw className="h-4 w-4 animate-spin" />
                  {t_pm.analyzing}
                </>
              ) : (
                <>
                  <Send className="h-4 w-4" />
                  {t_pm.analyzeAssign}
                </>
              )}
            </button>
          </div>
          
          {/* Task Assignments Display */}
          {taskAssignments.length > 0 && (
            <div className="mt-4">
              <h3 className="font-semibold mb-2">{t_pm.taskBreakdown}</h3>
              <div className="space-y-2">
                {taskAssignments.map((assignment, idx) => (
                  <div key={idx} className="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                    <div className="flex justify-between items-start">
                      <div>
                        <p className="font-medium">{assignment.task}</p>
                        <p className="text-sm text-gray-500">
                          {t_pm.assignedTo}: <span className="font-semibold">{assignment.cli}</span>
                          {assignment.project && (
                            <span className="ml-2">({assignment.project})</span>
                          )}
                          <span className="mx-2">|</span>
                          {t_pm.priority}: {assignment.priority}
                        </p>
                      </div>
                      <span className="px-2 py-1 text-xs bg-green-100 text-green-600 rounded">
                        {assignment.status}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
      
      {/* Pending Decisions */}
      {pendingDecisions.length > 0 && (
        <div className="bg-yellow-50 dark:bg-yellow-900/20 rounded-lg shadow p-6">
          <h3 className="font-semibold mb-4 flex items-center gap-2">
            <AlertCircle className="h-5 w-5 text-yellow-500" />
            {t_pm.pendingDecisions}
          </h3>
          <div className="space-y-3">
            {pendingDecisions.map((decision, idx) => (
              <div key={idx} className="p-4 bg-white dark:bg-gray-800 rounded-lg">
                <p className="mb-3">{decision.description}</p>
                <div className="flex gap-2">
                  <button
                    onClick={() => makeDecision('approve_completion', decision)}
                    className="px-3 py-1 bg-green-500 text-white rounded hover:bg-green-600"
                  >
                    {t_pm.approve}
                  </button>
                  <button
                    onClick={() => makeDecision('request_revision', decision)}
                    className="px-3 py-1 bg-yellow-500 text-white rounded hover:bg-yellow-600"
                  >
                    {t_pm.requestRevision}
                  </button>
                  <button
                    onClick={() => makeDecision('reject', decision)}
                    className="px-3 py-1 bg-red-500 text-white rounded hover:bg-red-600"
                  >
                    {t_pm.reject}
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
      
      {/* Collaboration Starter */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <h3 className="font-semibold mb-4 flex items-center gap-2">
          <Users className="h-5 w-5 text-purple-500" />
          {t_pm.startCollaboration}
        </h3>
        <div className="space-y-3">
          <input
            type="text"
            placeholder={t_pm.collaborationTopic}
            value={collaborationTopic}
            onChange={(e) => setCollaborationTopic(e.target.value)}
            className="w-full p-2 border rounded-lg dark:bg-gray-700"
          />
          
          <select
            value={selectedTemplate}
            onChange={(e) => setSelectedTemplate(e.target.value)}
            className="w-full p-2 border rounded-lg dark:bg-gray-700"
          >
            <option value="feature_planning">Feature Planning</option>
            <option value="bug_fix">Bug Fix</option>
            <option value="documentation">Documentation</option>
          </select>
          
          <button
            onClick={startCollaboration}
            disabled={!collaborationTopic}
            className="w-full px-4 py-2 bg-purple-500 text-white rounded-lg hover:bg-purple-600 disabled:bg-gray-400"
          >
            <Users className="h-4 w-4 inline mr-2" />
            {t_pm.startCollaboration}
          </button>
        </div>
      </div>
      
      {/* Monitoring Stats */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <h3 className="font-semibold mb-4">{t_pm.monitoringPanel}</h3>
        <div className="grid grid-cols-3 gap-4">
          <div className="text-center">
            <p className="text-2xl font-bold text-blue-500">{taskAssignments.length}</p>
            <p className="text-sm text-gray-500">{t_pm.activeAssignments}</p>
          </div>
          <div className="text-center">
            <p className="text-2xl font-bold text-green-500">8</p>
            <p className="text-sm text-gray-500">{t_pm.completedToday}</p>
          </div>
          <div className="text-center">
            <p className="text-2xl font-bold text-yellow-500">{pendingDecisions.length}</p>
            <p className="text-sm text-gray-500">{t_pm.pendingReview}</p>
          </div>
        </div>
      </div>
    </div>
  )
}