#!/usr/bin/osascript

-- 완료 보고 수집 스크립트
-- 각 CLI 세션에서 완료 보고를 확인하고 GitHub Issue 댓글로 추가

on run
    set reports to {}
    set timestamp to do shell script "date '+%Y-%m-%d %H:%M:%S'"
    
    tell application "iTerm"
        tell current window
            tell current tab
                
                -- Session 5: Gemini 상태 확인
                if (count of sessions) ≥ 5 then
                    tell session 5
                        write text "# Gemini 작업 상태를 보고해주세요"
                        write text "현재 진행 중인 작업의 완료율과 상태를 알려주세요."
                        write text "" -- 엔터
                    end tell
                    set end of reports to "Gemini: 상태 확인 요청됨"
                end if
                
                delay 2
                
                -- Session 6: Codex 상태 확인
                if (count of sessions) ≥ 6 then
                    tell session 6
                        write text "# Codex 작업 상태를 보고해주세요"
                        write text "현재 진행 중인 작업의 완료율과 상태를 알려주세요."
                        write text "" -- 엔터
                    end tell
                    set end of reports to "Codex: 상태 확인 요청됨"
                end if
                
                delay 2
                
                -- Session 7: Claude2 상태 확인 (있다면)
                if (count of sessions) ≥ 7 then
                    tell session 7
                        write text "# Claude2 작업 상태를 보고해주세요"
                        write text "현재 진행 중인 작업의 완료율과 상태를 알려주세요."
                        write text "" -- 엔터
                    end tell
                    set end of reports to "Claude2: 상태 확인 요청됨"
                end if
                
            end tell
        end tell
    end tell
    
    -- 보고서 요약
    set reportSummary to "📋 완료 보고 수집 [" & timestamp & "]" & return
    repeat with report in reports
        set reportSummary to reportSummary & "• " & report & return
    end repeat
    
    return reportSummary
end run