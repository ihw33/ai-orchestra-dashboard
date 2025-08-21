#!/bin/bash

# AI별 특성을 고려한 스마트 워크플로우 테스트

echo "🤖 AI Orchestra 스마트 워크플로우 테스트"
echo "========================================"
echo "각 AI의 응답 특성:"
echo "  • PM Claude (Tab 2): 빠른 응답 (2초)"
echo "  • Gemini (Tab 3): 보통 속도 (3-4초)"
echo "  • Codex (Tab 4): 긴 답변 (5-6초+)"
echo "========================================"
echo ""

# 1. PM Claude에게 빠른 지시
echo "1️⃣ PM Claude (Tab 2) - 빠른 지시..."
osascript smart_task_sender.applescript 2 "PM_Claude" \
    "팀 전체 상태를 간단히 요약해주세요"

echo "   ✓ PM Claude 작업 전송 완료"
sleep 2

# 2. Gemini에게 중간 길이 작업
echo ""
echo "2️⃣ Gemini (Tab 3) - 기획 작업..."
osascript smart_task_sender.applescript 3 "Gemini" \
    "모니터링 대시보드 화면 구성을 설계해주세요. 주요 메트릭과 레이아웃을 포함해주세요."

echo "   ✓ Gemini 작업 전송 완료"
sleep 2

# 3. Codex에게 복잡한 작업
echo ""
echo "3️⃣ Codex (Tab 4) - 복잡한 개발 작업..."
echo "   ⚠️  Codex는 답변이 길 수 있으니 잠시 기다려주세요..."
osascript smart_task_sender.applescript 4 "Codex" \
    "WebSocket 기반 실시간 모니터링 API를 설계해주세요. 다음을 포함해주세요: 1) 연결 관리 2) 메시지 프로토콜 3) 에러 핸들링 4) 성능 최적화 방안"

echo "   ✓ Codex 작업 전송 완료 (긴 답변 대기 포함)"

echo ""
echo "========================================"
echo "✅ 스마트 워크플로우 테스트 완료!"
echo ""
echo "💡 Tips:"
echo "1. 각 탭을 확인하여 AI가 제대로 응답했는지 확인"
echo "2. Codex (Tab 4)는 답변 중에 확인 프롬프트가 뜰 수 있음"
echo "3. 필요시 수동으로 '1' 입력하여 진행"
echo ""
echo "📌 다음 단계: 각 AI의 응답을 GitHub Issue로 수집"