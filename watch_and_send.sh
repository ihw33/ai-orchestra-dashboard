#!/bin/bash

# PM Claude 출력 감시하고 자동으로 다른 터미널에 전송
# fswatch 또는 파일 감시 + AppleScript 실행

echo "🎯 AI Orchestra 자동 플로우 시작"
echo "PM Claude 출력 감시 중..."

# 로그 파일 감시
tail -f ~/ai-orchestra-dashboard/cli-bridge/logs/pm-claude.out | while read line
do
    # @gemini: 패턴 감지
    if [[ $line == *"@gemini:"* ]]; then
        MESSAGE=$(echo "$line" | sed 's/.*@gemini://g')
        echo "📤 Gemini에게 전송: $MESSAGE"
        
        # AppleScript로 실제 키보드 입력
        osascript -e "
        tell application \"Terminal\"
            activate
            tell window 2
                tell application \"System Events\"
                    keystroke \"$MESSAGE\"
                    key code 36
                end tell
            end tell
        end tell"
    fi
    
    # @codex: 패턴 감지
    if [[ $line == *"@codex:"* ]]; then
        MESSAGE=$(echo "$line" | sed 's/.*@codex://g')
        echo "📤 Codex에게 전송: $MESSAGE"
        
        osascript -e "
        tell application \"Terminal\"
            activate
            tell window 3
                tell application \"System Events\"
                    keystroke \"$MESSAGE\"
                    key code 36
                end tell
            end tell
        end tell"
    fi
done