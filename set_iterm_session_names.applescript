#!/usr/bin/osascript
(*
iTerm2 세션에 이름 설정하기
각 세션에 고유 ID를 이름으로 설정
*)

on run
    tell application "iTerm2"
        -- Tab 1: Home
        tell tab 1 of current window
            set name to "🏠 Home"
            tell session 1
                set name to "HOME_MAIN"
            end tell
            if (count of sessions) ≥ 2 then
                tell session 2
                    set name to "HOME_MONITOR"
                end tell
            end if
        end tell
        
        -- Tab 2: AI Engine
        if (count of tabs of current window) ≥ 2 then
            tell tab 2 of current window
                set name to "🤖 AI Engine"
                tell session 1
                    set name to "ENGINE_GEMINI"
                end tell
                if (count of sessions) ≥ 2 then
                    tell session 2
                        set name to "ENGINE_CODEX"
                    end tell
                end if
                if (count of sessions) ≥ 3 then
                    tell session 3
                        set name to "ENGINE_TERMINAL"
                    end tell
                end if
            end tell
        end if
        
        -- Tab 3: IWL Project
        if (count of tabs of current window) ≥ 3 then
            tell tab 3 of current window
                set name to "📚 IWL Project"
                tell session 1
                    set name to "IWL_PM"
                end tell
                if (count of sessions) ≥ 2 then
                    tell session 2
                        set name to "IWL_CURSOR"
                    end tell
                end if
                if (count of sessions) ≥ 3 then
                    tell session 3
                        set name to "IWL_GEMINI"
                    end tell
                end if
                if (count of sessions) ≥ 4 then
                    tell session 4
                        set name to "IWL_CODEX"
                    end tell
                end if
            end tell
        end if
        
        -- Tab 4: Orchestra Board
        if (count of tabs of current window) ≥ 4 then
            tell tab 4 of current window
                set name to "🎼 Orchestra"
                tell session 1
                    set name to "ORCH_CLAUDE"
                end tell
                if (count of sessions) ≥ 2 then
                    tell session 2
                        set name to "ORCH_TERMINAL"
                    end tell
                end if
                if (count of sessions) ≥ 3 then
                    tell session 3
                        set name to "ORCH_GEMINI"
                    end tell
                end if
                if (count of sessions) ≥ 4 then
                    tell session 4
                        set name to "ORCH_CODEX"
                    end tell
                end if
            end tell
        end if
        
        return "✅ 세션 이름 설정 완료!"
    end tell
end run