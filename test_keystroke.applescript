#!/usr/bin/osascript

-- 간단한 테스트: Terminal에 텍스트 입력
tell application "Terminal"
    activate
    -- 첫 번째 터미널 창 활성화
    tell window 1
        activate
    end tell
    
    delay 1
    
    -- System Events로 실제 키보드 입력
    tell application "System Events"
        keystroke "테스트 메시지: 자동 입력됩니다"
        delay 0.5
        key code 36 -- Enter 키
    end tell
end tell

display notification "테스트 완료!" with title "AI Orchestra"