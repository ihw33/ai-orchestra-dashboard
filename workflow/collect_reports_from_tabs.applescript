#!/usr/bin/osascript

-- 각 탭에서 완료 보고 수집
-- Tab 2: PM Claude, Tab 3: Gemini, Tab 4: Codex

on run
    set reports to {}
    set timestamp to do shell script "date '+%Y-%m-%d %H:%M:%S'"
    
    tell application "iTerm"
        tell current window
            
            -- Tab 2: PM Claude 상태 확인
            if (count of tabs) ≥ 2 then
                tell tab 2
                    tell session 1
                        write text "# PM Claude 팀 전체 상태를 요약해주세요"
                        write text "각 팀원의 진행 상황과 이슈를 정리해주세요."
                        write text "" -- 엔터
                        delay 1
                        write text "1" -- bash command 실행
                        write text "" -- 엔터
                    end tell
                end tell
                set end of reports to "PM Claude: 팀 상태 요약 요청됨"
            end if
            
            delay 2
            
            -- Tab 3: Gemini 상태 확인
            if (count of tabs) ≥ 3 then
                tell tab 3
                    tell session 1
                        write text "# Gemini 작업 상태를 보고해주세요"
                        write text "현재 진행 중인 기획/문서 작업의 완료율과 상태를 알려주세요."
                        write text "" -- 엔터
                        delay 1
                        write text "1" -- bash command 실행
                        write text "" -- 엔터
                    end tell
                end tell
                set end of reports to "Gemini: 상태 확인 요청됨"
            end if
            
            delay 2
            
            -- Tab 4: Codex 상태 확인
            if (count of tabs) ≥ 4 then
                tell tab 4
                    tell session 1
                        write text "# Codex 작업 상태를 보고해주세요"
                        write text "현재 진행 중인 백엔드/API 작업의 완료율과 상태를 알려주세요."
                        write text "" -- 엔터
                        delay 1
                        write text "1" -- bash command 실행
                        write text "" -- 엔터
                    end tell
                end tell
                set end of reports to "Codex: 상태 확인 요청됨"
            end if
            
        end tell
    end tell
    
    -- 보고서 요약
    set reportSummary to "📋 완료 보고 수집 [" & timestamp & "]" & return
    repeat with report in reports
        set reportSummary to reportSummary & "• " & report & return
    end repeat
    
    return reportSummary
end run