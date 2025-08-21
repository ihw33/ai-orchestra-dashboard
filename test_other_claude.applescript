#!/usr/bin/osascript

-- 다른 Claude Code 탭에 질문 입력 테스트
on run
    tell application "iTerm"
        activate
        
        tell current window
            tell current tab
                -- 세션 수 확인
                set sessionCount to count of sessions
                
                display notification "세션 수: " & sessionCount with title "테스트 시작"
                
                -- 다른 Claude가 있을 세션 선택 (2번 또는 다른 번호)
                -- 현재 세션이 1번이라면 2번에 메시지 전송
                if sessionCount ≥ 2 then
                    tell session 2
                        -- Claude에게 1+1 질문
                        write text "1+1이 뭐야?"
                        delay 0.5
                        write text "" -- Enter 효과
                    end tell
                    
                    display notification "세션 2에 '1+1이 뭐야?' 전송 완료!" with title "성공"
                else
                    display dialog "2개 이상의 세션이 필요합니다"
                end if
            end tell
        end tell
    end tell
end run