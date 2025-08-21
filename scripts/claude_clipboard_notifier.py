#!/usr/bin/env python3
"""
Claude Clipboard Notifier
작업을 클립보드에 복사하고 Claude를 활성화하는 간단한 방식
"""

import subprocess
import sys
import json
from datetime import datetime

def notify_claude_with_task(task_data):
    """Claude에 작업 알림 - 클립보드 방식"""
    
    # 작업 메시지 생성
    message = f"""
=== Task from PM Dashboard ===
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Type: {task_data.get('type', 'manual')}
Priority: {task_data.get('priority', 'normal')}

Task Description:
{task_data.get('description', 'No description provided')}

Please work on this task.
===========================
"""
    
    # 클립보드에 복사
    process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
    process.communicate(message.encode('utf-8'))
    
    # Claude 앱 활성화 + 알림
    script = '''
    tell application "Claude"
        activate
    end tell
    
    display notification "Task copied to clipboard. Press Cmd+V to paste in Claude." with title "📋 New Task from PM Dashboard" sound name "Hero"
    '''
    
    subprocess.run(['osascript', '-e', script])
    
    print(f"✅ Task copied to clipboard")
    print(f"📋 Message:\n{message}")
    print(f"\n⚠️ Please paste (Cmd+V) in Claude to start the task")
    
    return True

if __name__ == "__main__":
    # 테스트
    test_task = {
        'type': 'manual',
        'description': 'Test task from clipboard notifier',
        'priority': 'normal'
    }
    
    notify_claude_with_task(test_task)