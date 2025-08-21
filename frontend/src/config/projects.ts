// 멀티 프로젝트 설정
export interface Project {
  id: string
  name: string
  github: string
  path: string
  color: string
  bgColor: string
  icon: string
  team: string[]
  description: string
  features?: string[]
}

export const PROJECTS: Record<string, Project> = {
  'iwl-v5': {
    id: 'iwl-v5',
    name: 'IWL v5 Rebuild',
    github: 'ihw33/iwl-v5-rebuild',
    path: '/Users/m4_macbook/Projects/iwl-v5-rebuild',
    color: '#3B82F6',
    bgColor: 'bg-blue-500',
    icon: '📚',
    team: ['PM Claude', 'Cursor', 'Codex', 'Gemini', 'QA Claude'],
    description: '8×4 매트릭스 학습 플랫폼',
    features: ['8×4 Matrix', 'Phase 기반', 'Wiki 문서']
  },
  'ai-engine': {
    id: 'ai-engine',
    name: 'AI Engine Hub',
    github: 'ihw33/ai-engine-hub',
    path: '/Users/m4_macbook/Projects/ai-engine-hub',
    color: '#10B981',
    bgColor: 'bg-green-500',
    icon: '🤖',
    team: ['Gemini', 'Codex', 'Claude'],
    description: '공유 AI 인프라 플랫폼',
    features: ['Ollama 모델', 'GPT-OSS:20b', 'API 서버']
  },
  'calligraphy': {
    id: 'calligraphy',
    name: 'Calligraphy Coach v2',
    github: 'ihw33/calligraphy-coach-v2',
    path: '/Users/m4_macbook/calligraphy-coach-v2',
    color: '#8B5CF6',
    bgColor: 'bg-purple-500',
    icon: '🎨',
    team: ['PM Claude', 'Gemini', 'Codex', 'Cursor'],
    description: 'AI 기반 서예 학습 앱',
    features: ['모노레포', 'Round 기반', 'Storybook']
  }
}

// 프로젝트 목록 배열
export const PROJECT_LIST = Object.values(PROJECTS)

// 팀원 정보
export const TEAM_MEMBERS = {
  'PM Claude': { role: 'Project Manager', icon: '👨‍💼', status: 'active' },
  'Cursor': { role: 'Content/Design', icon: '🎨', status: 'active' },
  'Codex': { role: 'Backend/API', icon: '🔧', status: 'active' },
  'Gemini': { role: 'Data/Architecture', icon: '📊', status: 'active' },
  'QA Claude': { role: 'Quality Assurance', icon: '✅', status: 'idle' },
  'VSCode Claude': { role: 'Frontend', icon: '💻', status: 'active' }
}

// GitHub API 엔드포인트
export const GITHUB_API = {
  base: 'https://api.github.com',
  repos: (owner: string, repo: string) => `/repos/${owner}/${repo}`,
  issues: (owner: string, repo: string) => `/repos/${owner}/${repo}/issues`,
  pulls: (owner: string, repo: string) => `/repos/${owner}/${repo}/pulls`,
  milestones: (owner: string, repo: string) => `/repos/${owner}/${repo}/milestones`
}

// 프로젝트별 커스텀 메트릭스
export const PROJECT_METRICS = {
  'iwl-v5': {
    matrix: { total: 32, completed: 12 },
    phase: 'A Series',
    stage: { current: 4, total: 8 }
  },
  'ai-engine': {
    models: ['gpt-oss:20b', 'llama3.2', 'qwen2.5'],
    memory: { used: 15, total: 48 },
    apiStatus: 'healthy'
  },
  'calligraphy': {
    round: '1-2',
    progress: 70,
    storybook: { components: 12, stories: 24 },
    pipeline: { build: 'passing', test: 'passing', deploy: 'pending' }
  }
}