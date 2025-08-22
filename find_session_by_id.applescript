#!/usr/bin/osascript
(*
세션 ID로 특정 세션 찾아가기
*)

on findSessionByID(targetID)
    tell application "iTerm2"
        tell current window
            repeat with tabIndex from 1 to (count of tabs)
                tell tab tabIndex
                    repeat with sessionIndex from 1 to (count of sessions)
                        tell session sessionIndex
                            if name is targetID then
                                -- 찾은 세션으로 포커스 이동
                                select
                                return "✅ 세션 찾음: " & targetID & " (Tab " & tabIndex & ", Session " & sessionIndex & ")"
                            end if
                        end tell
                    end repeat
                end tell
            end repeat
        end tell
    end tell
    return "❌ 세션을 찾을 수 없음: " & targetID
end findSessionByID

-- 테스트
on run
    set testID to "ORCH_GEMINI"
    return findSessionByID(testID)
end run