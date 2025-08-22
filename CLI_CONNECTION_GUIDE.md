# CLI 실제 연결 방법

## 1. Claude Desktop 연결
```bash
# MCP (Model Context Protocol) 서버 사용
# Claude Desktop이 지원하는 공식 방법
claude mcp add file-server /path/to/project
claude mcp add github-server
```

## 2. Cursor 연결
```bash
# Cursor API 또는 Extension 필요
# 현재 공식 API 없음 - 대안:
# - 파일 시스템을 통한 통신
# - 공유 폴더에 작업 파일 생성
echo "task: Fix bug in auth.js" > ~/.cursor-tasks/task-001.md
```

## 3. Codex (OpenAI) 연결
```python
# OpenAI API 직접 호출
import openai
openai.api_key = "sk-..."

response = openai.Completion.create(
    engine="code-davinci-002",
    prompt="Fix the following code:",
    max_tokens=150
)
```

## 4. VSCode 연결
```bash
# VSCode Server 또는 Remote API
# code CLI 명령어 사용
code --goto file.js:10:5
code --diff file1.js file2.js
code --add folder/to/workspace
```

## 5. 실제 통신 방법들

### A. 파일 기반 통신 (가장 간단)
```python
# 1. 작업 파일 생성
task_file = f"/tmp/ai-tasks/{cli_name}/task-{id}.json"
with open(task_file, 'w') as f:
    json.dump({
        "task": "implement feature X",
        "issue": 42,
        "priority": "high"
    }, f)

# 2. CLI가 파일 모니터링
# 3. 완료 시 결과 파일 생성
result_file = f"/tmp/ai-tasks/{cli_name}/result-{id}.json"
```

### B. HTTP API 서버 (각 CLI에 로컬 서버)
```python
# 각 CLI에서 실행
from flask import Flask, request
app = Flask(__name__)

@app.route('/task', methods=['POST'])
def receive_task():
    task = request.json
    # CLI에 작업 표시
    return {"status": "received"}

app.run(port=5001)  # Claude
app.run(port=5002)  # Cursor
```

### C. WebSocket 실시간 연결
```javascript
// CLI Extension에서 WebSocket 서버 실행
const ws = new WebSocket('ws://localhost:8080');

ws.on('message', (data) => {
  const task = JSON.parse(data);
  // 에디터에 작업 표시
  vscode.window.showInformationMessage(`New task: ${task.description}`);
});
```

### D. GitHub Issues 기반 (간접 통신)
```python
# PM이 이슈에 코멘트 작성
issue.create_comment(f"""
@claude-cli Please implement authentication
@cursor-cli Please review the architecture
@codex-cli Please create API endpoints
""")

# 각 CLI가 GitHub를 폴링하여 자신의 멘션 확인
```

## 🚀 즉시 구현 가능한 방법

### 1단계: 파일 기반 통신 시스템
```bash
# 디렉토리 구조
/Users/m4_macbook/.ai-orchestra/
  ├── tasks/
  │   ├── claude/
  │   ├── cursor/
  │   └── codex/
  ├── results/
  └── status/
```

### 2단계: 각 CLI에 모니터링 스크립트
```python
# monitor.py - 각 CLI에서 실행
import time
import json
import os

task_dir = f"/Users/m4_macbook/.ai-orchestra/tasks/{CLI_NAME}/"

while True:
    for file in os.listdir(task_dir):
        if file.endswith('.json'):
            with open(f"{task_dir}/{file}") as f:
                task = json.load(f)
                print(f"New task: {task['description']}")
                # 작업 수행...
                # 결과 저장...
                os.remove(f"{task_dir}/{file}")
    time.sleep(5)
```

## 📝 현실적인 구현 순서

1. **파일 기반 통신** - 가장 간단, 모든 CLI 지원
2. **GitHub Issue 댓글** - 이미 GitHub API 있음
3. **각 CLI별 Extension** - 시간 필요
4. **WebSocket/HTTP API** - 각 CLI에 서버 필요