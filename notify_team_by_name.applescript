on run argv
    set sessionName to item 1 of argv
    set memberName to item 2 of argv
    set issueNumbers to item 3 of argv
    
    tell application "iTerm"
        activate
        tell window 1
            tell tab 4
                select
                set targetSession to ""
                repeat with s in sessions
                    if name of s contains sessionName then
                        set targetSession to s
                        exit repeat
                    end if
                end repeat
                
                if targetSession is not "" then
                    tell targetSession
                        select
                        write text "📢 AI Orchestra Dashboard 프로젝트 초기 설정"
                        write text ""
                        write text "프로젝트 경로: /Users/m4_macbook/Projects/ai-orchestra-dashboard"
                        write text "GitHub: https://github.com/ihw33/ai-orchestra-dashboard"
                        write text ""
                        write text "🏁 Round 1이 시작되었습니다!"
                        write text "담당 Issues: " & issueNumbers
                        write text ""
                        write text "작업 시작 전 필독:"
                        write text "cat /Users/m4_macbook/Projects/ai-orchestra-dashboard/TEAM_MEMBER_GUIDE.md"
                        write text ""
                        write text "Issue 확인:"
                        write text "gh issue list -R ihw33/ai-orchestra-dashboard --label " & memberName
                    end tell
                end if
            end tell
        end tell
    end tell
    
    delay 0.5
    
    tell application "System Events"
        tell process "iTerm2"
            keystroke return
        end tell
    end tell
end run