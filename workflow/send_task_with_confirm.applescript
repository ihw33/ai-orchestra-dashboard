#!/usr/bin/osascript

-- 작업 전송 후 자동으로 bash command 확인
-- 사용법: osascript send_task_with_confirm.applescript <tab_number> <cli_name> <task>

on run argv
    if (count of argv) < 3 then
        return "사용법: osascript send_task_with_confirm.applescript <tab_number> <cli_name> <task>"
    end if
    
    set tabNum to item 1 of argv as integer
    set cliName to item 2 of argv
    set taskDescription to item 3 of argv
    set timestamp to do shell script "date '+%H:%M:%S'"
    
    tell application "iTerm"
        tell current window
            
            if (count of tabs) ≥ tabNum then
                tell tab tabNum
                    tell session 1
                        -- 작업 프롬프트 전송
                        write text "# 🚀 [" & timestamp & "] 새로운 작업"
                        write text ""
                        write text taskDescription
                        write text "" -- 엔터
                        
                        -- bash command 창이 뜰 때까지 대기
                        delay 2
                        
                        -- 자동으로 1 입력하고 엔터
                        write text "1"
                        write text "" -- 엔터
                        
                        -- 추가 확인이 필요한 경우를 위해
                        delay 1
                        write text "" -- 한 번 더 엔터
                    end tell
                end tell
            else
                return "오류: Tab " & tabNum & "이 존재하지 않습니다"
            end if
            
        end tell
    end tell
    
    return cliName & " (Tab " & tabNum & ")에 작업 전송 및 자동 확인 완료"
end run