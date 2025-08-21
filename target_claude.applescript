tell application "iTerm"
    tell window 1
        tell tab 4
            select
            tell session 1
                select
                write text "PM Claude에게 보내는 메시지입니다"
            end tell
        end tell
    end tell
end tell

delay 1

tell application "System Events"
    key code 36
end tell