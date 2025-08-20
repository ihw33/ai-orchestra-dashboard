tell application "iTerm"
    tell session 3 of tab 4 of current window
        write text "Issue #5 작업이 완료되었으면 다음 명령어로 완료 보고하세요: gh issue comment 5 -R ihw33/ai-orchestra-dashboard --body '[Gemini 보고] ✅ 작업 완료: GitHub API 연동 완료, 데이터 수집 서비스 구현 완료. MultiProjectMonitor 클래스 작성 완료.'"
    end tell
end tell
tell application "System Events"
    keystroke return
end tell