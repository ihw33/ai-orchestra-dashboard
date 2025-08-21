#!/usr/bin/osascript

-- 모든 세션의 현재 상태 모니터링
on run
    tell application "iTerm"
        set statusReport to "📊 AI 팀 현재 상태 리포트" & return & return
        set timestamp to (current date) as string
        set statusReport to statusReport & "🕐 " & timestamp & return & return
        
        -- 모든 윈도우 탐색
        repeat with w from 1 to count of windows
            tell window w
                set statusReport to statusReport & "━━━━━━━━━━━━━━━━━━━━" & return
                set statusReport to statusReport & "📦 윈도우 " & w & return
                
                repeat with t from 1 to count of tabs
                    tell tab t
                        repeat with s from 1 to count of sessions
                            tell session s
                                set sessionName to name
                                set sessionText to text
                                set isAtPrompt to is at shell prompt
                                
                                set statusReport to statusReport & return & "  💻 세션 " & s & " (" & sessionName & ")" & return
                                
                                -- 쉘 프롬프트 상태
                                if isAtPrompt then
                                    set statusReport to statusReport & "  ⏸️  상태: 대기 중" & return
                                else
                                    set statusReport to statusReport & "  ⚡ 상태: 작업 실행 중" & return
                                end if
                                
                                -- 마지막 몇 줄 가져오기 (현재 작업 파악)
                                set textLines to paragraphs of sessionText
                                set lineCount to count of textLines
                                
                                if lineCount > 0 then
                                    set statusReport to statusReport & "  📝 최근 활동:" & return
                                    
                                    -- 마지막 5줄 표시
                                    set startLine to lineCount - 4
                                    if startLine < 1 then set startLine to 1
                                    
                                    repeat with i from startLine to lineCount
                                        if i ≤ (count of textLines) then
                                            set currentLine to item i of textLines
                                            -- 긴 줄은 잘라서 표시
                                            if length of currentLine > 50 then
                                                set currentLine to (text 1 thru 50 of currentLine) & "..."
                                            end if
                                            set statusReport to statusReport & "      " & currentLine & return
                                        end if
                                    end repeat
                                end if
                                
                                set statusReport to statusReport & return
                            end tell
                        end repeat
                    end tell
                end repeat
            end tell
        end repeat
        
        -- 결과를 파일로 저장
        set reportFile to "/tmp/ai_team_status.txt"
        do shell script "echo " & quoted form of statusReport & " > " & reportFile
        
        -- 알림 표시
        display notification "상태 리포트가 생성되었습니다" with title "AI Orchestra Monitor"
        
        -- 리포트 내용 반환
        return statusReport
    end tell
end run