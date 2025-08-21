#!/bin/bash

# AI Orchestra 세션 기반 워크플로우 테스트
# Session 1: 사용자 (여기)
# Session 2: PM Claude
# Session 3: Gemini  
# Session 4: Codex

echo "🤖 AI Orchestra 세션 기반 워크플로우 테스트"
echo "========================================"
echo "윈도우 세션 구성:"
echo "  • Session 1: 사용자 (현재 위치)"
echo "  • Session 2: PM Claude"
echo "  • Session 3: Gemini"
echo "  • Session 4: Codex"
echo "========================================"
echo ""

# 윈도우 1번 사용 (4개 분할 탭)
WINDOW_NUM=1

# 1. PM Claude에게 지시
echo "1️⃣ PM Claude (Session 2)에게 업무 지시..."
osascript -e "
tell application \"iTerm\"
    tell window $WINDOW_NUM
        tell current tab
            if (count of sessions) ≥ 2 then
                tell session 2
                    write text \"# 🎯 PM Claude, 새로운 프로젝트를 시작합니다\"
                    write text \"AI Orchestra 모니터링 대시보드를 구축해주세요\"
                    write text \"\" -- 엔터
                    delay 2
                    write text \"1\" -- bash command 확인
                    write text \"\" -- 엔터
                end tell
            end if
        end tell
    end tell
end tell
"

sleep 3

# 2. Gemini에게 작업 할당
echo ""
echo "2️⃣ Gemini (Session 3)에게 기획 작업 할당..."
osascript -e "
tell application \"iTerm\"
    tell window $WINDOW_NUM
        tell current tab
            if (count of sessions) ≥ 3 then
                tell session 3
                    write text \"# 📝 Gemini님, 기획 작업을 시작해주세요\"
                    write text \"대시보드 UI/UX 설계: 1) 레이아웃 2) 색상 스키마 3) 인터랙션\"
                    write text \"\" -- 엔터
                    delay 3
                    write text \"1\" -- bash command 확인
                    write text \"\" -- 엔터
                end tell
            end if
        end tell
    end tell
end tell
"

sleep 3

# 3. Codex에게 작업 할당
echo ""
echo "3️⃣ Codex (Session 4)에게 개발 작업 할당..."
echo "   ⚠️  Codex는 긴 답변을 할 수 있으니 기다려주세요..."
osascript -e "
tell application \"iTerm\"
    tell window $WINDOW_NUM
        tell current tab
            if (count of sessions) ≥ 4 then
                tell session 4
                    write text \"# 💻 Codex님, 백엔드 개발을 시작해주세요\"
                    write text \"REST API 구현: /api/dashboard, /api/metrics, WebSocket 지원\"
                    write text \"\" -- 엔터
                    delay 5 -- Codex는 더 오래 대기
                    write text \"1\" -- bash command 확인
                    write text \"\" -- 엔터
                end tell
            end if
        end tell
    end tell
end tell
"

echo ""
echo "========================================"
echo "✅ 세션 기반 워크플로우 테스트 완료!"
echo ""
echo "각 세션에서 AI들이 작업을 시작했는지 확인하세요:"
echo "• Session 2 (PM Claude): 프로젝트 관리"
echo "• Session 3 (Gemini): UI/UX 기획"
echo "• Session 4 (Codex): 백엔드 개발"