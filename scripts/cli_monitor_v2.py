#!/usr/bin/env python3
"""
CLI Monitor V2 - with Terminal Notifications
각 CLI에서 실행하여 작업을 모니터링하고 수행
"""

import os
import sys
import json
import time
import argparse
import subprocess
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
        
        # 디렉토리 생성
        self.tasks_dir.mkdir(parents=True, exist_ok=True)
        self.results_dir.mkdir(parents=True, exist_ok=True)
        self.status_dir.mkdir(parents=True, exist_ok=True)
        
        # 시작 알림
        self.terminal_alert("MONITOR STARTED", f"🤖 {cli_name.upper()} Monitor is now active")
        print(f"🤖 {cli_name.upper()} Monitor Started")
        print(f"📁 Monitoring: {self.tasks_dir}")
        print("-" * 60)
    
    def terminal_alert(self, title: str, message: str):
        """터미널에 시각적 알림 표시"""
        # 색상 있는 박스 표시
        print(f"\n\033[1;42m{'='*60}\033[0m")
        print(f"\033[1;33m{title.center(60)}\033[0m")
        print(f"\033[1;36m{message.center(60)}\033[0m")
        print(f"\033[1;42m{'='*60}\033[0m\n")
        
        # 벨 소리
        print("\a", end="", flush=True)
        
        # macOS 알림
        try:
            subprocess.run([
                'osascript', '-e',
                f'display notification "{message}" with title "{title}" sound name "Ping"'
            ], capture_output=True)
        except:
            pass
    
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
                task_data = json.load(f)
            
            # PING 타입 특별 처리
            if task_data.get('type') == 'ping':
                # 큰 시각적 알림
                self.terminal_alert(
                    f"🏓 PING from Dashboard",
                    task_data.get('description', 'Connection test')
                )
                
                # 화면 깜빡임 효과
                for _ in range(2):
                    print("\033[?5h", end="", flush=True)  # 반전
                    time.sleep(0.1)
                    print("\033[?5l", end="", flush=True)  # 정상
                    time.sleep(0.1)
                
                # 결과 저장
                result = {
                    "task_id": task_data.get('id'),
                    "cli": self.cli_name,
                    "type": "ping",
                    "status": "completed",
                    "message": "Ping received and acknowledged",
                    "timestamp": datetime.now().isoformat()
                }
                
                result_file = self.results_dir / f"{task_data.get('id')}.json"
                with open(result_file, 'w') as f:
                    json.dump(result, f, indent=2)
                
                print(f"✅ Ping acknowledged!")
                
            else:
                # 일반 작업 처리
                print(f"\n📋 New Task Received!")
                print(f"   ID: {task_data['id']}")
                print(f"   Type: {task_data.get('type', 'general')}")
                print(f"   Description: {task_data.get('description', 'No description')}")
                
                self.terminal_alert(
                    "NEW TASK",
                    f"{task_data.get('description', 'Task received')}[:50]"
                )
                
                # 상태 업데이트
                self.update_status("working", f"Task {task_data['id']}")
                
                # 작업 시뮬레이션
                print(f"\n⚙️  Processing task...")
                time.sleep(2)
                
                # 결과 생성
                result = {
                    "task_id": task_data['id'],
                    "cli": self.cli_name,
                    "completed_at": datetime.now().isoformat(),
                    "result": {
                        "status": "success",
                        "message": f"Task completed by {self.cli_name}"
                    }
                }
                
                # 결과 저장
                result_file = self.results_dir / f"{task_data['id']}.json"
                with open(result_file, 'w') as f:
                    json.dump(result, f, indent=2)
                
                print(f"✅ Task completed!")
            
            # 작업 파일 삭제
            task_file.unlink()
            
            # 상태 업데이트
            self.update_status("idle", "Ready")
            
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
        
        dot_count = 0
        try:
            while True:
                # 새 작업 확인
                if self.tasks_dir.exists():
                    task_files = list(self.tasks_dir.glob("*.json"))
                    
                    if task_files:
                        # 첫 번째 작업 처리
                        self.process_task(task_files[0])
                        dot_count = 0  # 점 카운터 리셋
                    else:
                        # 대기 상태 표시 (점이 너무 많아지지 않도록)
                        if dot_count < 12:
                            print(".", end="", flush=True)
                            dot_count += 1
                        else:
                            print("\r" + " " * 12 + "\r", end="", flush=True)  # 점 지우기
                            dot_count = 0
                
                # 주기적으로 상태 업데이트
                self.update_status("idle", "Monitoring")
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n\n👋 Monitor stopped")
            self.terminal_alert("MONITOR STOPPED", f"{self.cli_name.upper()} monitor shutdown")
            self.update_status("offline", "Monitor stopped")

def main():
    parser = argparse.ArgumentParser(description='CLI Task Monitor V2')
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