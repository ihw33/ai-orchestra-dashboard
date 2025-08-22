#!/bin/bash
# AI Orchestra Dashboard - Monitor 시작 스크립트

echo "🚀 Starting AI CLI Monitors..."
echo "================================"

cd /Users/m4_macbook/ai-orchestra-dashboard

# 각 모니터를 새 터미널 탭에서 실행
echo "Starting Cursor Monitor..."
osascript -e 'tell app "iTerm"
    tell current window
        create tab with default profile
        tell current session
            write text "cd /Users/m4_macbook/ai-orchestra-dashboard && python3 scripts/cli_monitor_v2.py --cli cursor"
        end tell
    end tell
end tell'

sleep 1

echo "Starting Codex Monitor..."
osascript -e 'tell app "iTerm"
    tell current window
        create tab with default profile
        tell current session
            write text "cd /Users/m4_macbook/ai-orchestra-dashboard && python3 scripts/cli_monitor_v2.py --cli codex"
        end tell
    end tell
end tell'

sleep 1

echo "Starting Gemini Monitor..."
osascript -e 'tell app "iTerm"
    tell current window
        create tab with default profile
        tell current session
            write text "cd /Users/m4_macbook/ai-orchestra-dashboard && python3 scripts/cli_monitor_v2.py --cli gemini"
        end tell
    end tell
end tell'

echo ""
echo "✅ All monitors started in separate iTerm tabs!"
echo "🏓 You can now send pings from the dashboard"