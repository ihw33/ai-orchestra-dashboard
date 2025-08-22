#!/usr/bin/env python3
"""
실제 세션 확인 스크립트
"""
import subprocess
import time

def check_tab(tab_number, message):
    """특정 탭에 메시지 전송하여 확인"""
    script = f'''
    tell application "iTerm2"
        tell current window
            tell tab {tab_number}
                select
                tell current session
                    write text "# === Tab {tab_number} 확인 ==="
                    write text "{message}"
                end tell
            end tell
        end tell
    end tell
    '''
    
    try:
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Tab {tab_number}: 메시지 전송 성공")
        else:
            print(f"❌ Tab {tab_number}: 전송 실패 - {result.stderr}")
    except Exception as e:
        print(f"❌ Tab {tab_number}: 에러 - {e}")

print("🔍 iTerm2 세션 확인 시작\n")

# 각 탭에 확인 메시지 전송
tabs_to_check = [
    (1, "echo 'Tab 1: Claude PM (이 탭)'"),
    (2, "echo 'Tab 2: Gemini인가요? gemini --version 명령 실행 가능?'"),
    (3, "echo 'Tab 3: Codex인가요? codex --version 명령 실행 가능?'"),
    (4, "echo 'Tab 4: Claude인가요? claude --version 명령 실행 가능?'"),
]

for tab_num, message in tabs_to_check:
    check_tab(tab_num, message)
    time.sleep(1)

print("\n각 탭을 확인해서 어떤 CLI가 실행 중인지 확인해주세요!")