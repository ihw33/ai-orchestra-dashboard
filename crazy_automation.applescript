#!/usr/bin/osascript

-- 미친 자동화: PM Claude가 팀 전체 제어
on run
    tell application "iTerm"
        tell current window
            tell current tab
                -- Claude 1에게 복잡한 계산
                tell session 2
                    write text "파이썬으로 피보나치 수열 100번째 값을 계산해줘"
                    write text ""
                end tell
                
                delay 2
                
                -- Claude 2에게 코드 리뷰
                tell session 3
                    write text "다음 코드를 리뷰해줘: function add(a,b) { return a+b }"
                    write text ""
                end tell
                
                delay 2
                
                -- Claude 3에게 문서 작성
                tell session 4
                    write text "README.md 파일을 작성해줘. 프로젝트명: AI Orchestra"
                    write text ""
                end tell
                
                display notification "🤯 모든 Claude가 동시에 작업 중!" with title "믿기지 않는 자동화"
            end tell
        end tell
    end tell
end run