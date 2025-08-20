#!/usr/bin/osascript

-- AI CLI의 bash command 자동 확인 헬퍼
-- 사용법: osascript auto_confirm.applescript <tab_number>

on run argv
    if (count of argv) < 1 then
        return "사용법: osascript auto_confirm.applescript <tab_number>"
    end if
    
    set tabNum to item 1 of argv as integer
    
    tell application "iTerm"
        tell current window
            if (count of tabs) ≥ tabNum then
                tell tab tabNum
                    tell session 1
                        -- 1초 대기 후 1 입력하고 엔터
                        delay 1
                        write text "1"
                        write text "" -- 엔터
                    end tell
                end tell
            end if
        end tell
    end tell
    
    return "Tab " & tabNum & " 자동 확인 완료"
end run