#!/usr/bin/env python3
"""
CLI Automation Bridge
PM이 할당한 작업을 실제 AI CLI에서 자동 실행
"""

import subprocess
import json
import time
from pathlib import Path
from datetime import datetime

class CLIAutomationBridge:
    """실제 AI CLI와 통신하는 브릿지"""
    
    def __init__(self, cli_name: str):
        self.cli_name = cli_name
        self.cli_commands = {
            'gemini': {
                'start': 'gemini',
                'send_message': self.send_to_gemini
            },
            'claude': {
                'start': None,  # Claude는 GUI 앱
                'send_message': self.send_to_claude
            },
            'cursor': {
                'start': None,  # Cursor는 GUI 앱
                'send_message': self.send_to_cursor
            },
            'codex': {
                'start': 'codex',
                'send_message': self.send_to_codex
            }
        }
    
    def send_to_gemini(self, message: str):
        """Gemini CLI에 메시지 전송"""
        from terminal_cli_bridge import TerminalCLIBridge
        
        bridge = TerminalCLIBridge('gemini')
        
        # Issue 형식으로 변환
        issue_data = {
            'description': message,
            'number': 'Manual',
            'title': 'Task from PM Dashboard'
        }
        
        return bridge.send_issue_to_cli(issue_data)
    
    def send_to_claude(self, message: str):
        """Claude GUI에 메시지 전송"""
        import tempfile
        import os
        
        # 메시지를 임시 파일에 저장
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
            f.write(message)
            temp_path = f.name
        
        # 클립보드에 메시지 복사
        subprocess.run(['pbcopy'], stdin=open(temp_path, 'r', encoding='utf-8'))
        
        # Claude 앱 활성화 - 새 대화를 열지 않고 현재 대화에 입력
        script = '''
        tell application "Claude"
            activate
        end tell
        
        delay 2
        
        tell application "System Events"
            tell process "Claude"
                -- 현재 입력 필드 클리어 (Cmd+A)
                keystroke "a" using command down
                delay 0.5
                
                -- 클립보드 내용 붙여넣기
                keystroke "v" using command down
                delay 1
                
                -- Enter로 전송
                key code 36
            end tell
        end tell
        '''
        
        try:
            subprocess.run(['osascript', '-e', script], check=True)
            print(f"✅ Claude에 메시지 전송 완료")
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Claude 제어 중 오류: {e}")
            # 대체 방법: 기본 입력 필드에 바로 붙여넣기
            fallback_script = '''
            tell application "Claude"
                activate
            end tell
            
            delay 2
            
            tell application "System Events"
                tell process "Claude"
                    -- 입력 필드 클릭 (화면 하단)
                    -- 붙여넣기
                    keystroke "a" using command down
                    delay 0.5
                    keystroke "v" using command down
                    delay 1
                    -- Enter로 전송
                    key code 36
                end tell
            end tell
            '''
            subprocess.run(['osascript', '-e', fallback_script])
        
        # 임시 파일 삭제
        os.unlink(temp_path)
        
        return True
    
    def send_to_cursor(self, message: str):
        """Cursor IDE에 메시지 전송"""
        # Cursor CLI 명령 사용
        project_path = "/Users/m4_macbook/ai-orchestra-dashboard"
        
        # Cursor에서 새 파일 생성하고 메시지 작성
        script = f'''
        tell application "Cursor"
            activate
        end tell
        
        tell application "System Events"
            tell process "Cursor"
                delay 0.5
                keystroke "p" using {{command down, shift down}} -- Command Palette
                delay 0.5
                keystroke "New AI Chat"
                delay 0.5
                keystroke return
                delay 1
                keystroke "{message}"
                delay 0.5
                keystroke return
            end tell
        end tell
        '''
        
        subprocess.run(['osascript', '-e', script])
        return True
    
    def send_to_codex(self, message: str):
        """Codex CLI에 메시지 전송"""
        from terminal_cli_bridge import TerminalCLIBridge
        
        bridge = TerminalCLIBridge('codex')
        
        # Issue 형식으로 변환
        issue_data = {
            'description': message,
            'number': 'Manual',
            'title': 'Task from PM Dashboard'
        }
        
        return bridge.send_issue_to_cli(issue_data)
    
    def execute_task(self, task: dict):
        """작업 실행"""
        cli = task.get('cli', self.cli_name)
        task_type = task.get('type')
        description = task.get('description', '')
        
        # 작업 메시지 생성
        if task_type == 'issue':
            message = f"📋 새로운 작업이 할당되었습니다:\\n\\nIssue #{task.get('issue_number')}\\n{description}\\n\\n이 작업을 수행해주세요."
        elif task_type == 'manual':
            message = f"🎯 PM으로부터 직접 작업 지시:\\n\\n{description}"
        else:
            message = description
        
        # 해당 CLI에 메시지 전송
        if cli in self.cli_commands:
            send_func = self.cli_commands[cli]['send_message']
            if send_func:
                print(f"📤 {cli.upper()}에 작업 전송 중...")
                success = send_func(message)
                if success:
                    print(f"✅ {cli.upper()}에 작업이 전달되었습니다!")
                    return True
        
        return False

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        cli_name = sys.argv[1]
        message = sys.argv[2]
        
        bridge = CLIAutomationBridge(cli_name)
        
        # 테스트 작업
        test_task = {
            'cli': cli_name,
            'type': 'manual',
            'description': message
        }
        
        bridge.execute_task(test_task)