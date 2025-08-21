tell application "iTerm"
    activate
    tell window 1
        tell tab 4
            select
            tell session 2
                select
                write text "Issue #11이 할당되었습니다. 확인해주세요: gh issue view 11 -R ihw33/ai-orchestra-dashboard"
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