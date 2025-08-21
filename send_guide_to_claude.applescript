tell application "iTerm"
    tell window 1
        tell tab 4
            select
            tell session 1
                select
                write text "당신은 Orchestra Dashboard 팀의 Frontend 개발자입니다. 프로젝트 경로: /Users/m4_macbook/Projects/ai-orchestra-dashboard, GitHub: ihw33/ai-orchestra-dashboard, 담당 Issue: #6. GitHub CLI(gh)로 Issue 댓글 작성이 필수입니다. 먼저 gh issue view 6 -R ihw33/ai-orchestra-dashboard 명령으로 Issue를 확인하세요."
            end tell
        end tell
    end tell
end tell

delay 1

tell application "System Events"
    key code 36
end tell