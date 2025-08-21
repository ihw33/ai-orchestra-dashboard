tell application "Cursor"
    activate
end tell

tell application "System Events"
    -- Ctrl+` to open terminal
    key code 50 using control down
    delay 1
    keystroke "gh issue view 9 -R ihw33/ai-orchestra-dashboard"
    keystroke return
end tell