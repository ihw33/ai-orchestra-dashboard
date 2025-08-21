#!/usr/bin/osascript

-- PM Claude가 팀원들의 작업 상황을 깊이 파악하기
on run
    tell application "iTerm"
        -- 각 세션에 작업 상태 요청 보내기
        tell current window
            tell current tab
                
                -- 세션 2 (다른 Claude)에게 상태 물어보기
                if (count of sessions) ≥ 2 then
                    tell session 2
                        write text "# PM이 묻습니다: 현재 무슨 작업 중인가요?"
                        write text ""
                        delay 2
                    end tell
                end if
                
                -- 세션 3 (Gemini/Codex)에게도 물어보기  
                if (count of sessions) ≥ 3 then
                    tell session 3
                        write text "# PM 요청: 진행 상황을 알려주세요"
                        write text ""
                        delay 2
                    end tell
                end if
                
                -- 세션 4에게도
                if (count of sessions) ≥ 4 then
                    tell session 4
                        write text "pwd && git status"
                        write text ""
                        delay 1
                    end tell
                end if
                
                -- PM 세션으로 돌아와서 결과 수집
                tell session 1
                    write text "echo '📊 팀 상태 점검 완료. 각 팀원의 응답을 확인하세요.'"
                    write text ""
                end tell
                
            end tell
        end tell
        
        display notification "모든 팀원에게 상태 요청 전송됨" with title "AI Orchestra PM"
    end tell
end run