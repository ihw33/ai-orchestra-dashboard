#!/usr/bin/osascript

-- AI Orchestra PM Master Control
-- PM Claude가 실행할 통합 제어 스크립트

on run argv
    -- 명령어 파싱
    if (count of argv) = 0 then
        return showHelp()
    end if
    
    set command to item 1 of argv
    
    if command = "status" then
        return checkAllStatus()
    else if command = "assign" then
        if (count of argv) ≥ 3 then
            set target to item 2 of argv
            set task to item 3 of argv
            return assignTask(target, task)
        else
            return "Usage: pm_master_control.applescript assign [gemini|codex|claude2] 'task'"
        end if
    else if command = "monitor" then
        return monitorAll()
    else if command = "web" then
        return controlWeb()
    else
        return showHelp()
    end if
end run

-- 도움말 표시
on showHelp()
    set help to "🎯 AI Orchestra PM Control" & return
    set help to help & "Commands:" & return
    set help to help & "  status  - 모든 팀원 상태 확인" & return
    set help to help & "  assign [target] [task] - 작업 할당" & return
    set help to help & "  monitor - 실시간 모니터링" & return
    set help to help & "  web - 웹 브라우저 제어" & return
    return help
end showHelp

-- 모든 CLI 상태 확인
on checkAllStatus()
    tell application "iTerm"
        tell current window
            tell current tab
                set status to "📊 Team Status Report" & return
                set status to status & "─────────────────────" & return
                
                set sessionCount to count of sessions
                repeat with i from 1 to sessionCount
                    tell session i
                        set sessionName to name
                        set isReady to is at shell prompt
                        
                        if isReady then
                            set statusIcon to "✅"
                        else
                            set statusIcon to "🔄"
                        end if
                        
                        set status to status & statusIcon & " Session " & i & ": " & sessionName & return
                    end tell
                end repeat
                
                return status
            end tell
        end tell
    end tell
end checkAllStatus

-- 작업 할당
on assignTask(target, taskMessage)
    tell application "iTerm"
        tell current window
            tell current tab
                -- 타겟 세션 찾기
                set targetSession to 0
                
                if target = "gemini" then
                    set targetSession to 2
                else if target = "codex" then
                    set targetSession to 3
                else if target = "claude2" then
                    set targetSession to 4
                end if
                
                if targetSession > 0 and targetSession ≤ (count of sessions) then
                    tell session targetSession
                        write text "# 📋 새로운 작업 할당: " & taskMessage
                        write text ""
                    end tell
                    return "✅ " & target & "에게 작업 할당 완료"
                else
                    return "❌ 타겟을 찾을 수 없음: " & target
                end if
            end tell
        end tell
    end tell
end assignTask

-- 전체 모니터링
on monitorAll()
    set report to "🎭 AI Orchestra Dashboard" & return
    set report to report & "Time: " & (current date) as string & return
    set report to report & "════════════════════════" & return & return
    
    -- iTerm 세션 체크
    tell application "iTerm"
        tell current window
            tell current tab
                set report to report & "【 CLI Team Status 】" & return
                repeat with i from 1 to count of sessions
                    tell session i
                        set sessionName to name
                        set isReady to is at shell prompt
                        if isReady then
                            set report to report & "  ✅ " & sessionName & " - Ready" & return
                        else
                            set report to report & "  🔄 " & sessionName & " - Working" & return
                        end if
                    end tell
                end repeat
            end tell
        end tell
    end tell
    
    set report to report & return
    
    -- Chrome 탭 체크
    tell application "Google Chrome"
        if (count of windows) > 0 then
            tell window 1
                set report to report & "【 Web Resources 】" & return
                set tabCount to count of tabs
                set report to report & "  Chrome: " & tabCount & " tabs open" & return
                
                repeat with t from 1 to tabCount
                    if t > 3 then exit repeat
                    tell tab t
                        set tabURL to URL
                        if tabURL contains "github" then
                            set report to report & "    🔧 GitHub" & return
                        else if tabURL contains "claude" then
                            set report to report & "    🤖 Claude" & return
                        else if tabURL contains "chatgpt" then
                            set report to report & "    💬 ChatGPT" & return
                        end if
                    end tell
                end repeat
            end tell
        end if
    end tell
    
    return report
end monitorAll

-- 웹 브라우저 제어
on controlWeb()
    tell application "Google Chrome"
        tell window 1
            -- GitHub로 전환
            repeat with t from 1 to count of tabs
                tell tab t
                    if URL contains "github" then
                        set active tab index to t
                        reload
                        return "🔧 GitHub 탭 새로고침 완료"
                    end if
                end tell
            end repeat
        end tell
    end tell
    return "웹 제어 완료"
end controlWeb