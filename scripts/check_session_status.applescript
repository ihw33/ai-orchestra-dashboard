#!/usr/bin/osascript

on checkSessionStatus(tabNum, sessionNum)
    tell application "iTerm"
        tell current window
            tell tab tabNum
                tell session sessionNum
                    set sessionText to contents
                    set lastLine to paragraph -1 of sessionText
                    set sessionName to name
                    
                    -- 상태 판단 로직
                    if lastLine contains ">" then
                        return {state:"ready", reason:"Claude prompt detected", lastLine:lastLine}
                    else if lastLine contains "$" then
                        return {state:"ready", reason:"Shell prompt detected", lastLine:lastLine}
                    else if lastLine contains "%" then
                        return {state:"ready", reason:"Zsh prompt detected", lastLine:lastLine}
                    else if lastLine contains "..." then
                        return {state:"processing", reason:"Continuation prompt", lastLine:lastLine}
                    else if lastLine contains "Press" and lastLine contains "continue" then
                        return {state:"paused", reason:"Waiting for user input", lastLine:lastLine}
                    else if lastLine contains "Password:" then
                        return {state:"auth_required", reason:"Password prompt", lastLine:lastLine}
                    else if sessionText contains "Thinking" then
                        return {state:"thinking", reason:"AI is thinking", lastLine:lastLine}
                    else if length of lastLine < 1 then
                        return {state:"unknown", reason:"Empty line", lastLine:"(empty)"}
                    else
                        return {state:"busy", reason:"No prompt detected", lastLine:lastLine}
                    end if
                end tell
            end tell
        end tell
    end tell
end checkSessionStatus

-- 사용 예시
set status to checkSessionStatus(1, 1)
return "Session State: " & state of status & return & "Reason: " & reason of status & return & "Last Line: " & lastLine of status
