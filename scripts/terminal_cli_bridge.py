#!/usr/bin/env python3
"""
Terminal CLI Bridge
터미널 기반 AI CLI (Gemini, Codex)와 통신하는 브릿지
iTerm2의 특정 세션에 명령을 전송
"""

import subprocess
import json
import time
from pathlib import Path
from datetime import datetime

class TerminalCLIBridge:
    """터미널 AI CLI와 통신하는 브릿지"""
    
    def __init__(self, cli_name: str):
        self.cli_name = cli_name
        self.session_file = Path.home() / f".ai-orchestra/sessions/{cli_name}_session.txt"
        self.session_file.parent.mkdir(parents=True, exist_ok=True)
        
    def start_cli_if_needed(self):
        """CLI가 실행중이 아니면 시작"""
        # CLI 실행 확인
        check_cmd = f"pgrep -f {self.cli_name}"
        result = subprocess.run(check_cmd, shell=True, capture_output=True)
        
        if not result.stdout:
            print(f"🚀 Starting {self.cli_name} in new iTerm tab...")
            
            # iTerm2에서 새 탭 열고 CLI 시작
            script = f'''
            tell application "iTerm"
                tell current window
                    set newTab to (create tab with default profile)
                    tell current session of newTab
                        write text "{self.cli_name}"
                        delay 3
                        write text "# {self.cli_name.upper()} CLI Ready for PM Tasks"
                    end tell
                end tell
            end tell
            '''
            
            subprocess.run(['osascript', '-e', script])
            time.sleep(5)  # CLI 시작 대기
            print(f"✅ {self.cli_name} started")
            return True
        else:
            print(f"✅ {self.cli_name} already running")
            return False
    
    def send_to_terminal_cli(self, message: str):
        """터미널 CLI에 메시지 전송"""
        
        # CLI 시작 확인
        self.start_cli_if_needed()
        
        # 메시지 단순화 - 한글 제거하고 영어만
        if 'Description:' in message:
            task_desc = message.split('Description:')[1].split('\n')[0].strip()
        else:
            task_desc = message.strip()
        
        # 영어로만 작성
        simple_message = f"Task from PM: {task_desc}"
        
        # 특수문자 이스케이프
        simple_message = simple_message.replace('"', '\\"').replace("'", "\\'")
        
        # iTerm2의 특정 세션에 직접 전송
        target_session = f"{self.cli_name.upper()}-AI"
        
        script = f'''
        tell application "iTerm"
            repeat with w in windows
                repeat with t in tabs of w
                    repeat with s in sessions of t
                        if name of s contains "{target_session}" then
                            tell s
                                write text "{simple_message}"
                            end tell
                            return "sent"
                        end if
                    end repeat
                end repeat
            end repeat
        end tell
        '''
        
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
        
        if "sent" in result.stdout:
            print(f"✅ Message sent to {target_session}")
        else:
            print(f"⚠️ Could not find session {target_session}, sending to current session")
            # 실패 시 현재 세션에 시도
            fallback_script = f'''
            tell application "iTerm"
                tell current session of current window
                    write text "{simple_message}"
                end tell
            end tell
            '''
            subprocess.run(['osascript', '-e', fallback_script])
        
        return True
    
    def send_issue_to_cli(self, issue_data: dict):
        """GitHub Issue를 CLI에 전송"""
        
        # Issue 정보를 CLI 명령 형식으로 변환
        if self.cli_name == "gemini":
            # Gemini 형식
            prompt = f"""
Please analyze and work on this GitHub Issue:

Issue #{issue_data.get('number', 'N/A')}
Title: {issue_data.get('title', 'No title')}
Description: {issue_data.get('description', 'No description')}

Provide your analysis and solution.
"""
        elif self.cli_name == "codex":
            # Codex 형식
            prompt = f"""
GitHub Issue #{issue_data.get('number', 'N/A')}
Title: {issue_data.get('title', '')}
Task: {issue_data.get('description', '')}

Generate code or solution for this issue.
"""
        else:
            # 기본 형식
            prompt = f"""
Task from PM Dashboard:
{issue_data.get('description', 'No description')}
"""
        
        # 터미널에 전송
        return self.send_to_terminal_cli(prompt)

def test_terminal_cli(cli_name: str):
    """터미널 CLI 테스트"""
    bridge = TerminalCLIBridge(cli_name)
    
    test_issue = {
        'number': 42,
        'title': 'Test Issue',
        'description': 'Please explain Python decorators with an example'
    }
    
    bridge.send_issue_to_cli(test_issue)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        test_terminal_cli(sys.argv[1])
    else:
        print("Usage: python terminal_cli_bridge.py [gemini|codex]")