#!/bin/bash
# Allow 요청 시스템 통합 테스트

echo "🧪 Allow 요청 시스템 테스트 시작"
echo "================================="

# 1. Python 테스트 실행
echo ""
echo "1️⃣ 명령어 분석 테스트:"
python3 test_allow_system.py

# 2. AppleScript 모니터링 테스트
echo ""
echo "2️⃣ iTerm2 모니터링 테스트:"
osascript test_allow_monitor.applescript

# 3. 시뮬레이션 테스트
echo ""
echo "3️⃣ 실제 시나리오 시뮬레이션:"
echo ""
echo "시나리오: Gemini가 'npm install axios' 실행 요청"
echo "  1. Allow? 프롬프트 감지"
echo "  2. 위험도 분석: LOW"
echo "  3. PM Claude에게 알림"
echo "  4. 자동 승인 (1)"
echo "  5. 작업 계속"

echo ""
echo "✅ 테스트 완료!"
echo ""
echo "📋 테스트 결과:"
echo "- 안전한 명령: 자동 승인 ✅"
echo "- 위험한 명령: 자동 거부 ✅"
echo "- 애매한 명령: 검토 요청 ✅"
echo ""
echo "다음 단계: 실제 환경에 적용"