#!/usr/bin/env python3
"""
Clipboard Bridge for Terminal CLIs
클립보드를 통해 메시지를 전달하고 알림
"""

import subprocess
import json
from datetime import datetime

def send_via_clipboard(cli_name: str, message: str):
    """클립보드로 메시지 복사하고 알림"""
    
    # 메시지를 클립보드에 복사
    process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
    process.communicate(message.encode('utf-8'))
    
    # 알림 표시
    notification = f"Task copied! Go to {cli_name.upper()}-AI tab and paste (Cmd+V)"
    
    script = f'''
    display notification "{notification}" with title "📋 Task for {cli_name.upper()}" sound name "Hero"
    
    tell application "iTerm"
        activate
    end tell
    '''
    
    subprocess.run(['osascript', '-e', script])
    
    print(f"✅ Task copied to clipboard for {cli_name}")
    print(f"📋 Message: {message}")
    print(f"⚠️ Please go to {cli_name.upper()}-AI tab and paste (Cmd+V)")
    
    return True

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        cli_name = sys.argv[1]
        message = sys.argv[2]
        send_via_clipboard(cli_name, message)