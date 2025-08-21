tell application "iTerm"
    tell session 3 of tab 4 of current window
        write text "gh issue comment 5 -R ihw33/iwl-v5-rebuild --body '[Gemini 보고] ⚙️ Data Collection 서비스 구현 중. GitHub API 연동 완료. 진행률: 50%'"
    end tell
end tell
tell application "System Events"
    keystroke return
end tell