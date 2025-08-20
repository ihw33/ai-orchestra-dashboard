#!/usr/bin/osascript

-- iTerm2용 PM → Gemini/Codex 메시지 전송 테스트
on run
    tell application "iTerm"
        activate
        
        -- 현재 윈도우의 탭들 확인
        tell current window
            set tabCount to count of tabs
            
            if tabCount < 3 then
                display dialog "iTerm2에 최소 3개 탭 필요 (PM, Gemini, Codex)" buttons {"OK"}
                return
            end if
            
            display notification "iTerm2 자동화 테스트 시작" with title "AI Orchestra"
            
            -- 탭 2 (Gemini)로 메시지 전송
            tell tab 2
                select
            end tell
            
            delay 1
            
            tell application "System Events"
                keystroke "# PM Claude로부터 자동 메시지:"
                key code 36 -- Enter
                delay 0.5
                keystroke "print('📥 Issue #3 사용자 가이드 작성을 시작해주세요')"
                key code 36 -- Enter
            end tell
            
            delay 2
            
            -- 탭 3 (Codex)로 메시지 전송
            tell tab 3
                select
            end tell
            
            delay 1
            
            tell application "System Events"
                keystroke "# PM Claude로부터 자동 메시지:"
                key code 36 -- Enter
                delay 0.5
                keystroke "print('📥 Issue #2 API 최적화를 진행해주세요')"
                key code 36 -- Enter
            end tell
            
            delay 2
            
            -- 탭 1 (PM)으로 돌아가기
            tell tab 1
                select
            end tell
            
            display notification "✅ 모든 메시지 전송 완료!" with title "AI Orchestra"
        end tell
    end tell
end run