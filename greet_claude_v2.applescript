tell application "iTerm"
    tell current window
        tell tab 4
            tell session 1
                write text "안녕하세요 Claude님!"
            end tell
        end tell
    end tell
end tell

delay 1

tell application "System Events"
    keystroke return
end tell