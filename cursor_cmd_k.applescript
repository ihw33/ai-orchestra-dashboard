tell application "Cursor"
    activate
end tell

delay 1

tell application "System Events"
    tell process "Cursor"
        -- Cmd+K to open AI chat
        keystroke "k" using command down
        delay 1
        
        -- Type message
        keystroke "안녕하세요! Orchestra Dashboard 프로젝트 테스트입니다."
        delay 0.5
        
        -- Send message
        keystroke return
    end tell
end tell