#!/bin/bash

# AI Orchestra CLI Controller
# tmux를 사용하여 여러 AI CLI를 관리하는 스크립트

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# CLI 세션 정의
declare -A CLI_SESSIONS=(
    ["claude"]="claude-cli"
    ["cursor"]="cursor-cli"
    ["codex"]="codex-cli"
    ["gemini"]="gemini-cli"
    ["vscode"]="vscode-cli"
)

# 함수: 모든 CLI 세션 시작
start_all_sessions() {
    echo -e "${BLUE}🚀 Starting all CLI sessions...${NC}"
    
    for cli in "${!CLI_SESSIONS[@]}"; do
        session_name="${CLI_SESSIONS[$cli]}"
        
        # 세션이 이미 존재하는지 확인
        if tmux has-session -t "$session_name" 2>/dev/null; then
            echo -e "${YELLOW}⚠️  Session $session_name already exists${NC}"
        else
            # 새 세션 생성
            tmux new-session -d -s "$session_name"
            
            # CLI 초기화 명령 전송
            case $cli in
                "claude")
                    tmux send-keys -t "$session_name" "claude" Enter
                    ;;
                "cursor")
                    tmux send-keys -t "$session_name" "cursor" Enter
                    ;;
                "codex")
                    tmux send-keys -t "$session_name" "codex" Enter
                    ;;
                "gemini")
                    tmux send-keys -t "$session_name" "gemini" Enter
                    ;;
                "vscode")
                    tmux send-keys -t "$session_name" "code ." Enter
                    ;;
            esac
            
            echo -e "${GREEN}✅ Started session: $session_name${NC}"
        fi
    done
}

# 함수: 특정 CLI에 메시지 전송
send_to_cli() {
    local cli_name=$1
    local message=$2
    
    session_name="${CLI_SESSIONS[$cli_name]}"
    
    if [ -z "$session_name" ]; then
        echo -e "${RED}❌ Unknown CLI: $cli_name${NC}"
        return 1
    fi
    
    if tmux has-session -t "$session_name" 2>/dev/null; then
        tmux send-keys -t "$session_name" "$message" Enter
        echo -e "${GREEN}📤 Sent to $cli_name: $message${NC}"
    else
        echo -e "${RED}❌ Session $session_name not found${NC}"
        return 1
    fi
}

# 함수: 모든 CLI에 브로드캐스트
broadcast_to_all() {
    local message=$1
    
    echo -e "${BLUE}📢 Broadcasting to all CLIs...${NC}"
    
    for cli in "${!CLI_SESSIONS[@]}"; do
        send_to_cli "$cli" "$message"
    done
}

# 함수: 이슈를 CLI에 할당
assign_issue() {
    local cli_name=$1
    local issue_number=$2
    local repo_name=$3
    
    echo -e "${BLUE}📋 Assigning Issue #$issue_number to $cli_name${NC}"
    
    # 알림 메시지
    send_to_cli "$cli_name" "📋 새로운 작업이 할당되었습니다: Issue #$issue_number"
    
    # GitHub CLI 명령
    send_to_cli "$cli_name" "gh issue view $issue_number -R $repo_name"
    
    # 작업 시작 안내
    send_to_cli "$cli_name" "작업을 시작하세요. 완료 후 이슈에 보고해주세요."
}

# 함수: CLI 상태 확인
check_status() {
    echo -e "${BLUE}📊 Checking CLI session status...${NC}"
    
    for cli in "${!CLI_SESSIONS[@]}"; do
        session_name="${CLI_SESSIONS[$cli]}"
        
        if tmux has-session -t "$session_name" 2>/dev/null; then
            echo -e "${GREEN}✅ $cli ($session_name): Active${NC}"
            
            # 현재 창의 내용 마지막 5줄 표시 (선택적)
            # echo "Last 5 lines:"
            # tmux capture-pane -t "$session_name" -p | tail -5
        else
            echo -e "${RED}❌ $cli ($session_name): Not running${NC}"
        fi
    done
}

# 함수: 협업 모드 시작
start_collaboration() {
    local topic=$1
    
    echo -e "${BLUE}🤝 Starting collaboration mode: $topic${NC}"
    
    # 모든 CLI에 협업 시작 알림
    broadcast_to_all "🤝 협업 모드 시작: $topic"
    broadcast_to_all "PR을 확인하고 할당된 챕터에 대해 의견을 제시해주세요."
}

# 함수: 세션 모니터링 (실시간)
monitor_sessions() {
    echo -e "${BLUE}👁️  Monitoring all sessions (Press Ctrl+C to exit)${NC}"
    
    # tmux 분할 창으로 모든 세션 모니터링
    tmux new-session -d -s monitor
    
    # 5개 창으로 분할
    tmux split-window -h -t monitor
    tmux split-window -v -t monitor:0.0
    tmux split-window -v -t monitor:0.1
    tmux split-window -v -t monitor:0.2
    
    # 각 창에서 다른 세션 모니터링
    local i=0
    for cli in "${!CLI_SESSIONS[@]}"; do
        session_name="${CLI_SESSIONS[$cli]}"
        tmux send-keys -t monitor:0.$i "tmux attach -t $session_name" Enter
        ((i++))
    done
    
    # 모니터 세션 연결
    tmux attach -t monitor
}

# 함수: 모든 세션 종료
stop_all_sessions() {
    echo -e "${YELLOW}⚠️  Stopping all CLI sessions...${NC}"
    
    for cli in "${!CLI_SESSIONS[@]}"; do
        session_name="${CLI_SESSIONS[$cli]}"
        
        if tmux has-session -t "$session_name" 2>/dev/null; then
            tmux kill-session -t "$session_name"
            echo -e "${GREEN}✅ Stopped session: $session_name${NC}"
        fi
    done
}

# 메인 메뉴
show_menu() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}   AI Orchestra CLI Controller  ${NC}"
    echo -e "${BLUE}================================${NC}"
    echo "1. Start all CLI sessions"
    echo "2. Send message to specific CLI"
    echo "3. Broadcast to all CLIs"
    echo "4. Assign issue to CLI"
    echo "5. Check status"
    echo "6. Start collaboration"
    echo "7. Monitor sessions"
    echo "8. Stop all sessions"
    echo "9. Exit"
    echo -e "${BLUE}================================${NC}"
}

# 메인 루프
main() {
    while true; do
        show_menu
        read -p "Select option: " choice
        
        case $choice in
            1)
                start_all_sessions
                ;;
            2)
                read -p "CLI name (claude/cursor/codex/gemini/vscode): " cli
                read -p "Message: " msg
                send_to_cli "$cli" "$msg"
                ;;
            3)
                read -p "Message to broadcast: " msg
                broadcast_to_all "$msg"
                ;;
            4)
                read -p "CLI name: " cli
                read -p "Issue number: " issue
                read -p "Repository (owner/repo): " repo
                assign_issue "$cli" "$issue" "$repo"
                ;;
            5)
                check_status
                ;;
            6)
                read -p "Collaboration topic: " topic
                start_collaboration "$topic"
                ;;
            7)
                monitor_sessions
                ;;
            8)
                stop_all_sessions
                ;;
            9)
                echo -e "${GREEN}👋 Goodbye!${NC}"
                exit 0
                ;;
            *)
                echo -e "${RED}Invalid option${NC}"
                ;;
        esac
        
        echo ""
        read -p "Press Enter to continue..."
    done
}

# 스크립트 실행
if [ "$1" == "--help" ] || [ "$1" == "-h" ]; then
    echo "Usage: $0 [command] [args]"
    echo ""
    echo "Commands:"
    echo "  start              - Start all CLI sessions"
    echo "  stop               - Stop all CLI sessions"
    echo "  send <cli> <msg>   - Send message to specific CLI"
    echo "  broadcast <msg>    - Broadcast message to all CLIs"
    echo "  status             - Check status of all sessions"
    echo ""
    echo "Without arguments, interactive menu will be shown."
    exit 0
fi

# 명령줄 인자 처리
case "$1" in
    "start")
        start_all_sessions
        ;;
    "stop")
        stop_all_sessions
        ;;
    "send")
        send_to_cli "$2" "$3"
        ;;
    "broadcast")
        broadcast_to_all "$2"
        ;;
    "status")
        check_status
        ;;
    *)
        main
        ;;
esac