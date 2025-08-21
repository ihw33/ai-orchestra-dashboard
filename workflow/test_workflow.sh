#!/bin/bash

# AI Orchestra 워크플로우 테스트
# 간단한 테스트 시나리오 실행

echo "🚀 AI Orchestra 워크플로우 테스트 시작"
echo "=================================="

# 1. PM에게 업무 지시
echo "1️⃣ PM Claude에게 업무 지시 전달 중..."
osascript pm_task_distributor.applescript \
    "AI Orchestra 대시보드 구축" \
    "1. 실시간 모니터링 대시보드 구현\n2. API 연동\n3. UI/UX 개선"

sleep 3

# 2. 각 CLI에 작업 할당
echo ""
echo "2️⃣ 팀원들에게 작업 할당 중..."

# Gemini에게 기획 작업
osascript assign_task_to_cli.applescript 5 "Gemini" \
    "대시보드 기획서 작성: 화면 구성, 기능 정의, 사용자 시나리오"

sleep 2

# Codex에게 백엔드 작업
osascript assign_task_to_cli.applescript 6 "Codex" \
    "REST API 구현: /api/status, /api/metrics, /api/tasks 엔드포인트"

sleep 2

# 3. 진행 상황 체크
echo ""
echo "3️⃣ 10초 후 진행 상황 체크..."
sleep 10

# 4. 완료 보고 수집
echo ""
echo "4️⃣ 완료 보고 수집 중..."
osascript collect_completion_report.applescript

echo ""
echo "✅ 테스트 완료!"
echo "=================================="
echo ""
echo "다음 단계:"
echo "1. 각 CLI 세션에서 응답 확인"
echo "2. GitHub Issue 생성 및 연동"
echo "3. 실제 작업 완료 후 알림 받기"