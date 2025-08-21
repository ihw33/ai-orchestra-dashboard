#!/usr/bin/osascript

-- Chrome 특정 탭 스크린샷 캡처
on run
    tell application "Google Chrome"
        tell window 1
            -- GitHub 탭으로 전환 (Tab 1)
            set active tab index to 1
            delay 1
            
            -- 스크린샷 저장 경로
            set screenshotPath to "/tmp/github_tab.png"
            
            -- screencapture 명령으로 활성 윈도우 캡처
            do shell script "screencapture -w -x " & screenshotPath
            
            -- ChatGPT 탭 캡처 (Tab 2)
            set active tab index to 2
            delay 1
            set screenshotPath2 to "/tmp/chatgpt_tab.png"
            do shell script "screencapture -w -x " & screenshotPath2
            
            -- Google Drive 탭 캡처 (Tab 3)
            set active tab index to 3
            delay 1
            set screenshotPath3 to "/tmp/gdrive_tab.png"
            do shell script "screencapture -w -x " & screenshotPath3
            
            return "📸 스크린샷 저장 완료:" & return & "  • /tmp/github_tab.png" & return & "  • /tmp/chatgpt_tab.png" & return & "  • /tmp/gdrive_tab.png"
        end tell
    end tell
end run