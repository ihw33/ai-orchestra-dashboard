tell application "Cursor"
    activate
end tell

delay 1

tell application "System Events"
    tell process "Cursor"
        -- Cmd+L to focus on chat
        keystroke "l" using command down
        delay 1
        
        -- Type message
        keystroke "Orchestra Dashboard 프로젝트 작업 준비되셨나요?"
        delay 0.5
        
        -- Send message
        keystroke return
    end tell
end tell