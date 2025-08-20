#!/usr/bin/osascript

-- 각 세션의 작업 상태 추적
on run
    tell application "iTerm"
        set report to "🎯 AI Orchestra 팀 작업 현황" & return & "─────────────────────" & return & return
        
        tell current window
            tell current tab
                set sessionCount to count of sessions
                
                repeat with i from 1 to sessionCount
                    tell session i
                        set sessionName to name
                        set sessionID to id
                        
                        set report to report & "📍 세션 " & i & " [" & sessionName & "]" & return
                        
                        -- 현재 디렉토리 확인 (프롬프트에서 추출)
                        try
                            -- 세션의 변수 가져오기
                            set currentDir to (variable named "PWD")'s value
                            set report to report & "   📂 위치: " & currentDir & return
                        on error
                            set report to report & "   📂 위치: 알 수 없음" & return
                        end try
                        
                        -- 실행 중인 프로세스 확인
                        try
                            set processName to (variable named "TERM_PROGRAM")'s value
                            set report to report & "   ⚙️ 프로그램: " & processName & return
                        on error
                            -- 무시
                        end try
                        
                        -- 프롬프트 상태 확인
                        if is at shell prompt then
                            set report to report & "   ✅ 상태: 대기 중 (프롬프트에서 대기)" & return
                        else
                            set report to report & "   🔄 상태: 작업 실행 중" & return
                        end if
                        
                        set report to report & return
                    end tell
                end repeat
                
                -- 특정 세션에서 작업 내용 가져오기 예시
                if sessionCount ≥ 2 then
                    tell session 2
                        -- 세션 2의 히스토리 마지막 명령 확인
                        write text "history | tail -1"
                        delay 0.5
                        set report to report & "📌 세션 2 마지막 명령 확인 중..." & return
                    end tell
                end if
                
            end tell
        end tell
        
        display dialog report buttons {"확인"} default button 1
        
        -- 파일로도 저장
        do shell script "echo " & quoted form of report & " > /tmp/ai_orchestra_status.txt"
        
        return report
    end tell
end run