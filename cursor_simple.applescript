tell application "Cursor"
    activate
end tell

tell application "System Events"
    keystroke "l" using command down
    delay 1
    keystroke "Issue #9 확인: gh issue view 9 -R ihw33/ai-orchestra-dashboard"
    keystroke return
end tell