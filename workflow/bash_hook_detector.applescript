#!/usr/bin/osascript

-- Bash Command Hook Detector
-- iTerm2 세션을 모니터링하고 특정 패턴 감지 시 알림

on run
    set checkInterval to 3 -- 3초마다 체크
    set sessions to {2, 3, 4} -- PM Claude, Gemini, Codex
    set sessionNames to {"PM_Claude", "Gemini", "Codex"}
    
    repeat
        repeat with i from 1 to count of sessions
            set sessionNum to item i of sessions
            set sessionName to item i of sessionNames
            
            try
                tell application "iTerm"
                    tell window 1
                        tell current tab
                            if (count of sessions of current tab) ≥ sessionNum then
                                tell session sessionNum
                                    -- 세션 내용 확인 (제한적)
                                    -- 실제로는 세션의 프롬프트 상태를 직접 확인하기 어려움
                                    
                                    -- 대신 주기적으로 Enter를 보내서 반응 확인
                                    -- 또는 특정 시간 간격으로 자동 응답
                                end tell
                            end if
                        end tell
                    end tell
                end tell
                
                -- 감지되면 알림
                if checkForBashCommand(sessionNum) then
                    displayNotification(sessionName, "Bash command detected!")
                    
                    -- 자동 응답 옵션
                    if autoRespond then
                        sendAutoResponse(sessionNum)
                    end if
                end if
                
            on error errMsg
                -- 에러 무시
            end try
        end repeat
        
        delay checkInterval
    end repeat
end run

-- Bash command 감지 함수 (시뮬레이션)
on checkForBashCommand(sessionNum)
    -- 실제 구현에서는 세션 상태를 확인
    return false
end checkForBashCommand

-- 알림 표시
on displayNotification(sessionName, message)
    display notification message with title "AI Orchestra" subtitle sessionName
end displayNotification

-- 자동 응답 전송
on sendAutoResponse(sessionNum)
    tell application "iTerm"
        tell window 1
            tell current tab
                tell session sessionNum
                    write text "1"
                    write text "" -- 엔터
                end tell
            end tell
        end tell
    end tell
end sendAutoResponse