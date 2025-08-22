#!/usr/bin/osascript
(*
Allow 요청 모니터링 테스트
iTerm2 세션에서 "Allow?" 감지하고 PM에게 알림
*)

on run
    log "🔍 Allow 요청 모니터링 테스트 시작..."
    
    -- 테스트 1: 현재 세션 텍스트 읽기
    tell application "iTerm2"
        tell current session of current window
            -- 세션 내용 가져오기
            set sessionText to contents
            
            -- Allow 요청 감지
            if sessionText contains "Allow?" then
                log "⚠️ Allow 요청 감지!"
                
                -- 명령어 추출 시도
                set commandLine to "테스트 명령어"
                
                -- PM Claude에게 알림 메시지 생성
                set alertMessage to "[ALLOW_REQUEST]" & return & ¬
                    "FROM: Test CLI" & return & ¬
                    "COMMAND: " & commandLine & return & ¬
                    "RISK_LEVEL: MEDIUM" & return & ¬
                    "SUGGESTED_ACTION: 3" & return & ¬
                    "[/ALLOW_REQUEST]"
                
                log "📤 PM에게 전송할 메시지:"
                log alertMessage
                
                -- 테스트 응답 (실제로는 PM이 판단)
                delay 2
                log "📥 테스트 응답: 1 (승인)"
                
                -- Allow 응답 입력 (테스트)
                -- write text "1"
                
                return "✅ Allow 요청 처리 완료"
            else
                log "ℹ️ Allow 요청 없음"
                return "대기 중..."
            end if
        end tell
    end tell
end run