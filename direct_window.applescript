#!/usr/bin/osascript

-- 특정 윈도우에 직접 접근
on run
    tell application "iTerm"
        activate
        
        -- 윈도우가 2개 이상 있는지 확인
        if (count of windows) ≥ 2 then
            -- 윈도우 2의 첫 번째 탭, 첫 번째 세션에 메시지
            tell window 2
                tell tab 1
                    tell session 1
                        write text "# 윈도우 2의 Claude입니다"
                        write text "10 + 10은 뭐야?"
                        write text ""
                    end tell
                end tell
            end tell
            
            display notification "윈도우 2에 질문 전송!" with title "성공"
            
            -- 3초 후 윈도우 1로 돌아오기
            delay 3
            
            tell window 1
                activate
            end tell
            
        else
            -- 윈도우가 1개만 있으면 새 윈도우 생성
            create window with default profile
            delay 1
            
            tell window 2
                tell current session
                    write text "# 새 윈도우에서 Claude 실행"
                    write text "claude"
                end tell
            end tell
            
            display notification "새 윈도우 생성 및 Claude 실행!" with title "자동화"
        end if
    end tell
end run