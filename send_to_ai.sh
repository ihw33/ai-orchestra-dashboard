#!/bin/bash
# AI 세션에 직접 명령 전송 스크립트

send_to_gemini() {
    echo "🚀 Gemini에게 전송: $1"
    osascript <<EOF
    tell application "iTerm2"
        tell current window
            tell first tab
                tell second session
                    write text "$1"
                end tell
            end tell
        end tell
    end tell
EOF
}

send_to_codex() {
    echo "🚀 Codex에게 전송: $1"
    osascript <<EOF
    tell application "iTerm2"
        tell current window
            tell second tab
                tell first session
                    write text "$1"
                end tell
            end tell
        end tell
    end tell
EOF
}

# 테스트 실행
echo "===== AI 직접 전송 테스트 ====="

# Gemini 테스트
send_to_gemini "echo 'Gemini 테스트: 2+2는?' | gemini"
sleep 2

# Codex 테스트  
send_to_codex "echo 'Codex 테스트 완료'"
sleep 1

echo "✅ 전송 완료 - iTerm2 화면을 확인하세요!"