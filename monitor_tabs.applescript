#!/usr/bin/osascript

-- 주요 탭들을 실시간 모니터링
on run
    tell application "Google Chrome"
        set report to "📊 AI Orchestra Chrome Monitor" & return
        set report to report & "Time: " & (current date) as string & return
        set report to report & "════════════════════════════════" & return & return
        
        tell window 1
            -- GitHub 탭 찾기 (Tab 1)
            tell tab 1
                set report to report & "🔧 GitHub Project" & return
                set report to report & "  Title: " & title & return
                
                -- Issue #21 페이지인지 확인
                if URL contains "issues/21" then
                    set report to report & "  📌 Issue #21 열람 중" & return
                    
                    -- JavaScript로 페이지 내용 추출
                    try
                        set issueTitle to execute javascript "document.querySelector('.js-issue-title')?.innerText || 'Loading...'"
                        set issueState to execute javascript "document.querySelector('.State')?.innerText || 'Unknown'"
                        set report to report & "  Issue: " & issueTitle & return
                        set report to report & "  State: " & issueState & return
                    on error
                        set report to report & "  (페이지 로딩 중)" & return
                    end try
                end if
                set report to report & return
            end tell
            
            -- ChatGPT 탭 찾기 (Tab 2)
            tell tab 2
                set report to report & "💬 ChatGPT" & return
                set report to report & "  Title: " & title & return
                
                if URL contains "chatgpt.com" then
                    try
                        -- 현재 대화 상태 확인
                        set hasTextarea to execute javascript "document.querySelector('textarea') ? true : false"
                        if hasTextarea as boolean then
                            set report to report & "  ✅ 입력창 활성화됨" & return
                        else
                            set report to report & "  ⏳ 로딩 중..." & return
                        end if
                    on error
                        set report to report & "  상태 확인 불가" & return
                    end try
                end if
                set report to report & return
            end tell
            
            -- Google Drive 탭 (Tab 3)
            tell tab 3
                set report to report & "📁 Google Drive" & return
                set report to report & "  Title: " & title & return
                
                if URL contains "drive.google.com" then
                    set report to report & "  📂 생각정리 기술 3.0 폴더" & return
                end if
                set report to report & return
            end tell
            
            -- 탭 간 전환 시연
            set report to report & "────────────────────────────────" & return
            set report to report & "🎯 Actions Available:" & return
            set report to report & "  • Switch to any tab" & return
            set report to report & "  • Refresh specific tabs" & return
            set report to report & "  • Execute JavaScript" & return
            set report to report & "  • Open new tabs" & return
            
            -- 특정 탭으로 전환 예시
            -- set active tab index to 1  -- GitHub 탭으로 전환
            
        end tell
        
        return report
    end tell
end run