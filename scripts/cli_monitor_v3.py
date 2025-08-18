#!/usr/bin/env python3
"""
CLI Monitor V3 - 실제 CLI 자동 실행 기능 포함
PM이 할당한 작업을 실제 AI CLI에서 자동으로 수행
"""

import os
import sys
import json
import time
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

# 자동화 브릿지 임포트
sys.path.append('/Users/m4_macbook/ai-orchestra-dashboard/scripts')
from cli_automation_bridge import CLIAutomationBridge

class CLIMonitor:
    """CLI 작업 모니터 - 실제 CLI 제어 기능 포함"""
    
    def __init__(self, cli_name: str, auto_execute: bool = True):
        self.cli_name = cli_name
        self.auto_execute = auto_execute
        self.base_dir = Path.home() / ".ai-orchestra"
        self.tasks_dir = self.base_dir / "tasks" / cli_name
        self.results_dir = self.base_dir / "results" / cli_name
        self.status_dir = self.base_dir / "status" / cli_name
        
        # 자동화 브릿지 초기화
        self.automation = CLIAutomationBridge(cli_name) if auto_execute else None
        
        # 디렉토리 생성
        self.tasks_dir.mkdir(parents=True, exist_ok=True)
        self.results_dir.mkdir(parents=True, exist_ok=True)
        self.status_dir.mkdir(parents=True, exist_ok=True)
        
        # 시작 알림
        mode = "AUTO-EXECUTE" if auto_execute else "MONITOR-ONLY"
        self.terminal_alert(f"🤖 {cli_name.upper()} Monitor", f"Mode: {mode}")
        print(f"🤖 {cli_name.upper()} Monitor Started")
        print(f"📁 Monitoring: {self.tasks_dir}")
        print(f"🔧 Mode: {mode}")
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
                f'display notification "{message}" with title "{title}" sound name "Hero"'
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
            
            task_type = task_data.get('type', 'general')
            
            # PING 타입 처리
            if task_type == 'ping':
                self.terminal_alert(
                    f"🏓 PING from Dashboard",
                    task_data.get('description', 'Connection test')
                )
                
                # 화면 깜빡임
                for _ in range(2):
                    print("\033[?5h", end="", flush=True)
                    time.sleep(0.1)
                    print("\033[?5l", end="", flush=True)
                    time.sleep(0.1)
                
                result = {
                    "task_id": task_data.get('id'),
                    "cli": self.cli_name,
                    "type": "ping",
                    "status": "completed",
                    "message": "Ping acknowledged"
                }
                
            # 실제 작업 처리
            else:
                # 작업 알림
                self.terminal_alert(
                    f"📋 NEW TASK ASSIGNED",
                    f"Type: {task_type} | Priority: {task_data.get('priority', 'normal')}"
                )
                
                print(f"\n{'='*60}")
                print(f"📋 작업 상세:")
                print(f"  ID: {task_data.get('id')}")
                print(f"  Type: {task_type}")
                print(f"  Issue: #{task_data.get('issue_number', 'N/A')}")
                print(f"  Description: {task_data.get('description', 'No description')}")
                print(f"  Priority: {task_data.get('priority', 'normal')}")
                print(f"{'='*60}\n")
                
                # 상태 업데이트
                self.update_status("working", f"Task {task_data.get('id')}")
                
                # 자동 실행 모드인 경우 실제 CLI에 작업 전송
                if self.auto_execute and self.automation:
                    print(f"🚀 {self.cli_name.upper()} CLI에 작업을 전송합니다...")
                    
                    # 작업 메시지 생성 (영어로)
                    if task_data.get('issue_number'):
                        prompt = f"""Please handle this GitHub Issue:

Issue #{task_data.get('issue_number')}
Title: {task_data.get('title', '')}
Description: {task_data.get('description', '')}

Please analyze this issue and provide a solution."""
                    else:
                        prompt = f"""Task assigned from PM Dashboard:

Task: {task_data.get('description', '')}
Priority: {task_data.get('priority', 'normal')}

Please work on this task."""
                    
                    # 실제 CLI에 전송
                    success = self.automation.execute_task({
                        'cli': self.cli_name,
                        'type': task_type,
                        'description': prompt,
                        'issue_number': task_data.get('issue_number')
                    })
                    
                    if success:
                        print(f"✅ {self.cli_name.upper()} CLI가 작업을 시작했습니다!")
                        self.terminal_alert(
                            "🎯 TASK SENT TO CLI",
                            f"{self.cli_name.upper()} is now working on it"
                        )
                    else:
                        print(f"⚠️ CLI 전송 실패. 수동으로 처리가 필요합니다.")
                else:
                    print("📝 모니터 전용 모드 - 작업이 기록되었습니다.")
                    time.sleep(2)  # 시뮬레이션
                
                # 결과 생성
                result = {
                    "task_id": task_data.get('id'),
                    "cli": self.cli_name,
                    "type": task_type,
                    "completed_at": datetime.now().isoformat(),
                    "status": "in_progress" if self.auto_execute else "logged",
                    "message": f"Task sent to {self.cli_name}" if self.auto_execute else "Task logged"
                }
            
            # 결과 저장
            result_file = self.results_dir / f"{task_data.get('id')}.json"
            with open(result_file, 'w') as f:
                json.dump(result, f, indent=2)
            
            print(f"📝 Result saved to: {result_file}")
            
            # 작업 파일 삭제
            task_file.unlink()
            
            # 상태 업데이트
            self.update_status("idle", "Ready for next task")
            
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
                        dot_count = 0
                    else:
                        # 대기 상태 표시
                        if dot_count < 12:
                            print(".", end="", flush=True)
                            dot_count += 1
                        else:
                            print("\r" + " " * 12 + "\r", end="", flush=True)
                            dot_count = 0
                
                # 상태 업데이트
                self.update_status("idle", "Monitoring")
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n\n👋 Monitor stopped")
            self.terminal_alert("MONITOR STOPPED", f"{self.cli_name.upper()} monitor shutdown")
            self.update_status("offline", "Monitor stopped")

def main():
    parser = argparse.ArgumentParser(description='CLI Task Monitor V3 with Auto-Execute')
    parser.add_argument('--cli', required=True, 
                       choices=['claude', 'cursor', 'codex', 'gemini', 'vscode'],
                       help='CLI name to monitor')
    parser.add_argument('--interval', type=int, default=5,
                       help='Check interval in seconds (default: 5)')
    parser.add_argument('--no-auto', action='store_true',
                       help='Disable auto-execution (monitor only mode)')
    
    args = parser.parse_args()
    
    # 모니터 시작
    monitor = CLIMonitor(args.cli, auto_execute=not args.no_auto)
    monitor.monitor(args.interval)

if __name__ == "__main__":
    main()