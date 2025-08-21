#!/usr/bin/env python3
"""
CLI Monitor
각 CLI에서 실행하여 작업을 모니터링하고 수행
"""

import os
import sys
import json
import time
import argparse
from pathlib import Path
from datetime import datetime

class CLIMonitor:
    """CLI 작업 모니터"""
    
    def __init__(self, cli_name: str):
        self.cli_name = cli_name
        self.base_dir = Path.home() / ".ai-orchestra"
        self.tasks_dir = self.base_dir / "tasks" / cli_name
        self.results_dir = self.base_dir / "results" / cli_name
        self.status_dir = self.base_dir / "status" / cli_name
        
        print(f"🤖 {cli_name.upper()} Monitor Started")
        print(f"📁 Monitoring: {self.tasks_dir}")
        print("-" * 60)
    
    def update_status(self, status: str, details: str = ""):
        """상태 업데이트"""
        status_file = self.status_dir / "current.json"
        status_data = {
            "cli": self.cli_name,
            "status": status,
            "details": details,
            "updated_at": datetime.now().isoformat()
        }
        
        with open(status_file, 'w') as f:
            json.dump(status_data, f, indent=2)
    
    def process_task(self, task_file: Path) -> bool:
        """작업 처리"""
        try:
            # 작업 읽기
            with open(task_file) as f:
                task = json.load(f)
            
            print(f"\n📋 New Task Received!")
            print(f"   ID: {task['id']}")
            print(f"   Type: {task.get('type', 'general')}")
            print(f"   Description: {task.get('description', 'No description')}")
            print(f"   Priority: {task.get('priority', 'normal')}")
            print(f"   Issue: #{task.get('issue_number', 'N/A')}")
            
            # 상태 업데이트
            self.update_status("working", f"Task {task['id']}")
            
            # 여기서 실제 작업 수행
            print(f"\n⚙️  Processing task...")
            print(f"   [시뮬레이션] {self.cli_name}가 작업을 수행 중입니다...")
            time.sleep(3)  # 작업 시뮬레이션
            
            # 결과 생성
            result = {
                "task_id": task['id'],
                "cli": self.cli_name,
                "completed_at": datetime.now().isoformat(),
                "result": {
                    "status": "success",
                    "message": f"Task completed by {self.cli_name}",
                    "details": f"Successfully processed: {task.get('description', '')}",
                    "output": "Task output would go here..."
                }
            }
            
            # 결과 저장
            result_file = self.results_dir / f"{task['id']}.json"
            with open(result_file, 'w') as f:
                json.dump(result, f, indent=2)
            
            print(f"✅ Task completed! Result saved to: {result_file}")
            
            # 작업 파일 삭제
            task_file.unlink()
            
            # 상태 업데이트
            self.update_status("idle", f"Completed {task['id']}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error processing task: {e}")
            self.update_status("error", str(e))
            return False
    
    def monitor(self, interval: int = 5):
        """작업 모니터링 시작"""
        print(f"\n👀 Monitoring for tasks (checking every {interval} seconds)...")
        print("Press Ctrl+C to stop\n")
        
        self.update_status("idle", "Monitoring")
        
        try:
            while True:
                # 새 작업 확인
                if self.tasks_dir.exists():
                    task_files = list(self.tasks_dir.glob("*.json"))
                    
                    if task_files:
                        # 첫 번째 작업 처리
                        self.process_task(task_files[0])
                    else:
                        # 대기 상태 표시
                        print(".", end="", flush=True)
                
                # 주기적으로 상태 업데이트 (살아있음을 알림)
                if not task_files:
                    self.update_status("idle", "Monitoring")
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n\n👋 Monitor stopped")
            self.update_status("offline", "Monitor stopped")

def main():
    parser = argparse.ArgumentParser(description='CLI Task Monitor')
    parser.add_argument('--cli', required=True, 
                       choices=['claude', 'cursor', 'codex', 'gemini', 'vscode'],
                       help='CLI name to monitor')
    parser.add_argument('--interval', type=int, default=5,
                       help='Check interval in seconds (default: 5)')
    
    args = parser.parse_args()
    
    # 모니터 시작
    monitor = CLIMonitor(args.cli)
    monitor.monitor(args.interval)

if __name__ == "__main__":
    main()