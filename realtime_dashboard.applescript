#!/usr/bin/osascript

-- 실시간 AI Orchestra 대시보드 (주식 트레이딩 화면처럼)
on run
    tell application "Google Chrome"
        activate
        
        -- 무한 루프로 실시간 모니터링
        repeat 10 times -- 테스트용으로 10회만
            
            set dashboard to "┌────────────────────────────────────────────────┐" & return
            set dashboard to dashboard & "│     🎯 AI ORCHESTRA REALTIME DASHBOARD         │" & return
            set dashboard to dashboard & "│     " & (current date) as string & "    │" & return
            set dashboard to dashboard & "└────────────────────────────────────────────────┘" & return & return
            
            -- 각 윈도우/탭 상태 체크
            repeat with w from 1 to count of windows
                tell window w
                    set dashboard to dashboard & "╔══════════════════════════════════════════════╗" & return
                    set dashboard to dashboard & "║ WINDOW " & w & " - TABS: " & (count of tabs) & "                            ║" & return
                    set dashboard to dashboard & "╠══════════════════════════════════════════════╣" & return
                    
                    repeat with t from 1 to count of tabs
                        tell tab t
                            set tabURL to URL
                            set tabTitle to title
                            set isLoading to loading
                            
                            -- 상태 인디케이터
                            if isLoading then
                                set statusIcon to "🔄"
                            else
                                set statusIcon to "✅"
                            end if
                            
                            -- 사이트별 아이콘
                            if tabURL contains "github" then
                                set siteIcon to "🔧"
                                set siteType to "GitHub"
                            else if tabURL contains "claude" then
                                set siteIcon to "🤖"
                                set siteType to "Claude"
                            else if tabURL contains "chatgpt" then
                                set siteIcon to "💬"
                                set siteType to "ChatGPT"
                            else if tabURL contains "gemini" then
                                set siteIcon to "✨"
                                set siteType to "Gemini"
                            else
                                set siteIcon to "🌐"
                                set siteType to "Web"
                            end if
                            
                            -- 제목 줄이기
                            if length of tabTitle > 30 then
                                set shortTitle to text 1 thru 30 of tabTitle & "..."
                            else
                                set shortTitle to tabTitle
                            end if
                            
                            set dashboard to dashboard & "║ " & statusIcon & " " & siteIcon & " [" & siteType & "] " & shortTitle
                            
                            -- 공백 채우기
                            set lineLength to length of ("║ " & statusIcon & " " & siteIcon & " [" & siteType & "] " & shortTitle)
                            repeat (48 - lineLength) times
                                set dashboard to dashboard & " "
                            end repeat
                            set dashboard to dashboard & "║" & return
                            
                            -- GitHub 이슈/PR 실시간 체크
                            if tabURL contains "github" and not isLoading then
                                try
                                    set issueInfo to execute javascript "
                                        var issues = document.querySelectorAll('.octicon-issue-opened').length;
                                        var prs = document.querySelectorAll('.octicon-git-pull-request').length;
                                        'Issues: ' + issues + ' | PRs: ' + prs
                                    "
                                    set dashboard to dashboard & "║    📊 " & issueInfo & "                        ║" & return
                                on error
                                    -- 무시
                                end try
                            end if
                            
                        end tell
                    end repeat
                    
                    set dashboard to dashboard & "╚══════════════════════════════════════════════╝" & return & return
                end tell
            end repeat
            
            -- iTerm2 세션 상태도 함께 표시
            tell application "iTerm"
                tell current window
                    tell current tab
                        set sessionCount to count of sessions
                        set dashboard to dashboard & "┌─── iTerm2 CLI Status ───────────────────────┐" & return
                        
                        repeat with s from 1 to sessionCount
                            tell session s
                                set sessionName to name
                                set atPrompt to is at shell prompt
                                
                                if atPrompt then
                                    set cliStatus to "⏸️  IDLE"
                                else
                                    set cliStatus to "⚡ BUSY"
                                end if
                                
                                set dashboard to dashboard & "│ Session " & s & ": " & cliStatus & " - " & sessionName
                                
                                -- 공백 채우기
                                set lineContent to "Session " & s & ": " & cliStatus & " - " & sessionName
                                repeat (45 - (length of lineContent)) times
                                    set dashboard to dashboard & " "
                                end repeat
                                set dashboard to dashboard & "│" & return
                            end tell
                        end repeat
                        
                        set dashboard to dashboard & "└──────────────────────────────────────────────┘" & return
                    end tell
                end tell
            end tell
            
            -- 콘솔 클리어하고 대시보드 출력 (터미널 시뮬레이션)
            do shell script "clear && echo " & quoted form of dashboard
            
            -- 파일로도 저장 (다른 도구에서 읽을 수 있도록)
            do shell script "echo " & quoted form of dashboard & " > /tmp/ai_orchestra_live.txt"
            
            -- 3초 대기 후 다시 업데이트
            delay 3
        end repeat
        
        display notification "대시보드 모니터링 완료" with title "AI Orchestra"
    end tell
end run