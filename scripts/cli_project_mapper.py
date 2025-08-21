#!/usr/bin/env python3
"""
CLI Project Mapper
각 CLI 세션을 프로젝트별로 구분하고 관리하는 시스템
"""

import subprocess
import json
import os
import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import hashlib

class CLIProjectMapper:
    """프로젝트별 CLI 세션 매핑 및 관리"""
    
    def __init__(self):
        self.cli_sessions = {}  # {session_id: {cli_type, project, window_info}}
        self.project_mappings = {}  # {project_name: [session_ids]}
        
    def get_terminal_sessions_detailed(self) -> List[Dict]:
        """터미널 세션의 상세 정보 가져오기"""
        sessions = []
        
        try:
            # Terminal.app의 모든 창과 탭 정보 가져오기
            terminal_script = '''
            tell application "Terminal"
                set sessionInfo to {}
                set windowIndex to 1
                repeat with w in windows
                    set tabIndex to 1
                    repeat with t in tabs of w
                        set sessionData to {windowIndex, tabIndex, name of w, current settings of t, history of t}
                        set end of sessionInfo to sessionData
                        set tabIndex to tabIndex + 1
                    end repeat
                    set windowIndex to windowIndex + 1
                end repeat
                return sessionInfo
            end tell
            '''
            
            result = subprocess.run(
                ["osascript", "-e", terminal_script],
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.returncode == 0:
                # 결과 파싱
                output = result.stdout.strip()
                # 간단한 파싱 (실제로는 더 복잡할 수 있음)
                sessions.append({
                    "app": "Terminal",
                    "data": output
                })
                
        except Exception as e:
            print(f"Error getting Terminal sessions: {e}")
        
        # iTerm2 정보 가져오기
        try:
            iterm_script = '''
            tell application "iTerm"
                set sessionInfo to {}
                repeat with w in windows
                    set windowId to id of w
                    repeat with t in tabs of w
                        repeat with s in sessions of t
                            set sessionData to {windowId, name of s, tty of s}
                            set end of sessionInfo to sessionData
                        end repeat
                    end repeat
                end repeat
                return sessionInfo
            end tell
            '''
            
            result = subprocess.run(
                ["osascript", "-e", iterm_script],
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.returncode == 0:
                sessions.append({
                    "app": "iTerm",
                    "data": result.stdout.strip()
                })
                
        except Exception as e:
            print(f"Error getting iTerm sessions: {e}")
        
        return sessions
    
    def identify_project_from_path(self, path: str) -> Optional[str]:
        """경로에서 프로젝트 이름 추출"""
        # 일반적인 프로젝트 경로 패턴
        patterns = [
            r'/([^/]+)/(?:src|app|backend|frontend)',  # 프로젝트 루트
            r'/Documents/GitHub/([^/]+)',  # GitHub 프로젝트
            r'/([^/]+)\.git',  # Git 저장소
            r'/Users/[^/]+/([^/]+)$',  # 홈 디렉토리 하위 프로젝트
        ]
        
        for pattern in patterns:
            match = re.search(pattern, path)
            if match:
                return match.group(1)
        
        # 마지막 디렉토리명을 프로젝트로 사용
        if '/' in path:
            return path.split('/')[-1]
        
        return None
    
    def get_window_working_directory(self, window_id: str, tab_id: str = None) -> Optional[str]:
        """특정 창/탭의 현재 작업 디렉토리 가져오기"""
        try:
            # lsof를 사용하여 터미널 프로세스의 cwd 찾기
            result = subprocess.run(
                ["lsof", "-a", "-d", "cwd", "-c", "bash"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if 'cwd' in line and 'DIR' in line:
                        # 경로 추출
                        parts = line.split()
                        if len(parts) > 8:
                            return parts[-1]
                            
        except Exception as e:
            print(f"Error getting working directory: {e}")
        
        return None
    
    def scan_cli_sessions(self) -> Dict:
        """모든 CLI 세션 스캔 및 프로젝트별 분류"""
        
        # 프로세스 목록에서 CLI 관련 정보 수집
        try:
            # ps 명령으로 상세 정보 가져오기
            result = subprocess.run(
                ["ps", "aux"],
                capture_output=True,
                text=True
            )
            
            cli_processes = []
            for line in result.stdout.split('\n'):
                # CLI 관련 프로세스 찾기
                cli_indicators = ['claude', 'cursor', 'codex', 'gemini', 'code', 'ChatGPT']
                for indicator in cli_indicators:
                    if indicator.lower() in line.lower():
                        # PID와 명령어 추출
                        parts = line.split(None, 10)
                        if len(parts) > 10:
                            pid = parts[1]
                            cmd = parts[10]
                            
                            # 작업 디렉토리 찾기
                            cwd = self.get_process_cwd(pid)
                            project = self.identify_project_from_path(cwd) if cwd else "unknown"
                            
                            # 세션 ID 생성 (PID 기반)
                            session_id = f"{indicator}_{pid}_{project}"
                            
                            self.cli_sessions[session_id] = {
                                "cli_type": indicator,
                                "project": project,
                                "pid": pid,
                                "command": cmd,
                                "working_dir": cwd,
                                "detected_at": datetime.utcnow().isoformat()
                            }
                            
                            # 프로젝트 매핑 업데이트
                            if project not in self.project_mappings:
                                self.project_mappings[project] = []
                            self.project_mappings[project].append(session_id)
                            
                            cli_processes.append({
                                "session_id": session_id,
                                "cli": indicator,
                                "project": project,
                                "pid": pid
                            })
                            break
            
        except Exception as e:
            print(f"Error scanning CLI sessions: {e}")
        
        return {
            "sessions": self.cli_sessions,
            "projects": self.project_mappings,
            "summary": {
                "total_sessions": len(self.cli_sessions),
                "total_projects": len(self.project_mappings),
                "sessions_by_project": {
                    project: len(sessions) 
                    for project, sessions in self.project_mappings.items()
                }
            }
        }
    
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
                        
        except Exception as e:
            print(f"Error getting cwd for PID {pid}: {e}")
        
        return None
    
    def assign_cli_for_project(self, project_name: str, task_type: str) -> Optional[Dict]:
        """특정 프로젝트를 위한 CLI 할당"""
        
        # 해당 프로젝트에서 사용 가능한 CLI 세션 찾기
        if project_name in self.project_mappings:
            available_sessions = self.project_mappings[project_name]
            
            # 작업 유형에 맞는 CLI 찾기
            task_cli_mapping = {
                "frontend": ["vscode", "cursor"],
                "backend": ["codex", "claude"],
                "documentation": ["cursor", "gemini"],
                "review": ["claude", "cursor"],
                "api": ["codex", "claude"]
            }
            
            preferred_clis = task_cli_mapping.get(task_type, ["claude", "cursor"])
            
            for session_id in available_sessions:
                session = self.cli_sessions[session_id]
                cli_type = session["cli_type"].lower()
                
                for preferred in preferred_clis:
                    if preferred in cli_type:
                        return {
                            "session_id": session_id,
                            "cli_type": cli_type,
                            "project": project_name,
                            "session_info": session
                        }
            
            # 선호 CLI가 없으면 첫 번째 사용 가능한 세션 반환
            if available_sessions:
                session_id = available_sessions[0]
                return {
                    "session_id": session_id,
                    "cli_type": self.cli_sessions[session_id]["cli_type"],
                    "project": project_name,
                    "session_info": self.cli_sessions[session_id]
                }
        
        return None
    
    def create_session_tag(self, project: str, cli_type: str) -> str:
        """세션 식별 태그 생성"""
        # 프로젝트와 CLI 타입을 조합한 고유 태그
        tag = f"[{project}:{cli_type}:{datetime.utcnow().strftime('%H%M')}]"
        return tag
    
    def send_to_specific_session(self, session_id: str, message: str) -> bool:
        """특정 세션에 메시지 전송"""
        if session_id not in self.cli_sessions:
            return False
        
        session = self.cli_sessions[session_id]
        pid = session.get("pid")
        
        # 세션 태그 추가
        project = session.get("project", "unknown")
        cli_type = session.get("cli_type", "unknown")
        tag = self.create_session_tag(project, cli_type)
        
        tagged_message = f"{tag} {message}"
        
        # 프로세스에 시그널 또는 메시지 전송
        # 실제 구현은 CLI 타입에 따라 다를 수 있음
        try:
            # AppleScript를 사용하여 특정 창에 메시지 전송
            if "cursor" in cli_type.lower() or "code" in cli_type.lower():
                # VSCode/Cursor의 경우
                script = f'''
                tell application "System Events"
                    set frontmost of process "{cli_type}" to true
                    keystroke "{tagged_message}"
                    key code 36  -- Enter key
                end tell
                '''
                subprocess.run(["osascript", "-e", script], check=False)
                return True
                
        except Exception as e:
            print(f"Error sending to session {session_id}: {e}")
        
        return False

def main():
    """테스트 및 리포트 생성"""
    mapper = CLIProjectMapper()
    result = mapper.scan_cli_sessions()
    
    print("=" * 70)
    print("CLI Project Mapping Report")
    print("=" * 70)
    print(f"Total Sessions: {result['summary']['total_sessions']}")
    print(f"Total Projects: {result['summary']['total_projects']}")
    
    print("\n📁 Projects and their CLI sessions:")
    print("-" * 70)
    
    for project, sessions in result['projects'].items():
        print(f"\n🗂️  Project: {project}")
        for session_id in sessions:
            session = result['sessions'][session_id]
            print(f"   └─ {session['cli_type']} (PID: {session['pid']})")
            if session.get('working_dir'):
                print(f"      Working Dir: {session['working_dir']}")
    
    # 작업 할당 테스트
    print("\n" + "=" * 70)
    print("Task Assignment Test")
    print("-" * 70)
    
    test_cases = [
        ("ai-orchestra-dashboard", "frontend"),
        ("ai-orchestra-dashboard", "backend"),
        ("personal-journal", "documentation"),
        ("iwl-project", "api")
    ]
    
    for project, task_type in test_cases:
        assignment = mapper.assign_cli_for_project(project, task_type)
        if assignment:
            print(f"✅ Project: {project}, Task: {task_type}")
            print(f"   → Assigned to: {assignment['cli_type']} (Session: {assignment['session_id'][:30]}...)")
        else:
            print(f"❌ Project: {project}, Task: {task_type} - No available CLI")
    
    # JSON 리포트 저장
    report_path = '/tmp/cli_project_mapping.json'
    with open(report_path, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"\n📄 Full report saved to: {report_path}")

if __name__ == "__main__":
    main()