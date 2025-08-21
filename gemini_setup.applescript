tell application "iTerm"
    activate
    tell window 1
        tell tab 4
            select
            tell session 2
                select
                write text "안녕하세요 Gemini님! 당신의 정보입니다. 프로젝트: /Users/m4_macbook/Projects/ai-orchestra-dashboard, GitHub: ihw33/ai-orchestra-dashboard, 역할: Data Collection 담당, 이름: Gemini, GitHub CLI(gh) 사용 가능. Issue #10을 확인하고 댓글을 남겨주세요: gh issue view 10 -R ihw33/ai-orchestra-dashboard"
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