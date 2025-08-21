"""
PM AI Orchestrator
PM AI가 모든 작업을 관리하고 CLI들에게 업무를 분배하는 핵심 모듈
"""

import os
import asyncio
import json
import subprocess
from typing import Dict, List, Optional, Any
from datetime import datetime
from anthropic import Anthropic
from github import Github
from dotenv import load_dotenv
import re

load_dotenv()

class CLIManager:
    """tmux를 통한 CLI 관리"""
    
    def __init__(self):
        self.cli_sessions = {
            "claude": "claude-cli",
            "cursor": "cursor-cli", 
            "codex": "codex-cli",
            "gemini": "gemini-cli",
            "vscode": "vscode-cli"
        }
        self.active_sessions = {}
        
    def create_tmux_session(self, name: str) -> bool:
        """tmux 세션 생성"""
        try:
            cmd = f"tmux new-session -d -s {name}"
            subprocess.run(cmd, shell=True, check=True)
            self.active_sessions[name] = {
                "status": "active",
                "created_at": datetime.utcnow().isoformat()
            }
            return True
        except subprocess.CalledProcessError:
            return False
    
    def send_to_cli(self, session_name: str, message: str) -> bool:
        """CLI에 메시지 전송 (tmux send-keys 사용)"""
        try:
            # 메시지를 tmux 세션에 전송
            escaped_message = message.replace('"', '\\"').replace('\n', ' ')
            cmd = f'tmux send-keys -t {session_name} "{escaped_message}" Enter'
            subprocess.run(cmd, shell=True, check=True)
            return True
        except subprocess.CalledProcessError:
            return False
    
    def push_issue_to_cli(self, cli_name: str, issue_number: int, repo_name: str) -> bool:
        """특정 CLI에 이슈 푸시"""
        message = f"📋 새로운 작업이 할당되었습니다: Issue #{issue_number} - {repo_name}"
        detail_message = f"gh issue view {issue_number} -R {repo_name}"
        
        session_name = self.cli_sessions.get(cli_name)
        if not session_name:
            return False
            
        # 알림 메시지 전송
        self.send_to_cli(session_name, message)
        # GitHub CLI 명령어 전송
        self.send_to_cli(session_name, detail_message)
        
        return True
    
    def broadcast_to_all_clis(self, message: str):
        """모든 CLI에 메시지 브로드캐스트"""
        for cli_name, session_name in self.cli_sessions.items():
            self.send_to_cli(session_name, message)

class PMAgent:
    """PM AI 에이전트 - 모든 작업을 관리하고 지시"""
    
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.github = Github(os.getenv("GITHUB_TOKEN"))
        self.cli_manager = CLIManager()
        self.task_assignments = {}
        self.pending_decisions = []
        self.cli_detector = None
        self.task_bridge = None
        self._init_cli_detector()
        self._init_task_bridge()
    
    def _init_cli_detector(self):
        """CLI 감지기 초기화"""
        try:
            import sys
            sys.path.append('/Users/m4_macbook/ai-orchestra-dashboard/scripts')
            from cli_detector import CLIDetector
            self.cli_detector = CLIDetector()
        except Exception as e:
            print(f"Failed to initialize CLI detector: {e}")
    
    def _init_task_bridge(self):
        """파일 브릿지 초기화"""
        try:
            import sys
            sys.path.append('/Users/m4_macbook/ai-orchestra-dashboard/scripts')
            from task_file_bridge import TaskFileBridge
            self.task_bridge = TaskFileBridge()
        except Exception as e:
            print(f"Failed to initialize task bridge: {e}")
    
    def detect_available_clis(self) -> Dict:
        """사용 가능한 CLI 감지"""
        if self.cli_detector:
            return self.cli_detector.scan_and_map()
        return {"active_clis": {}, "summary": {"total_available": 0}}
        
    async def analyze_issue(self, issue_data: Dict) -> Dict:
        """이슈 분석 및 업무 분배 계획 수립"""
        
        # 실제 사용 가능한 CLI 감지
        cli_status = self.detect_available_clis()
        available_clis = []
        
        for cli_name, status in cli_status.get("active_clis", {}).items():
            if status["available"]:
                capabilities = ", ".join(status["capabilities"])
                available_clis.append(f"{cli_name.upper()} CLI - {capabilities}")
        
        if not available_clis:
            return {
                "error": "No available CLIs detected",
                "task_breakdown": [],
                "coordination_needed": False,
                "pr_required": False,
                "summary": "CLI를 찾을 수 없습니다"
            }
        
        prompt = f"""
        당신은 프로젝트 매니저 AI입니다. 다음 이슈를 분석하고 업무 분배 계획을 수립하세요.
        
        이슈 정보:
        - 번호: #{issue_data.get('number')}
        - 제목: {issue_data.get('title')}
        - 내용: {issue_data.get('body')}
        - 라벨: {issue_data.get('labels')}
        
        현재 사용 가능한 AI CLI (실시간 감지됨):
        {chr(10).join(f'{i+1}. {cli}' for i, cli in enumerate(available_clis))}
        
        다음 형식으로 응답하세요:
        {{
            "task_breakdown": [
                {{
                    "cli": "cli_name",
                    "task": "구체적인 작업 내용",
                    "priority": "high/medium/low",
                    "estimated_time": "예상 시간"
                }}
            ],
            "coordination_needed": true/false,
            "pr_required": true/false,
            "summary": "전체 작업 요약"
        }}
        """
        
        response = self.client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        try:
            # JSON 형식으로 파싱
            content = response.content[0].text
            # JSON 블록 추출 (``` 제거)
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
            
        return {
            "task_breakdown": [],
            "coordination_needed": False,
            "pr_required": False,
            "summary": "분석 실패"
        }
    
    async def assign_tasks(self, issue_number: int, repo_name: str, analysis: Dict) -> List[Dict]:
        """분석 결과를 바탕으로 실제 업무 할당"""
        
        assignments = []
        repo = self.github.get_repo(repo_name)
        issue = repo.get_issue(issue_number)
        
        # 이슈에 PM 분석 결과 코멘트 추가
        comment_body = f"""
## 🤖 PM AI 업무 분배 계획

### 📋 작업 요약
{analysis['summary']}

### 👥 업무 할당
"""
        
        for task in analysis['task_breakdown']:
            cli_name = task['cli']
            task_desc = task['task']
            priority = task['priority']
            
            comment_body += f"""
**{cli_name}**
- 작업: {task_desc}
- 우선순위: {priority}
- 예상 시간: {task['estimated_time']}
"""
            
            # CLI에 이슈 푸시 (파일 브릿지 사용)
            if self.task_bridge:
                task_data = {
                    "type": task['priority'],
                    "description": task_desc,
                    "issue_number": issue_number,
                    "repo_name": repo_name,
                    "priority": priority,
                    "github_url": f"https://github.com/{repo_name}/issues/{issue_number}"
                }
                task_id = self.task_bridge.create_task(cli_name.lower(), task_data)
                print(f"Task {task_id} created for {cli_name}")
            else:
                self.cli_manager.push_issue_to_cli(cli_name, issue_number, repo_name)
            
            # 할당 기록
            assignment = {
                "issue_number": issue_number,
                "cli": cli_name,
                "task": task_desc,
                "status": "assigned",
                "assigned_at": datetime.utcnow().isoformat()
            }
            assignments.append(assignment)
            self.task_assignments[f"{issue_number}_{cli_name}"] = assignment
        
        comment_body += f"""
### 🔄 조율 필요: {'예' if analysis['coordination_needed'] else '아니오'}
### 📝 PR 필요: {'예' if analysis['pr_required'] else '아니오'}

---
*PM AI가 자동으로 업무를 분배했습니다. 각 CLI는 할당된 작업을 확인하세요.*
"""
        
        # GitHub 이슈에 코멘트 추가
        issue.create_comment(comment_body)
        
        return assignments
    
    async def monitor_progress(self, issue_number: int, repo_name: str) -> Dict:
        """이슈 진행 상황 모니터링"""
        
        repo = self.github.get_repo(repo_name)
        issue = repo.get_issue(issue_number)
        
        # 이슈 코멘트 확인
        comments = issue.get_comments()
        
        progress = {
            "issue_number": issue_number,
            "total_comments": comments.totalCount,
            "cli_reports": [],
            "status": "in_progress"
        }
        
        # CLI 완료 보고 확인
        for comment in comments:
            if "완료 보고" in comment.body or "작업 완료" in comment.body:
                cli_match = re.search(r'\[(.+?)\]', comment.body)
                if cli_match:
                    progress["cli_reports"].append({
                        "cli": cli_match.group(1),
                        "report": comment.body,
                        "time": comment.created_at.isoformat()
                    })
        
        # 모든 CLI가 완료 보고를 했는지 확인
        assigned_clis = [t['cli'] for t in self.task_assignments.values() 
                        if t['issue_number'] == issue_number]
        reported_clis = [r['cli'] for r in progress["cli_reports"]]
        
        if set(assigned_clis).issubset(set(reported_clis)):
            progress["status"] = "ready_for_review"
            
        return progress
    
    async def make_decision(self, decision_request: Dict) -> Dict:
        """대시보드를 통한 의사결정 처리"""
        
        decision_type = decision_request.get("type")
        
        if decision_type == "approve_completion":
            # 작업 완료 승인
            return await self.approve_task_completion(decision_request)
            
        elif decision_type == "request_revision":
            # 수정 요청
            return await self.request_revision(decision_request)
            
        elif decision_type == "initiate_collaboration":
            # 협업 시작
            return await self.initiate_collaboration(decision_request)
            
        return {"status": "unknown_decision_type"}
    
    async def approve_task_completion(self, request: Dict) -> Dict:
        """작업 완료 승인"""
        
        issue_number = request.get("issue_number")
        repo_name = request.get("repo_name")
        
        repo = self.github.get_repo(repo_name)
        issue = repo.get_issue(issue_number)
        
        # 완료 코멘트 추가
        comment = """
## ✅ PM AI 작업 완료 확인

모든 할당된 작업이 성공적으로 완료되었습니다.
이슈를 종료합니다.

---
*대시보드를 통해 승인되었습니다.*
"""
        issue.create_comment(comment)
        
        # 이슈 종료
        issue.edit(state="closed")
        
        return {"status": "completed", "issue_number": issue_number}
    
    async def request_revision(self, request: Dict) -> Dict:
        """수정 요청"""
        
        issue_number = request.get("issue_number")
        repo_name = request.get("repo_name")
        cli_name = request.get("cli")
        revision_details = request.get("details")
        
        # 특정 CLI에 수정 요청 전송
        message = f"🔄 수정 요청: Issue #{issue_number} - {revision_details}"
        self.cli_manager.push_issue_to_cli(cli_name, issue_number, repo_name)
        
        # GitHub 이슈에 코멘트
        repo = self.github.get_repo(repo_name)
        issue = repo.get_issue(issue_number)
        
        comment = f"""
## 🔄 PM AI 수정 요청

**대상:** {cli_name}
**내용:** {revision_details}

수정 후 다시 보고해주세요.

---
*대시보드를 통해 요청되었습니다.*
"""
        issue.create_comment(comment)
        
        return {"status": "revision_requested", "cli": cli_name}
    
    async def initiate_collaboration(self, request: Dict) -> Dict:
        """협업 워크플로우 시작"""
        
        topic = request.get("topic")
        template = request.get("template", "default")
        participants = request.get("participants", [])
        
        # PR 생성
        repo_name = request.get("repo_name")
        repo = self.github.get_repo(repo_name)
        
        # 새 브랜치 생성
        branch_name = f"collab_{topic.lower().replace(' ', '_')}_{datetime.utcnow().strftime('%Y%m%d')}"
        
        # PR 본문 템플릿
        pr_body = f"""
## 🤝 협업 작업: {topic}

### 참여자
{', '.join(participants)}

### 템플릿
{template}

### 챕터별 의견 수렴

#### 1. 개요 및 목적
- [ ] Cursor CLI 의견
- [ ] Gemini CLI 의견
- [ ] PM 종합

#### 2. 기술적 구현
- [ ] Codex CLI 의견
- [ ] VSCode Claude 의견
- [ ] PM 종합

#### 3. 사용자 경험
- [ ] Gemini CLI 의견
- [ ] Cursor CLI 의견
- [ ] PM 종합

#### 4. 테스트 및 배포
- [ ] Codex CLI 의견
- [ ] Claude CLI 의견
- [ ] PM 종합

---
각 CLI는 할당된 챕터에 대해 의견을 제시해주세요.
PM AI가 종합하여 최종 문서를 작성합니다.
"""
        
        # 모든 CLI에 협업 요청 브로드캐스트
        self.cli_manager.broadcast_to_all_clis(
            f"🤝 협업 요청: {topic} - PR을 확인하고 의견을 제시해주세요"
        )
        
        return {
            "status": "collaboration_initiated",
            "branch": branch_name,
            "participants": participants
        }

class ChapterTemplateManager:
    """챕터별 의견 수렴 템플릿 관리"""
    
    def __init__(self):
        self.templates = {
            "feature_planning": {
                "name": "기능 기획",
                "chapters": [
                    {"title": "요구사항 분석", "assignees": ["cursor", "gemini"]},
                    {"title": "기술 스택 선정", "assignees": ["codex", "vscode"]},
                    {"title": "UI/UX 설계", "assignees": ["gemini", "vscode"]},
                    {"title": "API 설계", "assignees": ["codex", "cursor"]},
                    {"title": "테스트 계획", "assignees": ["claude", "codex"]}
                ]
            },
            "bug_fix": {
                "name": "버그 수정",
                "chapters": [
                    {"title": "문제 분석", "assignees": ["codex", "claude"]},
                    {"title": "원인 파악", "assignees": ["codex", "vscode"]},
                    {"title": "해결 방안", "assignees": ["all"]},
                    {"title": "테스트", "assignees": ["claude", "cursor"]}
                ]
            },
            "documentation": {
                "name": "문서 작성",
                "chapters": [
                    {"title": "개요", "assignees": ["cursor", "gemini"]},
                    {"title": "상세 설명", "assignees": ["all"]},
                    {"title": "예제 코드", "assignees": ["codex", "vscode"]},
                    {"title": "FAQ", "assignees": ["gemini", "claude"]}
                ]
            }
        }
    
    async def gather_opinions(self, template_name: str, chapter_index: int) -> List[Dict]:
        """챕터별 의견 수집"""
        
        template = self.templates.get(template_name)
        if not template:
            return []
            
        chapter = template["chapters"][chapter_index]
        opinions = []
        
        # 할당된 CLI들에게 의견 요청
        for assignee in chapter["assignees"]:
            if assignee == "all":
                # 모든 CLI에게 요청
                pass
            else:
                # 특정 CLI에게 요청
                opinion = {
                    "cli": assignee,
                    "chapter": chapter["title"],
                    "status": "requested",
                    "requested_at": datetime.utcnow().isoformat()
                }
                opinions.append(opinion)
        
        return opinions
    
    async def synthesize_chapter(self, opinions: List[Dict]) -> str:
        """의견 종합하여 챕터 작성"""
        
        # PM AI가 의견들을 종합
        synthesis_prompt = f"""
        다음 의견들을 종합하여 일관성 있는 챕터를 작성하세요:
        
        {json.dumps(opinions, indent=2, ensure_ascii=False)}
        
        최종 문서는 전문적이고 일관성 있게 작성해주세요.
        """
        
        # Claude API를 통해 종합
        # ... 구현
        
        return "종합된 챕터 내용"

# Singleton instances
pm_agent = PMAgent()
template_manager = ChapterTemplateManager()