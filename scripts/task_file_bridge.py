#!/usr/bin/env python3
"""
Task File Bridge
파일 시스템을 통한 CLI 통신 브릿지
각 CLI가 모니터링할 수 있는 작업 파일 생성
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

class TaskFileBridge:
    """파일 기반 CLI 통신 시스템"""
    
    def __init__(self):
        # 기본 디렉토리 설정
        self.base_dir = Path.home() / ".ai-orchestra"
        self.tasks_dir = self.base_dir / "tasks"
        self.results_dir = self.base_dir / "results"
        self.status_dir = self.base_dir / "status"
        
        # 디렉토리 생성
        self._setup_directories()
        
    def _setup_directories(self):
        """필요한 디렉토리 구조 생성"""
        cli_names = ["claude", "cursor", "codex", "gemini", "vscode"]
        
        for cli in cli_names:
            (self.tasks_dir / cli).mkdir(parents=True, exist_ok=True)
            (self.results_dir / cli).mkdir(parents=True, exist_ok=True)
            (self.status_dir / cli).mkdir(parents=True, exist_ok=True)
    
    def create_task(self, cli_name: str, task_data: Dict) -> str:
        """CLI를 위한 작업 파일 생성"""
        
        # 작업 ID 생성
        task_id = f"{int(time.time())}_{task_data.get('issue_number', 'manual')}"
        
        # 작업 데이터 구성
        task = {
            "id": task_id,
            "cli": cli_name,
            "created_at": datetime.now().isoformat(),
            "status": "pending",
            **task_data
        }
        
        # 작업 파일 저장
        task_file = self.tasks_dir / cli_name / f"{task_id}.json"
        with open(task_file, 'w') as f:
            json.dump(task, f, indent=2)
        
        print(f"✅ Task created for {cli_name}: {task_file}")
        
        # 상태 파일 생성
        self.update_cli_status(cli_name, "task_assigned", task_id)
        
        return task_id
    
    def update_cli_status(self, cli_name: str, status: str, details: str = ""):
        """CLI 상태 업데이트"""
        status_file = self.status_dir / cli_name / "current.json"
        
        status_data = {
            "cli": cli_name,
            "status": status,
            "details": details,
            "updated_at": datetime.now().isoformat()
        }
        
        with open(status_file, 'w') as f:
            json.dump(status_data, f, indent=2)
    
    def check_result(self, cli_name: str, task_id: str) -> Optional[Dict]:
        """작업 결과 확인"""
        result_file = self.results_dir / cli_name / f"{task_id}.json"
        
        if result_file.exists():
            with open(result_file) as f:
                return json.load(f)
        
        return None
    
    def get_cli_status(self, cli_name: str) -> Optional[Dict]:
        """CLI 현재 상태 확인"""
        status_file = self.status_dir / cli_name / "current.json"
        
        if status_file.exists():
            with open(status_file) as f:
                return json.load(f)
        
        return None
    
    def list_pending_tasks(self, cli_name: str) -> list:
        """특정 CLI의 대기 중인 작업 목록"""
        tasks_path = self.tasks_dir / cli_name
        pending_tasks = []
        
        if tasks_path.exists():
            for task_file in tasks_path.glob("*.json"):
                with open(task_file) as f:
                    task = json.load(f)
                    if task.get("status") == "pending":
                        pending_tasks.append(task)
        
        return pending_tasks
    
    def mark_task_completed(self, cli_name: str, task_id: str, result: Dict):
        """작업 완료 표시"""
        # 결과 파일 저장
        result_file = self.results_dir / cli_name / f"{task_id}.json"
        result_data = {
            "task_id": task_id,
            "cli": cli_name,
            "completed_at": datetime.now().isoformat(),
            "result": result
        }
        
        with open(result_file, 'w') as f:
            json.dump(result_data, f, indent=2)
        
        # 원본 작업 파일 삭제
        task_file = self.tasks_dir / cli_name / f"{task_id}.json"
        if task_file.exists():
            task_file.unlink()
        
        # 상태 업데이트
        self.update_cli_status(cli_name, "idle", f"Completed {task_id}")
        
        print(f"✅ Task {task_id} completed by {cli_name}")

def demo():
    """데모 및 테스트"""
    bridge = TaskFileBridge()
    
    print("=" * 60)
    print("Task File Bridge Demo")
    print("=" * 60)
    
    # 작업 생성 예시
    test_tasks = [
        {
            "cli": "claude",
            "data": {
                "type": "review",
                "description": "Review PR #42",
                "issue_number": 42,
                "priority": "high"
            }
        },
        {
            "cli": "cursor",
            "data": {
                "type": "architecture",
                "description": "Design authentication system",
                "issue_number": 41,
                "priority": "medium"
            }
        },
        {
            "cli": "vscode",
            "data": {
                "type": "frontend",
                "description": "Update UI components",
                "issue_number": 40,
                "priority": "low"
            }
        }
    ]
    
    print("\n📝 Creating tasks...")
    created_tasks = []
    for task in test_tasks:
        task_id = bridge.create_task(task["cli"], task["data"])
        created_tasks.append((task["cli"], task_id))
    
    print("\n📊 Checking CLI status...")
    for cli in ["claude", "cursor", "vscode"]:
        status = bridge.get_cli_status(cli)
        if status:
            print(f"{cli}: {status['status']} - {status['details']}")
    
    print("\n📋 Pending tasks...")
    for cli in ["claude", "cursor", "vscode"]:
        tasks = bridge.list_pending_tasks(cli)
        print(f"{cli}: {len(tasks)} pending tasks")
    
    print(f"\n✅ Setup complete!")
    print(f"📁 Task directory: {bridge.tasks_dir}")
    print(f"📁 Results directory: {bridge.results_dir}")
    print(f"📁 Status directory: {bridge.status_dir}")
    
    print("\n🔍 각 CLI에서 다음 명령으로 모니터링 시작:")
    print("python3 /Users/m4_macbook/ai-orchestra-dashboard/scripts/cli_monitor.py --cli claude")

if __name__ == "__main__":
    demo()