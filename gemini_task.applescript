tell application "iTerm"
    tell window 1
        tell tab 4
            select
            tell session 2
                select
                write text "cd /Users/m4_macbook/Projects/ai-orchestra-dashboard"
            end tell
        end tell
    end tell
end tell

delay 1

tell application "System Events"
    key code 36
end tell