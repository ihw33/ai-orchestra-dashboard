#!/usr/bin/env python3
"""
엔터 확인 테스트
메시지 전송 후 엔터가 제대로 눌렸는지 확인
"""

import subprocess
import time

def check_session_state(session_name):
    """세션 상태 확인"""
    script = f'''
    tell application "iTerm2"
        tell current window
            repeat with aTab in tabs
                repeat with aSession in sessions of aTab
                    if name of aSession contains "{session_name}" then
                        set sessionInfo to "found|"
                        if is at shell prompt of aSession then
                            set sessionInfo to sessionInfo & "at_prompt|"
                        else
                            set sessionInfo to sessionInfo & "not_at_prompt|"
                        end if
                        
                        if is processing of aSession then
                            set sessionInfo to sessionInfo & "processing"
                        else
                            set sessionInfo to sessionInfo & "idle"
                        end if
                        return sessionInfo
                    end if
                end repeat
            end repeat
        end tell
    end tell
    return "not_found||"
    '''
    
    result = subprocess.run(
        ['osascript', '-e', script],
        capture_output=True,
        text=True
    )
    
    parts = result.stdout.strip().split('|')
    return {
        "found": parts[0] == "found",
        "at_prompt": "at_prompt" in parts[1] if len(parts) > 1 else False,
        "processing": "processing" in parts[2] if len(parts) > 2 else False
    }

def send_with_enter_check(session_name, command):
    """명령 전송 후 엔터 확인"""
    print(f"\n📤 세션: {session_name}")
    print(f"   명령: {command}")
    
    # 1. 전송 전 상태
    before = check_session_state(session_name.split('(')[0].strip())
    print(f"   전송 전: 프롬프트={before['at_prompt']}, 처리중={before['processing']}")
    
    # 2. 명령 전송
    script = f'''
    tell application "iTerm2"
        tell current window
            repeat with aTab in tabs
                repeat with aSession in sessions of aTab
                    if name of aSession contains "{session_name.split('(')[0].strip()}" then
                        tell aSession to write text "{command}"
                        return "sent"
                    end if
                end repeat
            end repeat
        end tell
    end tell
    '''
    
    subprocess.run(['osascript', '-e', script])
    
    # 3. 잠시 대기
    time.sleep(1)
    
    # 4. 전송 후 상태
    after = check_session_state(session_name.split('(')[0].strip())
    print(f"   전송 후: 프롬프트={after['at_prompt']}, 처리중={after['processing']}")
    
    # 5. 엔터 판단
    if before['at_prompt'] and not after['at_prompt']:
        print("   ✅ 엔터 성공 - 명령 실행 시작")
    elif after['processing']:
        print("   ✅ 엔터 성공 - 처리 중")
    elif before['at_prompt'] and after['at_prompt']:
        print("   ⚠️ 엔터 미전송 - 여전히 프롬프트 대기")
        
        # 엔터 재전송
        print("   🔄 엔터 재전송...")
        script_enter = f'''
        tell application "iTerm2"
            tell current window
                repeat with aTab in tabs
                    repeat with aSession in sessions of aTab
                        if name of aSession contains "{session_name.split('(')[0].strip()}" then
                            tell aSession to write text ""
                            return "enter_sent"
                        end if
                    end repeat
                end repeat
            end tell
        end tell
        '''
        subprocess.run(['osascript', '-e', script_enter])
        
        time.sleep(0.5)
        final = check_session_state(session_name.split('(')[0].strip())
        if not final['at_prompt'] or final['processing']:
            print("   ✅ 엔터 재전송 성공")
        else:
            print("   ❌ 엔터 재전송 실패")
    else:
        print("   ❓ 상태 불명확")

def main():
    print("🧪 엔터 확인 테스트")
    print("=" * 60)
    
    # 테스트할 세션과 명령
    test_cases = [
        ("-zsh", "echo 'Test from PM Claude'"),
        ("-zsh", "ls -la | head -5"),
        ("🌟 Gemini - AI Engine", "# 테스트 메시지입니다")
    ]
    
    for session, command in test_cases:
        send_with_enter_check(session, command)
        time.sleep(2)

if __name__ == "__main__":
    main()