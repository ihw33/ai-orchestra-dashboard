# 🚀 Claude Task Master 설치 가이드

## 1. 설치

### npm으로 설치
```bash
npm install -g task-master-ai
```

또는 GitHub에서 직접
```bash
git clone https://github.com/eyaltoledano/claude-task-master.git
cd claude-task-master
npm install
```

## 2. MCP 설정

### Claude Desktop 설정 (~/.claude/mcp.json)
```json
{
  "servers": {
    "task-master": {
      "command": "npx",
      "args": ["task-master-ai"],
      "env": {
        "CLAUDE_API_KEY": "your-key",
        "GITHUB_TOKEN": "your-github-token"
      }
    },
    "github": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "your-github-token"
      }
    }
  }
}
```

## 3. 우리 프로젝트 워크플로우

### 3.1 PRD → Task 변환
```bash
# PRD 파일로 Task 생성
tm plan --input round3_prd.md --output tasks.json

# 또는 대화형으로
tm chat
> "Round 3: PL Bot, Allow 알림, WebSocket 구현"
```

### 3.2 GitHub 연동
```bash
# Task를 GitHub Issue로 변환
tm sync github --repo ihw33/ai-orchestra-dashboard \
  --project "AI Orchestra Board" \
  --column "To Do"
```

### 3.3 자동화 스크립트
```javascript
// sync_tasks_to_github.js
const { Octokit } = require('@octokit/rest');
const tasks = require('./tasks.json');

const octokit = new Octokit({
  auth: process.env.GITHUB_TOKEN
});

async function syncTasks() {
  for (const task of tasks) {
    // Issue 생성
    const issue = await octokit.issues.create({
      owner: 'ihw33',
      repo: 'ai-orchestra-dashboard',
      title: task.title,
      body: task.description,
      labels: ['round-3', task.type],
      assignees: [task.assignee]
    });
    
    // Projects 칸반에 추가
    await octokit.graphql(`
      mutation {
        addProjectV2ItemById(input: {
          projectId: "PVT_xxx",
          contentId: "${issue.data.node_id}"
        }) {
          item { id }
        }
      }
    `);
  }
}
```

## 4. 실제 사용 예시

### Round 3 작업 자동화
```bash
# 1. PRD 작성
cat > round3.md << EOF
Round 3: Intelligence Layer
- PL Bot으로 팀원 상태 자동 추적
- Allow 요청 즉시 알림 시스템
- 실시간 WebSocket 대시보드
EOF

# 2. Task 생성
tm plan --input round3.md

# 3. GitHub 동기화
tm sync github --auto-assign

# 4. 상태 확인
tm status
```

## 5. 장점

### Before (수동)
- PM Claude가 Issue 하나씩 생성
- 수동으로 칸반 보드 업데이트
- 팀원 배정 수동

### After (자동)
- PRD 입력 → 자동 Issue 생성
- 칸반 보드 자동 업데이트
- AI별 역할에 따라 자동 배정

## 6. 우리 프로젝트 커스터마이징

### 팀원 매핑
```json
{
  "assignee_mapping": {
    "frontend": "Claude-VSCode",
    "backend": "Codex",
    "data": "Gemini",
    "pm": "PM-Claude"
  }
}
```

### 라벨 자동화
```json
{
  "label_rules": {
    "UI": ["frontend", "p2"],
    "API": ["backend", "p1"],
    "Bot": ["automation", "p0"]
  }
}
```

## 7. 통합 테스트

```bash
# 테스트 PRD
echo "테스트: 간단한 TODO 앱 만들기" | tm plan

# 결과 확인
tm list

# GitHub 미리보기 (dry-run)
tm sync github --dry-run
```

---

**다음 단계**:
1. Task Master 설치
2. GitHub 토큰 설정
3. 테스트 PRD로 시험
4. Round 3 작업에 적용