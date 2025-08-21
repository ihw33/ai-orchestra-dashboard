#!/usr/bin/osascript

-- AI Orchestra 완전 자동화
-- PM Claude (세션 1) → 팀원들 (세션 2,3,4)

on run
    tell application "iTerm"
        activate
        
        tell current window
            tell current tab
                -- PM이 작업 지시
                tell session 1
                    write text "# 🎯 PM Claude: 팀 전체에 작업 할당"
                end tell
                
                delay 1
                
                -- Gemini에게
                tell session 2
                    write text "print('PM으로부터: Issue #3 사용자 가이드 작성 시작하세요')"
                    write text "" -- Enter 효과
                end tell
                
                delay 2
                
                -- Codex에게  
                tell session 3
                    write text "print('PM으로부터: Issue #2 API 최적화 진행하세요')"
                    write text "" -- Enter 효과
                end tell
                
                delay 2
                
                -- 4번째 패널이 있다면
                set sessionCount to count of sessions
                if sessionCount ≥ 4 then
                    tell session 4
                        write text "print('PM으로부터: 추가 작업 - 테스트 코드 작성')"
                        write text "" -- Enter 효과
                    end tell
                end if
                
                delay 2
                
                -- PM이 상태 확인
                tell session 1
                    write text "# ✅ 모든 팀원에게 작업 할당 완료!"
                end tell
            end tell
        end tell
    end tell
    
    display notification "🎉 AI Orchestra 자동화 성공!" with title "완료"
end run