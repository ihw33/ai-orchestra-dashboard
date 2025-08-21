#!/usr/bin/osascript

-- AppleScript가 어떻게 찾는지 보여주는 스크립트
on run
    tell application "iTerm"
        tell current window
            tell current tab
                -- 모든 세션 정보 수집
                set sessionCount to count of sessions
                set sessionInfo to "🔍 세션 탐색 결과:\n"
                
                repeat with i from 1 to sessionCount
                    tell session i
                        -- 각 세션의 정보 가져오기
                        set sessionName to name
                        set sessionID to id
                        set isAtShell to is at shell prompt
                        
                        set sessionInfo to sessionInfo & "세션 " & i & ":\n"
                        set sessionInfo to sessionInfo & "  - 이름: " & sessionName & "\n"
                        set sessionInfo to sessionInfo & "  - ID: " & sessionID & "\n"
                        set sessionInfo to sessionInfo & "  - 쉘 프롬프트: " & isAtShell & "\n\n"
                    end tell
                end repeat
                
                display dialog sessionInfo buttons {"OK"} default button 1
                
                -- 실제로는 이렇게 간단히 접근
                -- session 1 = 첫 번째 분할 패널
                -- session 2 = 두 번째 분할 패널
                -- session 3 = 세 번째 분할 패널
                -- session 4 = 네 번째 분할 패널
                
                -- 순서는 분할한 순서대로!
            end tell
        end tell
    end tell
end run