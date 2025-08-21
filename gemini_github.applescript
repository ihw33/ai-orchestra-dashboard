tell application "iTerm"
    tell window 1
        tell tab 4
            select
            tell session 2
                select
                write text "gh issue view 5 -R ihw33/ai-orchestra-dashboard"
            end tell
        end tell
    end tell
end tell

delay 1

tell application "System Events"
    key code 36
end tell