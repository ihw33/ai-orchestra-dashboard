#!/usr/bin/osascript

-- 모든 iTerm2 윈도우와 세션 매핑
on run
    tell application "iTerm"
        set allInfo to "🗺️ iTerm2 전체 구조:\n\n"
        
        -- 모든 윈도우 순회
        repeat with w from 1 to count of windows
            tell window w
                set allInfo to allInfo & "📦 윈도우 " & w & ":\n"
                
                -- 모든 탭 순회
                repeat with t from 1 to count of tabs
                    tell tab t
                        set allInfo to allInfo & "  📑 탭 " & t & ":\n"
                        
                        -- 모든 세션 순회
                        repeat with s from 1 to count of sessions
                            tell session s
                                set sessionName to name
                                set allInfo to allInfo & "    💻 세션 " & s & ": " & sessionName & "\n"
                                
                                -- 여기서 원하는 세션에 명령 전송 가능!
                                -- 예: window 2, tab 1, session 1
                                if w = 2 and t = 1 and s = 1 then
                                    write text "# 찾았다! 여기가 윈도우 2의 Claude"
                                end if
                            end tell
                        end repeat
                    end tell
                end repeat
                set allInfo to allInfo & "\n"
            end tell
        end repeat
        
        display dialog allInfo buttons {"OK"} default button 1
    end tell
end run