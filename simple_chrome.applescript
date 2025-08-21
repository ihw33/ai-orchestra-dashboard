#!/usr/bin/osascript

-- 간단한 Chrome 탭 정보 출력
on run
    tell application "Google Chrome"
        set output to ""
        
        -- 첫 번째 윈도우만 체크
        if (count of windows) > 0 then
            tell window 1
                set tabCount to count of tabs
                set output to output & "🌐 Chrome Window 1 - " & tabCount & " tabs" & return & return
                
                -- 최대 5개 탭만 표시
                set maxTabs to 5
                if tabCount < maxTabs then set maxTabs to tabCount
                
                repeat with t from 1 to maxTabs
                    tell tab t
                        set tabTitle to title
                        set tabURL to URL
                        
                        -- 제목 줄이기
                        if length of tabTitle > 40 then
                            set tabTitle to text 1 thru 40 of tabTitle & "..."
                        end if
                        
                        set output to output & "Tab " & t & ": " & tabTitle & return
                        set output to output & "  → " & tabURL & return & return
                    end tell
                end repeat
                
                if tabCount > 5 then
                    set output to output & "... and " & (tabCount - 5) & " more tabs" & return
                end if
            end tell
        else
            set output to "No Chrome windows open"
        end if
        
        -- 결과 반환 (dialog 없이)
        return output
    end tell
end run