#!/usr/bin/osascript

(*
AI Orchestra 자동화 플로우
PM Claude 터미널에서 특정 텍스트 감지 → Gemini/Codex 터미널에 자동 입력
*)

on run
    -- PM Claude 터미널에서 텍스트 가져오기
    tell application "Terminal"
        tell window 1
            set pmOutput to contents of selected tab
        end tell
    end tell
    
    -- @gemini: 패턴 찾기
    if pmOutput contains "@gemini:" then
        set geminiMessage to extractMessage(pmOutput, "@gemini:")
        sendToTerminal(2, geminiMessage) -- 터미널 2 (Gemini)
    end if
    
    -- @codex: 패턴 찾기
    if pmOutput contains "@codex:" then
        set codexMessage to extractMessage(pmOutput, "@codex:")
        sendToTerminal(3, codexMessage) -- 터미널 3 (Codex)
    end if
end run

-- 메시지 추출
on extractMessage(fullText, marker)
    set AppleScript's text item delimiters to marker
    set textItems to text items of fullText
    if (count of textItems) > 1 then
        set messageText to item 2 of textItems
        -- 줄바꿈까지만 추출
        set AppleScript's text item delimiters to return
        set firstLine to item 1 of text items of messageText
        return firstLine
    end if
    return ""
end extractMessage

-- 특정 터미널에 메시지 전송
on sendToTerminal(windowNumber, message)
    tell application "Terminal"
        activate
        tell window windowNumber
            -- 실제 키보드 입력처럼 타이핑
            tell application "System Events"
                keystroke message
                key code 36 -- Enter 키
            end tell
        end tell
    end tell
    
    -- 원래 창으로 돌아가기
    delay 0.5
    tell application "Terminal"
        tell window 1 to activate
    end tell
end sendToTerminal