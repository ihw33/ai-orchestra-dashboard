#!/usr/bin/osascript

-- Chrome 브라우저 탭 모니터링
on run
    tell application "Google Chrome"
        activate
        
        set monitorReport to "🌐 Chrome Browser Monitor" & return
        set monitorReport to monitorReport & "━━━━━━━━━━━━━━━━━━━━━━━━━━" & return & return
        
        -- 모든 윈도우 탐색
        set windowCount to count of windows
        set monitorReport to monitorReport & "📊 총 " & windowCount & "개의 Chrome 윈도우 발견" & return & return
        
        repeat with w from 1 to windowCount
            tell window w
                set monitorReport to monitorReport & "📦 윈도우 " & w & return
                set tabCount to count of tabs
                set monitorReport to monitorReport & "   탭 개수: " & tabCount & return & return
                
                -- 각 탭 정보 수집
                repeat with t from 1 to tabCount
                    tell tab t
                        set tabTitle to title
                        set tabURL to URL
                        
                        set monitorReport to monitorReport & "   📑 탭 " & t & ":" & return
                        set monitorReport to monitorReport & "      제목: " & tabTitle & return
                        set monitorReport to monitorReport & "      URL: " & tabURL & return
                        
                        -- 특정 사이트 식별
                        if tabURL contains "github.com" then
                            set monitorReport to monitorReport & "      🔧 타입: GitHub 저장소" & return
                            if tabURL contains "iwl-v5-rebuild" then
                                set monitorReport to monitorReport & "      ✨ IWL v5 리빌드 프로젝트!" & return
                            end if
                        else if tabURL contains "claude.ai" then
                            set monitorReport to monitorReport & "      🤖 타입: Claude AI" & return
                        else if tabURL contains "chatgpt.com" or tabURL contains "openai.com" then
                            set monitorReport to monitorReport & "      💬 타입: ChatGPT" & return
                        else if tabURL contains "gemini.google.com" then
                            set monitorReport to monitorReport & "      ✨ 타입: Google Gemini" & return
                        end if
                        
                        -- 로딩 상태 확인
                        if loading then
                            set monitorReport to monitorReport & "      ⏳ 상태: 로딩 중..." & return
                        else
                            set monitorReport to monitorReport & "      ✅ 상태: 로드 완료" & return
                        end if
                        
                        set monitorReport to monitorReport & return
                    end tell
                end repeat
                
                set monitorReport to monitorReport & return
            end tell
        end repeat
        
        -- 결과 표시
        display dialog monitorReport buttons {"확인"} default button 1
        
        -- 파일로 저장
        do shell script "echo " & quoted form of monitorReport & " > /tmp/chrome_monitor.txt"
        
        return monitorReport
    end tell
end run