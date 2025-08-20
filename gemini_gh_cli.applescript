tell application "iTerm"
    tell session 3 of tab 4 of current window
        write text "GitHub CLI를 사용해서 Issue #5에 완료 보고를 남기세요. 명령어: gh issue comment 5 -R ihw33/ai-orchestra-dashboard --body '[Gemini 보고] ✅ 작업 완료: Data Collection 서비스 구현 완료. MultiProjectMonitor, MetricsAggregator, WebSocket 매니저 모두 구현 완료.'"
    end tell
end tell
tell application "System Events"
    keystroke return
end tell