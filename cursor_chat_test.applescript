tell application "Cursor"
    activate
end tell

delay 1

tell application "System Events"
    -- Cmd+L to focus on chat
    keystroke "l" using command down
    delay 0.5
    
    -- Type message
    keystroke "안녕하세요 Cursor! Orchestra Dashboard 프로젝트에서 작업 중이신가요?"
    delay 0.5
    
    -- Send message
    keystroke return
end tell