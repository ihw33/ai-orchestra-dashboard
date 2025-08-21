on run argv
    -- 사용법: osascript onboard_new_member.applescript [session_number] [member_name] [role]
    
    set sessionNum to item 1 of argv
    set memberName to item 2 of argv
    set memberRole to item 3 of argv
    
    tell application "iTerm"
        activate
        tell window 1
            tell tab 4
                select
                tell session sessionNum
                    select
                    
                    -- 1. 환영 메시지
                    write text "안녕하세요 " & memberName & "님! AI Orchestra Dashboard 팀에 오신 것을 환영합니다."
                end tell
            end tell
        end tell
    end tell
    
    delay 1
    
    tell application "System Events"
        tell process "iTerm2"
            keystroke return
        end tell
    end tell
    
    delay 1
    
    -- 2. 프로젝트 정보
    tell application "iTerm"
        tell window 1
            tell tab 4
                tell session sessionNum
                    write text "📁 프로젝트: /Users/m4_macbook/Projects/ai-orchestra-dashboard"
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
    
    delay 1
    
    -- 3. GitHub 정보
    tell application "iTerm"
        tell window 1
            tell tab 4
                tell session sessionNum
                    write text "🔗 GitHub: ihw33/ai-orchestra-dashboard"
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
    
    delay 1
    
    -- 4. 역할 정보
    tell application "iTerm"
        tell window 1
            tell tab 4
                tell session sessionNum
                    write text "👤 당신의 역할: " & memberRole
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
    
    delay 1
    
    -- 5. 가이드 확인 지시
    tell application "iTerm"
        tell window 1
            tell tab 4
                tell session sessionNum
                    write text "📚 필독: cat /Users/m4_macbook/Projects/ai-orchestra-dashboard/TEAM_MEMBER_GUIDE.md 명령으로 팀원 가이드를 숙지하세요"
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
    
    delay 1
    
    -- 6. 첫 작업 지시
    tell application "iTerm"
        tell window 1
            tell tab 4
                tell session sessionNum
                    write text "시작하려면: 1) cd /Users/m4_macbook/Projects/ai-orchestra-dashboard 2) gh auth status 3) gh issue list -R ihw33/ai-orchestra-dashboard"
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
    
end run