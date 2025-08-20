#!/bin/bash

# Simple Auto Confirm - 5초마다 각 세션 체크

echo "🤖 Simple Auto Confirm 시작"
echo "세션: 2(PM), 3(Gemini), 4(Codex)"
echo "중지: Ctrl+C"
echo "========================"

while true; do
    for session in 2 3 4; do
        case $session in
            2) name="PM_Claude" ;;
            3) name="Gemini" ;;
            4) name="Codex" ;;
        esac
        
        echo "[$(date '+%H:%M:%S')] Checking $name..."
        
        osascript -e "
        tell application \"iTerm\"
            tell window 1
                tell current tab
                    if (count of sessions) ≥ $session then
                        tell session $session
                            write text \"1\"
                            write text \"\"
                        end tell
                    end if
                end tell
            end tell
        end tell
        " 2>/dev/null
        
        sleep 2
    done
    
    echo "--- 대기 중 ---"
    sleep 10
done