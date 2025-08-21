#!/usr/bin/env python3
"""
CLI Detector and Mapper
실제 열려있는 CLI를 감지하고 작업을 매핑하는 시스템
"""

import subprocess
import json
import os
from typing import Dict, List, Optional
from datetime import datetime

class CLIDetector:
    """열려있는 CLI 터미널 감지 및 관리"""
    
    def __init__(self):
        self.cli_mapping = {
            "claude": {
                "process_names": ["claude", "claude-cli", "Claude.app"],
                "tmux_session": "claude-cli",
                "window_title_patterns": ["Claude", "claude"],
                "capabilities": ["github", "general", "pm"]
            },
            "cursor": {
                "process_names": ["cursor", "Cursor.app", "cursor-cli"],
                "tmux_session": "cursor-cli",
                "window_title_patterns": ["Cursor", "ChatGPT"],
                "capabilities": ["architecture", "planning", "documentation"]
            },
            "codex": {
                "process_names": ["codex", "codex-cli"],
                "tmux_session": "codex-cli",
                "window_title_patterns": ["Codex", "codex"],
                "capabilities": ["backend", "api", "database"]
            },
            "gemini": {
                "process_names": ["gemini", "gemini-cli", "bard"],
                "tmux_session": "gemini-cli",
                "window_title_patterns": ["Gemini", "Bard"],
                "capabilities": ["content", "ux", "research"]
            },
            "vscode": {
                "process_names": ["code", "Code.app", "vscode"],
                "tmux_session": "vscode-cli",
                "window_title_patterns": ["Visual Studio Code", "VSCode"],
                "capabilities": ["frontend", "ui", "components"]
            }
        }
        
        self.active_clis = {}
        
    def detect_tmux_sessions(self) -> List[str]:
        """tmux 세션 감지"""
        try:
            result = subprocess.run(
                ["tmux", "list-sessions", "-F", "#{session_name}"],
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.returncode == 0:
                sessions = result.stdout.strip().split('\n')
                return [s for s in sessions if s]
            
        except Exception as e:
            print(f"Error detecting tmux sessions: {e}")
        
        return []
    
    def detect_terminal_apps(self) -> Dict[str, List[str]]:
        """macOS에서 실행 중인 터미널 앱 감지"""
        detected = {}
        
        try:
            # Terminal.app 창 확인
            terminal_windows = subprocess.run(
                ["osascript", "-e", '''
                tell application "Terminal"
                    set windowList to {}
                    repeat with w in windows
                        set end of windowList to (name of w as string)
                    end repeat
                    return windowList
                end tell
                '''],
                capture_output=True,
                text=True
            )
            
            if terminal_windows.returncode == 0:
                windows = terminal_windows.stdout.strip().split(", ")
                detected["terminal"] = windows
            
            # iTerm2 확인
            iterm_windows = subprocess.run(
                ["osascript", "-e", '''
                tell application "iTerm"
                    set sessionList to {}
                    repeat with w in windows
                        repeat with t in tabs of w
                            repeat with s in sessions of t
                                set end of sessionList to (name of s as string)
                            end repeat
                        end repeat
                    end repeat
                    return sessionList
                end tell
                '''],
                capture_output=True,
                text=True,
                check=False
            )
            
            if iterm_windows.returncode == 0:
                sessions = iterm_windows.stdout.strip().split(", ")
                detected["iterm"] = sessions
                
        except Exception as e:
            print(f"Error detecting terminal apps: {e}")
        
        return detected
    
    def detect_running_processes(self) -> Dict[str, List[Dict]]:
        """실행 중인 프로세스 감지 - 상세 정보 포함"""
        detailed_processes = {}
        
        try:
            result = subprocess.run(
                ["ps", "aux"],
                capture_output=True,
                text=True
            )
            
            for line in result.stdout.split('\n'):
                parts = line.split(None, 10)
                if len(parts) > 10:
                    pid = parts[1]
                    cmd = parts[10]
                    
                    for cli_name, info in self.cli_mapping.items():
                        for process_name in info["process_names"]:
                            if process_name.lower() in cmd.lower():
                                if cli_name not in detailed_processes:
                                    detailed_processes[cli_name] = []
                                
                                # 작업 디렉토리 가져오기
                                cwd = self.get_process_cwd(pid)
                                project = self.extract_project_name(cwd) if cwd else "unknown"
                                
                                detailed_processes[cli_name].append({
                                    "pid": pid,
                                    "project": project,
                                    "working_dir": cwd or "N/A",
                                    "command": cmd[:100],  # 명령어 처음 100자
                                    "status": "active"
                                })
                                break
            
            return detailed_processes
            
        except Exception as e:
            print(f"Error detecting processes: {e}")
            return {}
    
    def get_process_cwd(self, pid: str) -> Optional[str]:
        """프로세스의 현재 작업 디렉토리 가져오기"""
        try:
            result = subprocess.run(
                ["lsof", "-a", "-p", pid, "-d", "cwd", "-F", "n"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                for line in result.stdout.strip().split('\n'):
                    if line.startswith('n'):
                        return line[1:]  # 'n' 제거하고 경로 반환
        except:
            pass
        return None
    
    def extract_project_name(self, path: str) -> str:
        """경로에서 프로젝트 이름 추출"""
        if not path:
            return "unknown"
        
        # 일반적인 프로젝트 경로 패턴에서 이름 추출
        parts = path.split('/')
        
        # GitHub 폴더에서
        if 'GitHub' in parts:
            idx = parts.index('GitHub')
            if idx + 1 < len(parts):
                return parts[idx + 1]
        
        # Documents 폴더에서
        if 'Documents' in parts:
            idx = parts.index('Documents')
            if idx + 1 < len(parts):
                return parts[idx + 1]
        
        # 마지막 폴더명을 프로젝트명으로
        return parts[-1] if parts[-1] else "root"
    
    def identify_cli_from_window(self, window_title: str) -> Optional[str]:
        """창 제목으로 CLI 식별"""
        window_lower = window_title.lower()
        
        for cli_name, info in self.cli_mapping.items():
            for pattern in info["window_title_patterns"]:
                if pattern.lower() in window_lower:
                    return cli_name
        
        return None
    
    def scan_and_map(self) -> Dict:
        """전체 스캔 및 매핑"""
        
        # 1. tmux 세션 확인
        tmux_sessions = self.detect_tmux_sessions()
        
        # 2. 터미널 앱 확인
        terminal_apps = self.detect_terminal_apps()
        
        # 3. 실행 중인 프로세스 확인 (상세 정보 포함)
        detailed_processes = self.detect_running_processes()
        
        # 4. 매핑 결과 생성
        self.active_clis = {}
        
        for cli_name, info in self.cli_mapping.items():
            cli_status = {
                "name": cli_name,
                "available": False,
                "connection_type": None,
                "session_info": None,
                "capabilities": info["capabilities"]
            }
            
            # tmux 세션 확인
            if info["tmux_session"] in tmux_sessions:
                cli_status["available"] = True
                cli_status["connection_type"] = "tmux"
                cli_status["session_info"] = info["tmux_session"]
            
            # 프로세스 확인 (상세 정보 포함)
            elif cli_name in detailed_processes:
                cli_status["available"] = True
                cli_status["connection_type"] = "process"
                cli_status["instances"] = detailed_processes[cli_name]
                cli_status["total_instances"] = len(detailed_processes[cli_name])
                cli_status["session_info"] = f"{len(detailed_processes[cli_name])} instances"
            
            # 터미널 창 확인
            else:
                for app_name, windows in terminal_apps.items():
                    for window in windows:
                        if self.identify_cli_from_window(window) == cli_name:
                            cli_status["available"] = True
                            cli_status["connection_type"] = f"{app_name}_window"
                            cli_status["session_info"] = window
                            break
            
            self.active_clis[cli_name] = cli_status
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "active_clis": self.active_clis,
            "tmux_sessions": tmux_sessions,
            "terminal_windows": terminal_apps,
            "summary": {
                "total_available": sum(1 for c in self.active_clis.values() if c["available"]),
                "connection_types": {
                    "tmux": sum(1 for c in self.active_clis.values() if c["connection_type"] == "tmux"),
                    "process": sum(1 for c in self.active_clis.values() if c["connection_type"] == "process"),
                    "terminal": sum(1 for c in self.active_clis.values() if c["connection_type"] and "window" in c["connection_type"])
                }
            }
        }
    
    def get_best_cli_for_task(self, task_type: str) -> Optional[str]:
        """작업 유형에 가장 적합한 사용 가능한 CLI 찾기"""
        
        # 작업 유형별 선호 CLI
        task_preferences = {
            "github": ["claude", "cursor"],
            "frontend": ["vscode", "cursor"],
            "backend": ["codex", "cursor"],
            "api": ["codex", "claude"],
            "database": ["codex", "claude"],
            "documentation": ["cursor", "gemini"],
            "ux": ["gemini", "cursor"],
            "architecture": ["cursor", "claude"],
            "review": ["claude", "cursor"],
            "planning": ["cursor", "claude", "gemini"]
        }
        
        preferred_clis = task_preferences.get(task_type, ["claude", "cursor"])
        
        # 선호 순서대로 사용 가능한 CLI 찾기
        for cli_name in preferred_clis:
            if cli_name in self.active_clis and self.active_clis[cli_name]["available"]:
                return cli_name
        
        # 선호 CLI가 없으면 아무 사용 가능한 CLI 반환
        for cli_name, status in self.active_clis.items():
            if status["available"]:
                return cli_name
        
        return None
    
    def assign_task_to_cli(self, task: Dict) -> Optional[Dict]:
        """작업을 적절한 CLI에 할당"""
        
        task_type = task.get("type", "general")
        assigned_cli = task.get("preferred_cli")
        
        # 이미 지정된 CLI가 있으면 사용 가능한지 확인
        if assigned_cli:
            if assigned_cli in self.active_clis and self.active_clis[assigned_cli]["available"]:
                return {
                    "cli": assigned_cli,
                    "connection": self.active_clis[assigned_cli],
                    "task": task,
                    "status": "assigned"
                }
        
        # 작업에 가장 적합한 CLI 찾기
        best_cli = self.get_best_cli_for_task(task_type)
        
        if best_cli:
            return {
                "cli": best_cli,
                "connection": self.active_clis[best_cli],
                "task": task,
                "status": "assigned"
            }
        
        return None

def main():
    """테스트 및 상태 출력"""
    detector = CLIDetector()
    result = detector.scan_and_map()
    
    print("=" * 60)
    print("CLI Detection Report")
    print("=" * 60)
    print(f"Timestamp: {result['timestamp']}")
    print(f"\nSummary:")
    print(f"  Total Available CLIs: {result['summary']['total_available']}")
    print(f"  Connection Types:")
    for conn_type, count in result['summary']['connection_types'].items():
        print(f"    - {conn_type}: {count}")
    
    print(f"\nActive CLIs:")
    for cli_name, status in result['active_clis'].items():
        if status['available']:
            print(f"  ✅ {cli_name}:")
            print(f"     Connection: {status['connection_type']}")
            print(f"     Session: {status['session_info']}")
            print(f"     Capabilities: {', '.join(status['capabilities'])}")
        else:
            print(f"  ❌ {cli_name}: Not available")
    
    # 작업 할당 테스트
    print("\n" + "=" * 60)
    print("Task Assignment Test")
    print("=" * 60)
    
    test_tasks = [
        {"type": "frontend", "description": "Update UI components"},
        {"type": "backend", "description": "Fix API endpoint"},
        {"type": "documentation", "description": "Write user guide"},
        {"type": "github", "description": "Review PR #42"}
    ]
    
    for task in test_tasks:
        assignment = detector.assign_task_to_cli(task)
        if assignment:
            print(f"✅ Task: {task['description']}")
            print(f"   Assigned to: {assignment['cli']} via {assignment['connection']['connection_type']}")
        else:
            print(f"❌ Task: {task['description']} - No available CLI")
    
    # JSON 형식으로 저장
    with open('/tmp/cli_detection_report.json', 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"\nFull report saved to: /tmp/cli_detection_report.json")

if __name__ == "__main__":
    main()