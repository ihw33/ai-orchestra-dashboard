#!/usr/bin/env python3
"""
Terminal Notifier
터미널에 직접 알림 메시지를 보내는 시스템
"""

import subprocess
import sys
from datetime import datetime

def send_terminal_notification(cli_name: str, message: str):
    """터미널에 알림 표시"""
    
    # macOS 터미널 알림
    timestamp = datetime.now().strftime('%H:%M:%S')
    
    # 1. osascript를 사용한 시스템 알림
    try:
        notification_text = f"🏓 PING from Dashboard\n{cli_name.upper()} - {timestamp}"
        subprocess.run([
            'osascript', '-e',
            f'display notification "{message}" with title "{notification_text}" sound name "Ping"'
        ])
    except:
        pass
    
    # 2. 터미널 벨 소리
    print(f"\a\033[1;32m{'='*50}\033[0m")
    print(f"\033[1;33m🏓 PING RECEIVED - {cli_name.upper()}\033[0m")
    print(f"\033[1;36m{message}\033[0m")
    print(f"\033[1;35mTime: {timestamp}\033[0m")
    print(f"\033[1;32m{'='*50}\033[0m\n")
    
    # 3. iTerm2 특수 기능 (Badge 표시)
    if 'iTerm' in subprocess.run(['echo', '$TERM_PROGRAM'], 
                                  capture_output=True, text=True).stdout:
        # iTerm2 Badge 설정
        badge_text = f"PING {cli_name}"
        subprocess.run(['printf', f'\033]1337;SetBadgeFormat={badge_text}\a'])
    
    return True

def flash_terminal(cli_name: str):
    """터미널 창을 깜빡이게 함"""
    
    # ANSI 이스케이프 코드로 화면 깜빡임 효과
    flash_sequence = [
        "\033[?5h",  # 화면 반전
        "\033[?5l",  # 화면 정상
    ]
    
    import time
    for _ in range(3):  # 3번 깜빡임
        for seq in flash_sequence:
            print(seq, end='', flush=True)
            time.sleep(0.1)
    
    # 큰 시각적 알림
    print("\n")
    print("\033[1;42m" + " " * 60 + "\033[0m")
    print("\033[1;42m" + f"  🏓 PING ALERT - {cli_name.upper()}  ".center(60) + "\033[0m")
    print("\033[1;42m" + " " * 60 + "\033[0m")
    print("\n")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cli_name = sys.argv[1]
        message = sys.argv[2] if len(sys.argv) > 2 else "Ping from Dashboard"
        
        send_terminal_notification(cli_name, message)
        flash_terminal(cli_name)