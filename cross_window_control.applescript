#!/usr/bin/osascript

-- 다른 윈도우의 CLI 제어하기
on run
    tell application "iTerm"
        set windowCount to count of windows
        
        -- 윈도우가 2개 이상 있을 때
        if windowCount ≥ 2 then
            -- 윈도우 2의 첫 번째 탭, 첫 번째 세션 찾기
            tell window 2
                tell tab 1
                    tell session 1
                        write text "# PM Claude가 윈도우 2의 팀원에게 작업 지시"
                        write text "echo '🎯 새로운 작업이 할당되었습니다'"
                        write text ""
                    end tell
                end tell
            end tell
            
            delay 1
            
            -- 윈도우 3이 있다면 거기도
            if windowCount ≥ 3 then
                tell window 3
                    tell tab 1
                        tell session 1
                            write text "# 윈도우 3의 다른 팀원에게도 메시지"
                            write text "echo '📋 협업 요청이 도착했습니다'"
                            write text ""
                        end tell
                    end tell
                end tell
            end if
            
            -- 원래 윈도우로 돌아오기
            tell window 1
                activate
                tell tab 1
                    tell session 1
                        write text "echo '✅ 모든 팀원에게 메시지 전송 완료'"
                    end tell
                end tell
            end tell
        else
            display dialog "여러 윈도우를 먼저 열어주세요" buttons {"OK"}
        end if
    end tell
end run