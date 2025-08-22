#!/usr/bin/env python3
"""
실제 세션 이름으로 테스트
"""

import subprocess
import time

def test_real_session():
    # 실제 세션 이름들 중 하나 선택
    test_sessions = [
        "✳ 한국어 테스트 (claude)",
        "🌟 Gemini - AI Engine (node)", 
        "🔧 Claude - Integration (claude)",
        "-zsh"
    ]
    
    for session_name in test_sessions:
        print(f"\n테스트: {session_name}")
        
        # 세션에 간단한 명령 전송
        script = f'''
        tell application "iTerm2"
            tell current window
                repeat with aTab in tabs
                    repeat with aSession in sessions of aTab
                        if name of aSession contains "{session_name.split('(')[0].strip()}" then
                            tell aSession
                                write text "echo 'Hello from PM Claude'"
                                return "sent to " & name of aSession
                            end tell
                        end if
                    end repeat
                end repeat
            end tell
        end tell
        return "not found"
        '''
        
        result = subprocess.run(
            ['osascript', '-e', script],
            capture_output=True, 
            text=True
        )
        
        print(f"  결과: {result.stdout.strip()}")
        time.sleep(1)

if __name__ == "__main__":
    print("🧪 실제 세션 테스트")
    print("=" * 50)
    test_real_session()