#!/usr/bin/osascript

-- Chrome 브라우저 제어 및 모니터링
on run
    tell application "Google Chrome"
        activate
        
        -- 새 윈도우 생성 (또는 기존 윈도우 사용)
        if (count of windows) = 0 then
            make new window
        end if
        
        tell window 1
            -- IWL v5 리빌드 GitHub 탭 열기
            set iwlTab to make new tab with properties {URL:"https://github.com/ihw33/iwl-v5-rebuild"}
            delay 2
            
            -- Claude AI 탭 열기
            set claudeTab to make new tab with properties {URL:"https://claude.ai"}
            delay 2
            
            -- ChatGPT 탭 열기
            set chatgptTab to make new tab with properties {URL:"https://chatgpt.com"}
            delay 2
            
            -- 각 탭 순회하며 정보 수집
            set report to "🎯 AI Orchestra 웹 대시보드" & return
            set report to report & "════════════════════════════" & return & return
            
            -- GitHub 탭 확인
            set active tab index to 1
            tell active tab
                set report to report & "📍 GitHub - IWL v5 Rebuild" & return
                set report to report & "   URL: " & URL & return
                set report to report & "   제목: " & title & return
                
                -- JavaScript로 페이지 정보 가져오기
                try
                    set issueCount to execute javascript "document.querySelectorAll('.octicon-issue-opened').length"
                    set report to report & "   열린 이슈: " & issueCount & "개" & return
                on error
                    set report to report & "   (페이지 정보 로딩 중)" & return
                end try
                set report to report & return
            end tell
            
            -- Claude 탭 확인
            set active tab index to 2
            delay 1
            tell active tab
                set report to report & "🤖 Claude AI" & return
                set report to report & "   URL: " & URL & return
                set report to report & "   제목: " & title & return
                
                -- Claude 페이지에서 정보 추출 시도
                try
                    set conversationStatus to execute javascript "document.querySelector('main') ? '대화 준비됨' : '로딩 중'"
                    set report to report & "   상태: " & conversationStatus & return
                on error
                    set report to report & "   상태: 확인 중..." & return
                end try
                set report to report & return
            end tell
            
            -- ChatGPT 탭 확인
            set active tab index to 3
            delay 1
            tell active tab
                set report to report & "💬 ChatGPT" & return
                set report to report & "   URL: " & URL & return
                set report to report & "   제목: " & title & return
                
                -- ChatGPT 상태 확인
                try
                    set chatStatus to execute javascript "document.querySelector('textarea') ? '입력 준비됨' : '로딩 중'"
                    set report to report & "   상태: " & chatStatus & return
                on error
                    set report to report & "   상태: 확인 중..." & return
                end try
                set report to report & return
            end tell
            
            -- 모든 탭 요약
            set tabCount to count of tabs
            set report to report & "━━━━━━━━━━━━━━━━━━━━━━━━━━━━" & return
            set report to report & "📊 총 " & tabCount & "개 탭 활성화" & return
            
        end tell
        
        display dialog report buttons {"확인"} default button 1
        
        -- 파일로 저장
        do shell script "echo " & quoted form of report & " > /tmp/chrome_dashboard.txt"
        
        return report
    end tell
end run