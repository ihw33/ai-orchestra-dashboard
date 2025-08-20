#!/usr/bin/osascript

-- iTerm2 윈도우 단위로 테스트 (탭이 아닌 윈도우)
on run
    tell application "iTerm"
        activate
        
        -- 열려있는 윈도우 수 확인
        set windowList to windows
        set windowCount to count of windowList
        
        if windowCount < 3 then
            -- 현재 윈도우에서 세션으로 시도
            tell current window
                tell current session
                    write text "# 테스트: 현재 세션에 직접 텍스트 입력"
                    write text "print('이 메시지가 보이면 성공!')"
                end tell
            end tell
            
            display notification "현재 세션에 메시지 전송" with title "테스트"
        else
            -- 윈도우 2로 전송
            tell window 2
                tell current session
                    write text "# PM으로부터 자동 메시지"
                    write text "print('📥 Gemini: Issue #3 작업 시작')"
                end tell
            end tell
            
            delay 1
            
            -- 윈도우 3으로 전송
            tell window 3
                tell current session
                    write text "# PM으로부터 자동 메시지"
                    write text "print('📥 Codex: Issue #2 작업 시작')"
                end tell
            end tell
            
            display notification "✅ 메시지 전송 완료!" with title "성공"
        end if
    end tell
end run