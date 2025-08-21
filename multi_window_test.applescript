#!/usr/bin/osascript

-- 여러 윈도우에서 Claude 찾기
on run
    tell application "iTerm"
        activate
        
        -- 모든 윈도우 탐색
        set windowCount to count of windows
        display notification "윈도우 개수: " & windowCount with title "탐색 시작"
        
        -- 각 윈도우 확인
        repeat with w from 1 to windowCount
            tell window w
                set tabCount to count of tabs
                
                -- 각 탭 확인
                repeat with t from 1 to tabCount
                    tell tab t
                        set sessionCount to count of sessions
                        
                        -- 각 세션 확인
                        repeat with s from 1 to sessionCount
                            tell session s
                                -- 윈도우 2, 탭 1, 세션 1에 메시지 전송
                                if w = 2 and t = 1 and s = 1 then
                                    write text "# 다른 윈도우의 Claude를 찾았습니다!"
                                    write text "윈도우 " & w & ", 탭 " & t & ", 세션 " & s & "에서 5+5는?"
                                    write text ""
                                    
                                    display notification "윈도우 2에 메시지 전송!" with title "성공"
                                end if
                            end tell
                        end repeat
                    end tell
                end repeat
            end tell
        end repeat
    end tell
end run