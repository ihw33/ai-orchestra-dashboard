tell application "iTerm"
    tell session 1 of tab 2 of current window
        write text "GitHub Issue #9에 테스트 공지가 있습니다. 확인하세요: https://github.com/ihw33/ai-orchestra-dashboard/issues/9"
    end tell
end tell
tell application "System Events"
    keystroke return
end tell