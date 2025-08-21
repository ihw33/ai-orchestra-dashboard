tell application "iTerm"
    tell current window
        tell tab 4
            tell session 1
                write text "반가워요"
            end tell
        end tell
    end tell
end tell

delay 0.5

tell application "System Events"
    keystroke return
end tell