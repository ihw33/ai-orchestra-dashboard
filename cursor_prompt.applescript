tell application "Cursor"
    activate
end tell

tell application "System Events"
    delay 0.5
    -- Cmd+L to focus on chat
    keystroke "l" using command down
    delay 0.5
    keystroke "GitHub Issue #9를 확인하고 댓글을 남겨주세요. 먼저 gh issue view 9 -R ihw33/ai-orchestra-dashboard 명령으로 내용을 확인한 다음, gh issue comment 명령으로 확인 댓글을 남겨주세요."
    keystroke return
end tell