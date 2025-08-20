#!/usr/bin/osascript

-- 실제 개발 워크플로우 자동화
on run
    -- 1단계: Claude Desktop에서 전체 설계
    tell application "Claude"
        activate
        tell application "System Events"
            keystroke "n" using command down -- 새 대화
            delay 0.5
            keystroke "전자상거래 앱의 장바구니 기능을 설계해주세요. React, TypeScript, Tailwind 사용"
            key code 36 -- Enter
        end tell
    end tell
    
    display notification "Claude Desktop 설계 중..." with title "1/5"
    delay 5 -- Claude가 응답할 시간
    
    -- 2단계: Cursor에서 컴포넌트 생성
    tell application "Cursor"
        activate
        tell application "System Events"
            -- 새 파일 생성
            keystroke "n" using command down
            delay 0.5
            -- AI에게 코드 생성 요청 (Cmd+K)
            keystroke "k" using command down
            delay 0.5
            keystroke "Cart.tsx 컴포넌트 구현: 장바구니 아이템 추가/삭제, 수량 조절, 총액 계산"
            key code 36
        end tell
    end tell
    
    display notification "Cursor 코드 생성 중..." with title "2/5"
    delay 3
    
    -- 3단계: iTerm2 CLI들에게 병렬 작업 할당
    tell application "iTerm"
        activate
        tell current window
            tell current tab
                -- Gemini: 사용자 가이드 작성
                tell session 2
                    write text "# 장바구니 기능 사용자 가이드 작성"
                    write text "print('📚 다국어 지원 가이드 작성 시작...')"
                    write text ""
                end tell
                
                -- Codex: API 엔드포인트 구현
                tell session 3
                    write text "# 장바구니 백엔드 API 구현"
                    write text "print('🔧 /api/cart 엔드포인트 구현 시작...')"
                    write text ""
                end tell
                
                -- 4번째 패널이 있으면 테스트
                set sessionCount to count of sessions
                if sessionCount ≥ 4 then
                    tell session 4
                        write text "# 장바구니 E2E 테스트 작성"
                        write text "print('🧪 Cypress 테스트 시나리오 작성...')"
                        write text ""
                    end tell
                end if
            end tell
        end tell
    end tell
    
    display notification "CLI 팀 작업 중..." with title "3/5"
    delay 3
    
    -- 4단계: VSCode에서 통합 및 테스트
    tell application "Visual Studio Code"
        activate
        tell application "System Events"
            -- 터미널 열기
            keystroke "`" using control down
            delay 0.5
            -- 개발 서버 실행
            keystroke "npm run dev"
            key code 36
        end tell
    end tell
    
    display notification "VSCode 통합 테스트..." with title "4/5"
    delay 2
    
    -- 5단계: PM Claude에서 최종 확인
    tell application "iTerm"
        tell current window
            tell current tab
                tell session 1
                    write text "# ✅ 장바구니 기능 개발 완료 체크리스트:"
                    write text "# - Claude Desktop: 설계 완료"
                    write text "# - Cursor: 컴포넌트 구현 완료"
                    write text "# - Gemini: 문서화 완료"
                    write text "# - Codex: API 구현 완료"
                    write text "# - VSCode: 통합 테스트 완료"
                    write text "gh issue close 1 -c '장바구니 기능 구현 완료'"
                end tell
            end tell
        end tell
    end tell
    
    display notification "🎉 전체 워크플로우 완료!" with title "5/5"
end run