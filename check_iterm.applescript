#!/usr/bin/osascript

-- iTerm2 구조 확인 스크립트
tell application "iTerm"
    activate
    
    -- 윈도우 개수 확인
    set windowCount to count of windows
    display dialog "윈도우 개수: " & windowCount
    
    if windowCount > 0 then
        tell window 1
            -- 탭 개수 확인
            set tabCount to count of tabs
            display dialog "윈도우 1의 탭 개수: " & tabCount
            
            -- 각 탭의 세션 확인
            repeat with i from 1 to tabCount
                tell tab i
                    set sessionCount to count of sessions
                    display dialog "탭 " & i & "의 세션 개수: " & sessionCount
                end tell
            end repeat
        end tell
    end if
end tell