'use client'

import { useState, useEffect, useMemo } from 'react'
import { PROJECTS, PROJECT_LIST } from '@/config/projects'

interface ProjectSelectorProps {
  selectedProject?: string
  onProjectSelect: (projectId: string) => void
}

export default function ProjectSelector({ selectedProject, onProjectSelect }: ProjectSelectorProps) {
  const [isOpen, setIsOpen] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')
  const [recentProjects, setRecentProjects] = useState<string[]>([])

  const currentProject = selectedProject ? PROJECTS[selectedProject] : null

  // Load recent projects from localStorage
  useEffect(() => {
    const stored = localStorage.getItem('recentProjects')
    if (stored) {
      setRecentProjects(JSON.parse(stored))
    }
  }, [])

  // Update recent projects when a project is selected
  const handleProjectSelect = (projectId: string) => {
    onProjectSelect(projectId)
    
    if (projectId) {
      const newRecent = [projectId, ...recentProjects.filter(id => id !== projectId)].slice(0, 3)
      setRecentProjects(newRecent)
      localStorage.setItem('recentProjects', JSON.stringify(newRecent))
    }
    
    setIsOpen(false)
    setSearchQuery('')
  }

  // Filter projects based on search query
  const filteredProjects = useMemo(() => {
    if (!searchQuery) return PROJECT_LIST
    
    const query = searchQuery.toLowerCase()
    return PROJECT_LIST.filter(project => 
      project.name.toLowerCase().includes(query) ||
      project.description.toLowerCase().includes(query) ||
      project.features?.some(f => f.toLowerCase().includes(query))
    )
  }, [searchQuery])

  // Get recent project objects
  const recentProjectObjects = useMemo(() => {
    return recentProjects
      .map(id => PROJECTS[id])
      .filter(Boolean)
      .slice(0, 3)
  }, [recentProjects])

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 px-4 py-2 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
      >
        {currentProject ? (
          <>
            <span className="text-2xl">{currentProject.icon}</span>
            <span className="font-medium">{currentProject.name}</span>
          </>
        ) : (
          <>
            <span className="text-gray-500">🔍</span>
            <span className="text-gray-600 dark:text-gray-400">Select Project</span>
          </>
        )}
        <svg
          className={`w-4 h-4 transition-transform ${isOpen ? 'rotate-180' : ''}`}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {isOpen && (
        <div className="absolute top-full mt-2 w-96 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg z-50">
          {/* Search Input */}
          <div className="p-3 border-b border-gray-200 dark:border-gray-700">
            <div className="relative">
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search projects..."
                className="w-full pl-9 pr-3 py-2 bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
                autoFocus
              />
              <svg
                className="absolute left-3 top-2.5 w-4 h-4 text-gray-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
          </div>

          {/* Recent Projects */}
          {!searchQuery && recentProjectObjects.length > 0 && (
            <div className="p-2 border-b border-gray-200 dark:border-gray-700">
              <div className="px-3 py-1 text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">
                Recent Projects
              </div>
              {recentProjectObjects.map((project) => (
                <button
                  key={project.id}
                  onClick={() => handleProjectSelect(project.id)}
                  className={`w-full text-left px-3 py-2 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors ${
                    selectedProject === project.id ? 'bg-gray-100 dark:bg-gray-700' : ''
                  }`}
                >
                  <div className="flex items-center gap-2">
                    <span className="text-lg">{project.icon}</span>
                    <span className="text-sm font-medium">{project.name}</span>
                    <svg className="w-3 h-3 text-gray-400 ml-auto" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd" />
                    </svg>
                  </div>
                </button>
              ))}
            </div>
          )}

          {/* All Projects or Search Results */}
          <div className="p-2 max-h-96 overflow-y-auto">
            {searchQuery && filteredProjects.length === 0 ? (
              <div className="px-3 py-4 text-center text-sm text-gray-500 dark:text-gray-400">
                No projects found matching "{searchQuery}"
              </div>
            ) : (
              <>
                {!searchQuery && (
                  <div className="px-3 py-1 text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">
                    All Projects
                  </div>
                )}
                {filteredProjects.map((project) => (
                  <button
                    key={project.id}
                    onClick={() => handleProjectSelect(project.id)}
                    className={`w-full text-left px-3 py-2 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors ${
                      selectedProject === project.id ? 'bg-gray-100 dark:bg-gray-700' : ''
                    }`}
                  >
                    <div className="flex items-start gap-3">
                      <span className="text-2xl mt-1">{project.icon}</span>
                      <div className="flex-1">
                        <div className="font-medium flex items-center gap-2">
                          {project.name}
                          {selectedProject === project.id && (
                            <span className="text-xs px-2 py-0.5 bg-blue-100 dark:bg-blue-900 text-blue-600 dark:text-blue-400 rounded">
                              Active
                            </span>
                          )}
                        </div>
                        <div className="text-sm text-gray-600 dark:text-gray-400">
                          {project.description}
                        </div>
                        <div className="flex gap-1 mt-1">
                          {project.features?.map((feature, idx) => (
                            <span
                              key={idx}
                              className="text-xs px-2 py-0.5 bg-gray-100 dark:bg-gray-700 rounded"
                            >
                              {feature}
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>
                  </button>
                ))}
              </>
            )}
          </div>
          
          {/* View All Button */}
          <div className="border-t border-gray-200 dark:border-gray-700 p-2">
            <button
              onClick={() => handleProjectSelect('')}
              className="w-full text-left px-3 py-2 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors text-sm text-gray-600 dark:text-gray-400"
            >
              View All Projects
            </button>
          </div>
        </div>
      )}
    </div>
  )
}