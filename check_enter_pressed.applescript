#!/usr/bin/osascript
(*
엔터키가 제대로 눌렸는지 확인
메시지 전송 후 상태 변화 감지
*)

on checkEnterPressed(sessionID, testMessage)
    tell application "iTerm2"
        tell current window
            -- 세션 찾기
            repeat with aTab in tabs
                repeat with aSession in sessions of aTab
                    if name of aSession is sessionID then
                        tell aSession
                            -- 1. 전송 전 상태
                            set beforePrompt to is at shell prompt
                            set beforeProcessing to is processing
                            
                            -- 2. 메시지 전송
                            write text testMessage
                            
                            -- 3. 잠시 대기
                            delay 0.5
                            
                            -- 4. 전송 후 상태
                            set afterPrompt to is at shell prompt
                            set afterProcessing to is processing
                            
                            -- 5. 결과 판단
                            if (beforePrompt and not afterPrompt) or afterProcessing then
                                return "✅ 엔터 성공 - 명령 실행 중"
                            else if afterPrompt and not beforePrompt then
                                return "✅ 엔터 성공 - 명령 완료"
                            else if beforePrompt and afterPrompt then
                                return "⚠️ 엔터 미전송 - 프롬프트 대기 중"
                            else
                                return "❓ 상태 불명확"
                            end if
                        end tell
                        return
                    end if
                end repeat
            end repeat
        end tell
    end tell
    return "❌ 세션을 찾을 수 없음: " & sessionID
end checkEnterPressed

-- 테스트
on run
    set result to checkEnterPressed("ORCH_TERMINAL", "echo 'test'")
    log result
    return result
end run