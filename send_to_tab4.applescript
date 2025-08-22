tell application "System Events"
    -- Tab 4 Claude에게 메시지 전송
    set messageText to "KPI 시스템 개선 작업 요청입니다.

작업 지시서를 확인해주세요:
/Users/m4_macbook/Projects/ai-orchestra-dashboard/task_for_tab4_claude.md

다음 파일들을 리뷰하고 개선해주세요:
- /Users/m4_macbook/Projects/ai-orchestra-dashboard/round5/improved_kpi_system.py
- /Users/m4_macbook/Projects/ai-orchestra-dashboard/round5/detailed_kpi_system.py
- /Users/m4_macbook/Projects/ai-orchestra-dashboard/round5/kpi_analyzer.py

완료 후:
1. round5/final_kpi_system.py 생성
2. round5/improvements.md 작성
3. PR #61 업데이트 준비

감사합니다!
- PM Claude"
    
    -- 클립보드에 복사
    set the clipboard to messageText
    
    -- iTerm2로 전환
    tell application "iTerm2"
        activate
        tell current window
            -- Tab 4 선택 (0-indexed이므로 3)
            tell tab 4
                select
            end tell
        end tell
    end tell
    
    delay 0.5
    
    -- 메시지 붙여넣기
    keystroke "v" using command down
    delay 0.2
    
    -- 엔터 키 전송
    key code 36
end tell