#!/usr/bin/osascript

-- AI 응답을 모니터링하고 적절한 시점에 확인
-- 사용법: osascript monitor_and_confirm.applescript <tab_number> <cli_name>

on run argv
    if (count of argv) < 2 then
        return "사용법: osascript monitor_and_confirm.applescript <tab_number> <cli_name>"
    end if
    
    set tabNum to item 1 of argv as integer
    set cliName to item 2 of argv
    set maxWait to 10 -- 최대 대기 시간 (초)
    set checkInterval to 2 -- 체크 간격 (초)
    set waited to 0
    
    tell application "iTerm"
        tell current window
            
            if (count of tabs) ≥ tabNum then
                tell tab tabNum
                    tell session 1
                        
                        repeat while waited < maxWait
                            delay checkInterval
                            set waited to waited + checkInterval
                            
                            -- 상태 체크 (실제로는 더 복잡한 로직 필요)
                            -- 여기서는 단순히 시간 기반으로 처리
                            
                            if cliName = "Codex" and waited >= 6 then
                                -- Codex는 6초 후 확인
                                write text "1"
                                write text "" -- 엔터
                                exit repeat
                                
                            else if cliName = "Gemini" and waited >= 4 then
                                -- Gemini는 4초 후 확인
                                write text "1"
                                write text "" -- 엔터
                                exit repeat
                                
                            else if cliName contains "PM" and waited >= 2 then
                                -- PM은 2초 후 확인
                                write text "1"
                                write text "" -- 엔터
                                exit repeat
                            end if
                        end repeat
                        
                        -- 타임아웃 시에도 한 번 시도
                        if waited >= maxWait then
                            write text "1"
                            write text "" -- 엔터
                        end if
                        
                    end tell
                end tell
            else
                return "오류: Tab " & tabNum & "이 존재하지 않습니다"
            end if
            
        end tell
    end tell
    
    return cliName & " 응답 모니터링 및 확인 완료 (대기 시간: " & waited & "초)"
end run