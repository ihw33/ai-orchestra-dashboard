tell application "iTerm"
    tell window 1
        tell tab 4
            select
            tell session 2
                select
                write text "/chat 안녕하세요 Gemini님, 작업 준비되셨나요?"
            end tell
        end tell
    end tell
end tell

delay 1

tell application "System Events"
    key code 36
end tell