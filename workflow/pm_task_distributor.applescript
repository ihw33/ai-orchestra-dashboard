#!/usr/bin/osascript

-- PM Claude 업무 배분 자동화 스크립트
-- 사용법: osascript pm_task_distributor.applescript "이슈제목" "이슈내용"

on run argv
    if (count of argv) < 2 then
        return "사용법: osascript pm_task_distributor.applescript '이슈제목' '이슈내용'"
    end if
    
    set issueTitle to item 1 of argv
    set issueBody to item 2 of argv
    set timestamp to do shell script "date '+%Y-%m-%d %H:%M:%S'"
    
    tell application "iTerm"
        tell current window
            tell current tab
                
                -- Tab 2: PM Claude에게 업무 지시
                tell tab 2
                    tell session 1
                        write text "# 🎯 새로운 업무 지시가 도착했습니다"
                        write text "# 시간: " & timestamp
                        write text "# 제목: " & issueTitle
                        write text "# 내용: " & issueBody
                        write text ""
                        delay 1
                        
                        write text "PM으로서 다음 업무를 팀원들에게 배분해주세요:"
                        write text "1. Gemini (Tab 3): 기획 및 문서 작업"
                        write text "2. Codex (Tab 4): 백엔드 및 API 개발"
                        write text ""
                        write text "각 팀원의 구체적인 태스크를 정의하고 GitHub Issue를 생성해주세요."
                        write text "" -- 엔터
                        delay 1
                        write text "1" -- bash command 실행을 위한 1 입력
                        write text "" -- 엔터
                    end tell
                end if
                
            end tell
        end tell
    end tell
    
    return "PM Claude에게 업무 지시 전달 완료: " & issueTitle
end run