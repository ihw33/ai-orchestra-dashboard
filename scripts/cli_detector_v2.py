#!/usr/bin/env python3
"""
CLI Detector V2 - 개선된 버전
실제 메인 프로세스만 감지하고, 연결된 모니터 상태 확인
"""

import subprocess
import json
import os
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path

class CLIDetectorV2:
    """개선된 CLI 감지기 - 실제 연결 가능한 것만"""
    
    def __init__(self):
        self.base_dir = Path.home() / ".ai-orchestra"
        self.status_dir = self.base_dir / "status"
        
        # 메인 프로세스만 감지하기 위한 필터
        self.main_process_patterns = {
            "claude": {
                "include": ["/Applications/Claude.app/Contents/MacOS/Claude"],
                "exclude": ["Helper", "Renderer", "GPU", "chrome", "electron"]
            },
            "cursor": {
                "include": ["Cursor.app/Contents/MacOS/Cursor", "cursor"],
                "exclude": ["Helper", "crashpad", "chrome"]
            },
            "vscode": {
                "include": ["Visual Studio Code.app/Contents/MacOS/Electron", "code"],
                "exclude": ["Helper", "crashpad", "chrome", "extensionHost"]
            },
            "codex": {
                "include": ["node /Users/m4_macbook/.npm-global/bin/codex", "codex-aarch64"],
                "exclude": ["grep", "ps"]
            },
            "gemini": {
                "include": ["node /Users/m4_macbook/.npm-global/bin/gemini", "bin/gEMINI"],
                "exclude": ["grep", "ps"]
            }
        }
    
    def get_main_processes_only(self) -> Dict[str, List[Dict]]:
        """메인 프로세스만 감지 (Helper, Renderer 제외)"""
        main_processes = {}
        
        try:
            result = subprocess.run(
                ["ps", "aux"],
                capture_output=True,
                text=True
            )
            
            for cli_name, patterns in self.main_process_patterns.items():
                found_processes = []
                
                for line in result.stdout.split('\n'):
                    # Include 패턴 확인
                    include_match = any(inc in line for inc in patterns["include"])
                    # Exclude 패턴 확인
                    exclude_match = any(exc in line for exc in patterns["exclude"])
                    
                    if include_match and not exclude_match:
                        parts = line.split(None, 10)
                        if len(parts) > 10:
                            pid = parts[1]
                            cmd = parts[10]
                            
                            # 중복 제거를 위해 이미 있는 PID는 스킵
                            if not any(p['pid'] == pid for p in found_processes):
                                found_processes.append({
                                    "pid": pid,
                                    "command": cmd[:100]  # 명령어 일부만
                                })
                
                if found_processes:
                    main_processes[cli_name] = found_processes
        
        except Exception as e:
            print(f"Error detecting main processes: {e}")
        
        return main_processes
    
    def get_connected_monitors(self) -> Dict[str, Dict]:
        """현재 연결된 CLI 모니터 확인"""
        connected_monitors = {}
        
        # status 디렉토리에서 각 CLI의 현재 상태 확인
        if self.status_dir.exists():
            for cli_dir in self.status_dir.iterdir():
                if cli_dir.is_dir():
                    cli_name = cli_dir.name
                    status_file = cli_dir / "current.json"
                    
                    if status_file.exists():
                        try:
                            with open(status_file) as f:
                                status = json.load(f)
                                
                                # 최근 5분 이내 업데이트된 것만 "연결됨"으로 표시
                                updated_at = datetime.fromisoformat(status['updated_at'])
                                time_diff = datetime.now() - updated_at
                                
                                if time_diff.total_seconds() < 300:  # 5분
                                    connected_monitors[cli_name] = {
                                        "status": status['status'],
                                        "last_update": status['updated_at'],
                                        "details": status.get('details', ''),
                                        "connected": True
                                    }
                                else:
                                    connected_monitors[cli_name] = {
                                        "status": "offline",
                                        "last_update": status['updated_at'],
                                        "connected": False
                                    }
                        except Exception as e:
                            print(f"Error reading status for {cli_name}: {e}")
        
        return connected_monitors
    
    def get_pending_tasks(self) -> Dict[str, List]:
        """각 CLI의 대기 중인 작업 확인"""
        pending_tasks = {}
        tasks_dir = self.base_dir / "tasks"
        
        if tasks_dir.exists():
            for cli_dir in tasks_dir.iterdir():
                if cli_dir.is_dir():
                    cli_name = cli_dir.name
                    tasks = list(cli_dir.glob("*.json"))
                    if tasks:
                        pending_tasks[cli_name] = [t.name for t in tasks]
        
        return pending_tasks
    
    def get_completed_tasks(self) -> Dict[str, List]:
        """각 CLI의 완료된 작업 확인"""
        completed_tasks = {}
        results_dir = self.base_dir / "results"
        
        if results_dir.exists():
            for cli_dir in results_dir.iterdir():
                if cli_dir.is_dir():
                    cli_name = cli_dir.name
                    results = list(cli_dir.glob("*.json"))
                    if results:
                        completed_tasks[cli_name] = [r.name for r in results]
        
        return completed_tasks
    
    def get_full_status(self) -> Dict:
        """전체 상태 종합"""
        main_processes = self.get_main_processes_only()
        connected_monitors = self.get_connected_monitors()
        pending_tasks = self.get_pending_tasks()
        completed_tasks = self.get_completed_tasks()
        
        # 종합 상태
        cli_status = {}
        
        for cli_name in ["claude", "cursor", "codex", "gemini", "vscode"]:
            status = {
                "name": cli_name,
                "main_process": False,
                "process_count": 0,
                "monitor_connected": False,
                "monitor_status": "offline",
                "pending_tasks": 0,
                "completed_tasks": 0,
                "available": False  # 실제 사용 가능 여부
            }
            
            # 메인 프로세스 확인
            if cli_name in main_processes:
                status["main_process"] = True
                status["process_count"] = len(main_processes[cli_name])
                status["processes"] = main_processes[cli_name]
            
            # 모니터 연결 확인
            if cli_name in connected_monitors:
                monitor = connected_monitors[cli_name]
                status["monitor_connected"] = monitor["connected"]
                status["monitor_status"] = monitor["status"]
                status["last_monitor_update"] = monitor["last_update"]
            
            # 작업 확인
            if cli_name in pending_tasks:
                status["pending_tasks"] = len(pending_tasks[cli_name])
            
            if cli_name in completed_tasks:
                status["completed_tasks"] = len(completed_tasks[cli_name])
            
            # 실제 사용 가능 = 모니터가 연결되어 있는 경우
            status["available"] = status["monitor_connected"]
            
            cli_status[cli_name] = status
        
        return {
            "timestamp": datetime.now().isoformat(),
            "cli_status": cli_status,
            "summary": {
                "total_apps_running": len(main_processes),
                "total_monitors_connected": sum(1 for c in cli_status.values() if c["monitor_connected"]),
                "total_available": sum(1 for c in cli_status.values() if c["available"]),
                "total_pending_tasks": sum(c["pending_tasks"] for c in cli_status.values()),
                "total_completed_tasks": sum(c["completed_tasks"] for c in cli_status.values())
            }
        }

def main():
    """테스트 및 리포트"""
    detector = CLIDetectorV2()
    status = detector.get_full_status()
    
    print("=" * 70)
    print("CLI Status Report V2 - 실제 연결 상태")
    print("=" * 70)
    print(f"Timestamp: {status['timestamp']}\n")
    
    print("📊 Summary:")
    print(f"  Apps Running: {status['summary']['total_apps_running']}")
    print(f"  Monitors Connected: {status['summary']['total_monitors_connected']}")
    print(f"  Available for Tasks: {status['summary']['total_available']}")
    print(f"  Pending Tasks: {status['summary']['total_pending_tasks']}")
    print(f"  Completed Tasks: {status['summary']['total_completed_tasks']}")
    
    print("\n📱 CLI Status:")
    print("-" * 70)
    
    for cli_name, info in status['cli_status'].items():
        # 상태 아이콘
        if info['available']:
            icon = "✅"
        elif info['main_process']:
            icon = "🟡"  # 앱은 실행 중이지만 모니터 없음
        else:
            icon = "❌"
        
        print(f"\n{icon} {cli_name.upper()}")
        print(f"   App Running: {'Yes' if info['main_process'] else 'No'}")
        if info['main_process']:
            print(f"   Process Count: {info['process_count']} (main only)")
        print(f"   Monitor: {'Connected' if info['monitor_connected'] else 'Not Connected'}")
        
        if info['monitor_connected']:
            print(f"   Monitor Status: {info['monitor_status']}")
            print(f"   Last Update: {info.get('last_monitor_update', 'N/A')}")
        
        if info['pending_tasks'] > 0:
            print(f"   Pending Tasks: {info['pending_tasks']}")
        if info['completed_tasks'] > 0:
            print(f"   Completed Tasks: {info['completed_tasks']}")
    
    print("\n" + "=" * 70)
    print("💡 Note: Only CLIs with connected monitors can receive tasks")
    
    # JSON 리포트 저장
    report_path = '/tmp/cli_status_v2.json'
    with open(report_path, 'w') as f:
        json.dump(status, f, indent=2)
    
    print(f"📄 Full report saved to: {report_path}")

if __name__ == "__main__":
    main()