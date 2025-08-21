#!/usr/bin/osascript

-- iTerm2 분할 패널(Split Panes)용 테스트
on run
    tell application "iTerm"
        activate
        
        tell current window
            tell current tab
                -- 세션(패널) 개수 확인
                set sessionCount to count of sessions
                
                if sessionCount < 3 then
                    display dialog "분할 패널이 3개 이상 필요합니다. 현재: " & sessionCount buttons {"OK"}
                    return
                end if
                
                display notification "분할 패널 자동화 테스트 시작" with title "AI Orchestra"
                
                -- 세션 1 (PM Claude)
                tell session 1
                    write text "# PM Claude 준비 완료"
                end tell
                
                delay 1
                
                -- 세션 2 (Gemini)에 메시지 전송
                tell session 2
                    write text "# PM Claude로부터 자동 메시지:"
                    write text "print('📥 Gemini: Issue #3 사용자 가이드 작성을 시작해주세요')"
                end tell
                
                delay 1
                
                -- 세션 3 (Codex)에 메시지 전송
                tell session 3
                    write text "# PM Claude로부터 자동 메시지:"
                    write text "print('📥 Codex: Issue #2 API 최적화를 진행해주세요')"
                end tell
                
                delay 1
                
                -- 세션 4가 있다면 추가 메시지
                if sessionCount ≥ 4 then
                    tell session 4
                        write text "# PM Claude로부터 자동 메시지:"
                        write text "print('📥 추가 작업: 테스트 자동화 성공!')"
                    end tell
                end if
                
                display notification "✅ 모든 분할 패널에 메시지 전송 완료!" with title "AI Orchestra"
            end tell
        end tell
    end tell
end run