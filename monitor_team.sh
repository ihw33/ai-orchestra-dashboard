#!/bin/bash

# 팀 모니터링 스크립트
# 5분마다 자동 실행

echo "🔍 Orchestra Dashboard 팀 모니터링"
echo "================================"
echo "시간: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# 1. GitHub Issue 상태 체크
echo "📋 Issue 상태:"
gh issue list --state open --limit 5

echo ""
echo "💬 최근 Issue 댓글:"
for issue in 4 5 6 7; do
    echo "Issue #$issue:"
    gh issue view $issue --comments | tail -5 | grep -E "commented|🚀|⚙️|🚨|✅" || echo "  댓글 없음 ⚠️"
done

echo ""
echo "📂 최근 파일 변경 (5분 이내):"
find /Users/m4_macbook/Projects/ai-orchestra-dashboard -type f \( -name "*.py" -o -name "*.ts" -o -name "*.tsx" \) -mmin -5 -exec ls -la {} \;

echo ""
echo "🖥️ 서버 상태:"
ps aux | grep -E "uvicorn|npm run dev" | grep -v grep | head -2

echo ""
echo "💬 팀원 활동:"
# Tab 4 세션 체크
osascript -e 'tell application "iTerm"
    tell current window
        tell fourth tab
            set status to {}
            repeat with i from 1 to 4
                tell session i
                    set end of status to "Session " & i & ": " & name
                end tell
            end repeat
            return (status as string)
        end tell
    end tell
end tell'

echo ""
echo "================================"
echo "다음 체크: 5분 후"