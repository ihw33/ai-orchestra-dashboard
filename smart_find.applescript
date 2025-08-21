#!/usr/bin/osascript

-- 더 똑똑하게 찾는 방법: 세션 이름으로 찾기
on run
    tell application "iTerm"
        tell current window
            tell current tab
                set targetFound to false
                set sessionCount to count of sessions
                
                repeat with i from 1 to sessionCount
                    tell session i
                        set sessionName to name
                        
                        -- 세션 이름에 'claude'가 포함되어 있으면
                        if sessionName contains "claude" and i ≠ 1 then
                            write text "# 다른 Claude를 찾았습니다!"
                            write text "2 + 2는 뭐야?"
                            write text ""
                            set targetFound to true
                            exit repeat
                        end if
                        
                        -- 또는 프롬프트 텍스트로 찾기
                        set sessionText to text
                        if sessionText contains "Claude" and i ≠ 1 then
                            write text "# Claude 프롬프트 발견!"
                            write text "3 + 3은?"
                            write text ""
                            set targetFound to true
                            exit repeat
                        end if
                    end tell
                end repeat
                
                if not targetFound then
                    display dialog "다른 Claude 세션을 찾을 수 없습니다"
                end if
            end tell
        end tell
    end tell
end run