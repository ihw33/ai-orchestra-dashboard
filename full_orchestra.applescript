#!/usr/bin/osascript

-- 전체 개발 도구 협업 자동화
-- CLI + IDE + Desktop App 통합

on run
    display notification "🎼 Full Orchestra 시작!" with title "AI 협업"
    
    -- 1. Claude Desktop에서 기획
    tell application "Claude"
        activate
        delay 1
        -- Claude Desktop에 질문 입력
        tell application "System Events"
            keystroke "새로운 React 컴포넌트 구조를 설계해주세요"
            delay 0.5
            key code 36 -- Enter
        end tell
    end tell
    
    delay 3
    
    -- 2. Cursor IDE에서 코드 작성
    tell application "Cursor"
        activate
        delay 1
        -- 새 파일 생성 (Cmd+N)
        tell application "System Events"
            keystroke "n" using command down
            delay 0.5
            -- 컴포넌트 코드 작성 시작
            keystroke "// Claude Desktop의 설계를 바탕으로 구현"
            key code 36
            keystroke "import React from 'react'"
            key code 36
        end tell
    end tell
    
    delay 2
    
    -- 3. iTerm2의 CLI들에게 작업 분배
    tell application "iTerm"
        activate
        tell current window
            tell current tab
                -- PM Claude (세션 1)
                tell session 1
                    write text "# 협업 시작: 컴포넌트 개발"
                end tell
                
                -- Gemini (세션 2) - 문서화
                tell session 2
                    write text "print('📝 컴포넌트 문서 작성 시작')"
                    write text ""
                end tell
                
                -- Codex (세션 3) - 테스트 코드
                tell session 3
                    write text "print('🧪 테스트 코드 작성 시작')"
                    write text ""
                end tell
            end tell
        end tell
    end tell
    
    delay 2
    
    -- 4. VSCode에서 결과 확인
    tell application "Visual Studio Code"
        activate
        -- 터미널 열기
        tell application "System Events"
            keystroke "`" using control down
            delay 0.5
            -- 테스트 실행
            keystroke "npm test"
            key code 36
        end tell
    end tell
    
    display notification "✅ 모든 도구 협업 완료!" with title "성공"
end run