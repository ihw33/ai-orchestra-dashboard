#!/usr/bin/osascript

-- 여러 터미널 창 테스트
on run
    -- Terminal 앱 활성화
    tell application "Terminal"
        activate
        
        -- 열려있는 창 개수 확인
        set windowCount to count of windows
        
        if windowCount < 2 then
            display dialog "최소 2개의 터미널 창이 필요합니다!" buttons {"OK"} default button 1
            return
        end if
        
        -- 창 1에서 창 2로 메시지 전송 시뮬레이션
        display notification "창 1 → 창 2 메시지 전송 테스트" with title "AI Orchestra"
        
        -- 창 2로 전환
        tell window 2
            activate
        end tell
        
        delay 1
        
        -- 창 2에 메시지 입력
        tell application "System Events"
            keystroke "📥 PM으로부터 받은 메시지: Issue #3 작업 시작하세요"
            delay 0.5
            key code 36 -- Enter
        end tell
        
        delay 1
        
        -- 창 1로 돌아가기
        tell window 1
            activate
        end tell
        
        display notification "테스트 성공! 창 2를 확인하세요" with title "AI Orchestra"
    end tell
end run