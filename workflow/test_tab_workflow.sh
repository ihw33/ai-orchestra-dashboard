#!/bin/bash

# AI Orchestra 탭 기반 워크플로우 테스트
# Tab 1: 여기 (사용자)
# Tab 2: Claude PM
# Tab 3: Gemini
# Tab 4: Codex

echo "🚀 AI Orchestra 탭 기반 워크플로우 테스트"
echo "========================================"
echo "탭 구성:"
echo "  Tab 1: 사용자 (현재 위치)"
echo "  Tab 2: PM Claude"
echo "  Tab 3: Gemini"
echo "  Tab 4: Codex"
echo "========================================"
echo ""

# 1. PM에게 업무 지시
echo "1️⃣ PM Claude (Tab 2)에게 업무 지시 전달..."
osascript pm_task_distributor.applescript \
    "AI Orchestra 모니터링 시스템 구축" \
    "실시간 대시보드, API 연동, UI/UX 개선 작업 필요"

sleep 3

# 2. 각 탭의 CLI에 작업 할당
echo ""
echo "2️⃣ 각 팀원에게 작업 할당..."
echo ""

# Tab 3: Gemini에게 기획 작업
echo "   📝 Gemini (Tab 3): 기획/문서 작업 할당"
osascript assign_task_to_tab.applescript 3 "Gemini" \
    "모니터링 대시보드 기획서 작성: 1) 화면 레이아웃 설계 2) 주요 메트릭 정의 3) 사용자 시나리오 작성"

sleep 2

# Tab 4: Codex에게 백엔드 작업
echo "   💻 Codex (Tab 4): 백엔드 작업 할당"
osascript assign_task_to_tab.applescript 4 "Codex" \
    "모니터링 API 구현: 1) /api/health 상태 체크 2) /api/metrics 실시간 메트릭 3) WebSocket 실시간 업데이트"

sleep 3

# 3. 진행 상황 체크
echo ""
echo "3️⃣ 작업 할당 완료. 10초 후 진행 상황 체크..."
echo "   (각 탭에서 CLI들이 작업을 시작했는지 확인하세요)"
sleep 10

# 4. 완료 보고 수집
echo ""
echo "4️⃣ 각 탭에서 상태 보고 수집..."
result=$(osascript collect_reports_from_tabs.applescript)
echo "$result"

echo ""
echo "========================================"
echo "✅ 워크플로우 테스트 완료!"
echo ""
echo "다음 단계:"
echo "1. 각 탭으로 이동하여 CLI 응답 확인"
echo "2. PM Claude (Tab 2)의 팀 관리 확인"
echo "3. Gemini (Tab 3)의 기획 작업 진행 확인"
echo "4. Codex (Tab 4)의 개발 작업 진행 확인"
echo ""
echo "💡 Tip: Cmd+숫자로 탭 전환 가능 (Cmd+2 = PM Claude)"