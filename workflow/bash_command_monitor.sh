#!/bin/bash

# Bash Command 모니터링 및 자동 처리
# iTerm2 세션을 모니터링하고 bash command가 감지되면 알림

set -e

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 모니터링할 세션 목록
SESSIONS=(2 3 4)  # PM Claude, Gemini, Codex
SESSION_NAMES=("PM_Claude" "Gemini" "Codex")

# 알림 함수
notify() {
    local session_name=$1
    local message=$2
    
    # macOS 알림
    osascript -e "display notification \"$message\" with title \"🔔 AI Orchestra\" subtitle \"$session_name\""
    
    # 터미널 출력
    echo -e "${YELLOW}[$(date '+%H:%M:%S')] 🔔 $session_name: $message${NC}"
    
    # 로그 파일에 기록
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $session_name: $message" >> /tmp/ai_orchestra_alerts.log
}

# 자동 응답 함수
auto_respond() {
    local session_num=$1
    local session_name=$2
    
    echo -e "${GREEN}자동 응답: Session $session_num ($session_name)${NC}"
    
    osascript -e "
    tell application \"iTerm\"
        tell window 1
            tell current tab
                tell session $session_num
                    delay 0.5
                    write text \"1\"
                    write text \"\" -- 엔터
                end tell
            end tell
        end tell
    end tell
    "
}

# 세션 상태 확인 함수
check_session_for_bash_command() {
    local session_num=$1
    local session_name=$2
    
    # iTerm2 세션의 현재 내용을 확인 (이 부분은 실제로는 더 복잡한 구현 필요)
    # AppleScript로 세션 내용을 가져오기는 제한적이므로, 
    # 대신 정기적으로 체크하는 방식 사용
    
    # 여기서는 시뮬레이션
    echo -e "${BLUE}Checking session $session_num ($session_name)...${NC}"
}

# 메인 모니터링 루프
monitor_sessions() {
    echo -e "${GREEN}🚀 AI Orchestra Bash Command Monitor 시작${NC}"
    echo "모니터링 중: ${SESSION_NAMES[*]}"
    echo "자동 응답 모드: ON"
    echo "----------------------------------------"
    
    while true; do
        for i in "${!SESSIONS[@]}"; do
            session_num=${SESSIONS[$i]}
            session_name=${SESSION_NAMES[$i]}
            
            # 각 세션 체크
            check_session_for_bash_command $session_num $session_name
        done
        
        # 5초마다 체크
        sleep 5
    done
}

# 옵션 처리
case "${1:-}" in
    start)
        monitor_sessions
        ;;
    auto)
        # 특정 세션에 자동 응답
        if [[ -n "${2:-}" ]]; then
            auto_respond $2 "Manual"
        else
            echo "Usage: $0 auto <session_number>"
        fi
        ;;
    notify)
        # 테스트 알림
        notify "Test" "Bash command detected!"
        ;;
    *)
        echo "AI Orchestra Bash Command Monitor"
        echo "Usage: $0 {start|auto|notify}"
        echo ""
        echo "  start  - 모니터링 시작"
        echo "  auto   - 특정 세션 자동 응답"
        echo "  notify - 테스트 알림"
        ;;
esac