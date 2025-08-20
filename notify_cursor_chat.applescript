tell application "Cursor"
    activate
end tell

tell application "System Events"
    delay 0.5
    -- Cmd+L to focus on chat
    keystroke "l" using command down
    delay 0.5
    keystroke "GitHub Issue #9에 테스트 공지가 있습니다. 확인하세요: https://github.com/ihw33/ai-orchestra-dashboard/issues/9"
    keystroke return
end tell