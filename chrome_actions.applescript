#!/usr/bin/osascript

-- Chrome 탭 제어 (dialog 없이)
on run
    tell application "Google Chrome"
        tell window 1
            -- 1. ChatGPT 탭으로 전환 (Tab 2)
            set active tab index to 2
            delay 1
            
            -- 2. 페이지 새로고침
            tell active tab
                reload
            end tell
            delay 2
            
            -- 3. GitHub 탭으로 전환 (Tab 1)
            set active tab index to 1
            delay 1
            
            -- 4. GitHub에서 새로고침
            tell active tab
                reload
            end tell
            delay 2
            
            -- 5. Google Drive 탭으로 전환 (Tab 3)
            set active tab index to 3
            delay 1
            
            -- 6. 새 탭 열기 - Claude AI
            make new tab with properties {URL:"https://claude.ai"}
            delay 2
            
            -- 7. 다시 GitHub 탭으로
            set active tab index to 1
            
            return "✅ Chrome 제어 완료: 탭 전환, 새로고침, 새 탭 생성"
        end tell
    end tell
end run