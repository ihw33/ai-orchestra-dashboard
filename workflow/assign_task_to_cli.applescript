#!/usr/bin/osascript

-- 각 CLI에게 작업 프롬프트 전송
-- 사용법: osascript assign_task_to_cli.applescript <session_number> <cli_name> <task>

on run argv
    if (count of argv) < 3 then
        return "사용법: osascript assign_task_to_cli.applescript <session_number> <cli_name> <task>"
    end if
    
    set sessionNum to item 1 of argv as integer
    set cliName to item 2 of argv
    set taskDescription to item 3 of argv
    set timestamp to do shell script "date '+%H:%M:%S'"
    
    tell application "iTerm"
        tell current window
            tell current tab
                
                if (count of sessions) ≥ sessionNum then
                    tell session sessionNum
                        -- 작업 시작 프롬프트 전송
                        write text "# 🚀 [" & timestamp & "] 새로운 작업이 할당되었습니다"
                        write text "# 담당자: " & cliName
                        write text "# 작업 내용: " & taskDescription
                        write text ""
                        delay 0.5
                        
                        -- 실제 작업 요청
                        write text "다음 작업을 수행해주세요:"
                        write text taskDescription
                        write text ""
                        write text "작업을 완료하면 다음 형식으로 보고해주세요:"
                        write text "✅ 작업 완료: [완료 내용]"
                        write text "📊 결과: [구체적인 결과]"
                        write text "🔗 참고: [관련 파일이나 링크]"
                        write text "" -- 엔터
                    end tell
                else
                    return "오류: Session " & sessionNum & "이 존재하지 않습니다"
                end if
                
            end tell
        end tell
    end tell
    
    return cliName & "에게 작업 할당 완료: " & taskDescription
end run