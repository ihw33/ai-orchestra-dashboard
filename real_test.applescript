#!/usr/bin/osascript

-- 실제 PM → Gemini 메시지 전송 테스트
on run
    tell application "Terminal"
        activate
        
        -- 창 개수 확인
        set windowCount to count of windows
        if windowCount < 3 then
            display dialog "3개 터미널 필요 (PM, Gemini, Codex)" buttons {"OK"}
            return
        end if
        
        -- PM Claude 역할 (창 1)
        tell window 1
            activate
        end tell
        
        display notification "PM Claude가 메시지 전송 준비" with title "테스트 시작"
        delay 2
        
        -- Gemini에게 메시지 전송 (창 2)
        tell window 2
            activate
        end tell
        
        tell application "System Events"
            -- 실제로 Gemini CLI가 받을 메시지
            keystroke "print('PM Claude로부터: Issue #3 사용자 가이드 작성을 시작해주세요')"
            delay 0.5
            key code 36 -- Enter
        end tell
        
        delay 2
        
        -- Codex에게 메시지 전송 (창 3)
        tell window 3
            activate
        end tell
        
        tell application "System Events"
            keystroke "print('PM Claude로부터: Issue #2 API 최적화를 진행해주세요')"
            delay 0.5
            key code 36 -- Enter
        end tell
        
        delay 1
        
        -- PM 창으로 돌아가기
        tell window 1
            activate
        end tell
        
        display notification "✅ 모든 메시지 전송 완료!" with title "AI Orchestra"
    end tell
end run