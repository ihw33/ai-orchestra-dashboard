#!/usr/bin/osascript

-- 각 AI의 특성에 맞춰 작업 전송 및 확인
-- 사용법: osascript smart_task_sender.applescript <tab_number> <cli_name> <task>

on run argv
    if (count of argv) < 3 then
        return "사용법: osascript smart_task_sender.applescript <tab_number> <cli_name> <task>"
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
                        write text "# 🚀 [" & timestamp & "] " & cliName & "님께 새로운 작업 요청"
                        write text ""
                        write text taskDescription
                        write text "" -- 엔터
                        
                        -- AI별 대기 시간 설정
                        if cliName = "Codex" then
                            -- Codex는 답변이 길어서 더 오래 대기
                            delay 5
                            write text "" -- 엔터 (답변 중간에 끊을 수도 있음)
                            delay 3
                            write text "1" -- bash command 확인
                            write text "" -- 엔터
                            
                        else if cliName = "Gemini" then
                            -- Gemini는 보통 속도
                            delay 3
                            write text "1"
                            write text "" -- 엔터
                            
                        else if cliName contains "PM" then
                            -- PM Claude는 빠른 응답
                            delay 2
                            write text "1"
                            write text "" -- 엔터
                            
                        else
                            -- 기본 설정
                            delay 3
                            write text "1"
                            write text "" -- 엔터
                        end if
                        
                        -- 추가 확인 대기
                        delay 1
                        
                    end tell
                end tell
            else
                return "오류: Tab " & tabNum & "이 존재하지 않습니다"
            end if
            
        end tell
    end tell
    
    return cliName & " (Tab " & tabNum & ")에 작업 전송 완료 - " & cliName & " 특성에 맞춰 대기"
end run