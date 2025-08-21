tell application "iTerm"
    activate
    tell window 1
        tell tab 4
            select
            tell session 2
                select
                write text "Flash 모델로 전환되었습니다. 작업 준비 완료되었나요?"
            end tell
        end tell
    end tell
end tell

delay 0.5

tell application "System Events"
    tell process "iTerm2"
        keystroke return
    end tell
end tell