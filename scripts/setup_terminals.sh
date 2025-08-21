#!/bin/bash

# 🎯 AI Orchestra 터미널 설정 스크립트
# 각 터미널에 이름을 설정하고 tmux 세션을 생성합니다

echo "🚀 AI Orchestra Terminal Setup"
echo "================================"

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 터미널 번호 확인
echo -e "${BLUE}어느 터미널을 설정하시겠습니까?${NC}"
echo "1) 터미널 1 - Control Center (현재 메인)"
echo "2) 터미널 2 - PM Claude" 
echo "3) 터미널 3 - Worker CLI 1"
echo "4) 터미널 4 - Worker CLI 2"
echo -n "선택 (1-4): "
read terminal_num

case $terminal_num in
    1)
        # 터미널 1: Control Center
        echo -e "${GREEN}✅ Terminal 1: Control Center${NC}"
        echo -e "${YELLOW}이 터미널은 대시보드 제어용입니다${NC}"
        
        # iTerm2 탭 이름 설정
        echo -e "\033]0;🎮 Control Center\007"
        
        # 프롬프트 커스터마이징
        export PS1="🎮 Control> "
        
        echo "설정 완료! 이제 대시보드를 제어할 수 있습니다."
        echo "브라우저: http://localhost:3000"
        ;;
        
    2)
        # 터미널 2: PM Claude
        echo -e "${GREEN}✅ Terminal 2: PM Claude${NC}"
        echo -e "${YELLOW}PM 역할을 할 Claude를 설정합니다${NC}"
        
        # iTerm2 탭 이름 설정
        echo -e "\033]0;👔 PM Claude\007"
        
        # tmux 세션 생성 또는 연결
        if tmux has-session -t pm-claude 2>/dev/null; then
            echo "기존 pm-claude 세션에 연결합니다..."
            tmux attach-session -t pm-claude
        else
            echo "새 pm-claude 세션을 생성합니다..."
            tmux new-session -s pm-claude -n "PM" \; \
                send-keys "cd ~/ai-orchestra-dashboard" C-m \; \
                send-keys "export PS1='👔 PM> '" C-m \; \
                send-keys "clear" C-m \; \
                send-keys "echo '👔 PM Claude 준비 완료!'" C-m \; \
                send-keys "echo '이제 claude 명령을 실행하세요'" C-m
        fi
        ;;
        
    3)
        # 터미널 3: Worker CLI 1
        echo -e "${GREEN}✅ Terminal 3: Worker CLI 1${NC}"
        echo -e "${YELLOW}첫 번째 작업자 CLI를 설정합니다${NC}"
        
        # iTerm2 탭 이름 설정
        echo -e "\033]0;🤖 Worker 1\007"
        
        # CLI 선택
        echo "어떤 CLI를 실행하시겠습니까?"
        echo "1) Cursor (ChatGPT)"
        echo "2) Codex (Backend)"
        echo "3) Gemini (Content)"
        echo "4) Test CLI (테스트용)"
        echo -n "선택: "
        read cli_choice
        
        case $cli_choice in
            1)
                session_name="cursor-cli"
                cli_name="Cursor"
                cli_cmd="cursor"
                emoji="🎯"
                ;;
            2)
                session_name="codex-cli"
                cli_name="Codex"
                cli_cmd="codex"
                emoji="⚙️"
                ;;
            3)
                session_name="gemini-cli"
                cli_name="Gemini"
                cli_cmd="gemini"
                emoji="✨"
                ;;
            4)
                session_name="test-cli"
                cli_name="Test"
                cli_cmd="echo 'Test CLI 대기 중...'"
                emoji="🧪"
                ;;
            *)
                session_name="worker1-cli"
                cli_name="Worker1"
                cli_cmd="echo 'Worker 1 대기 중...'"
                emoji="🤖"
                ;;
        esac
        
        if tmux has-session -t $session_name 2>/dev/null; then
            echo "기존 $session_name 세션에 연결합니다..."
            tmux attach-session -t $session_name
        else
            echo "새 $session_name 세션을 생성합니다..."
            tmux new-session -s $session_name -n "$cli_name" \; \
                send-keys "cd ~/ai-orchestra-dashboard" C-m \; \
                send-keys "export PS1='$emoji $cli_name> '" C-m \; \
                send-keys "clear" C-m \; \
                send-keys "echo '$emoji $cli_name CLI 준비 완료!'" C-m \; \
                send-keys "echo '명령 대기 중...'" C-m
        fi
        ;;
        
    4)
        # 터미널 4: Worker CLI 2
        echo -e "${GREEN}✅ Terminal 4: Worker CLI 2${NC}"
        echo -e "${YELLOW}두 번째 작업자 CLI를 설정합니다${NC}"
        
        # iTerm2 탭 이름 설정
        echo -e "\033]0;🔧 Worker 2\007"
        
        # 터미널 3과 동일한 로직
        echo "어떤 CLI를 실행하시겠습니까?"
        echo "1) Cursor (ChatGPT)"
        echo "2) Codex (Backend)"
        echo "3) Gemini (Content)"
        echo "4) VSCode Claude"
        echo "5) Test CLI (테스트용)"
        echo -n "선택: "
        read cli_choice
        
        case $cli_choice in
            1)
                session_name="cursor-cli"
                cli_name="Cursor"
                emoji="🎯"
                ;;
            2)
                session_name="codex-cli"
                cli_name="Codex"
                emoji="⚙️"
                ;;
            3)
                session_name="gemini-cli"
                cli_name="Gemini"
                emoji="✨"
                ;;
            4)
                session_name="vscode-cli"
                cli_name="VSCode"
                emoji="📝"
                ;;
            5)
                session_name="test-cli-2"
                cli_name="Test2"
                emoji="🧪"
                ;;
            *)
                session_name="worker2-cli"
                cli_name="Worker2"
                emoji="🔧"
                ;;
        esac
        
        if tmux has-session -t $session_name 2>/dev/null; then
            echo "기존 $session_name 세션에 연결합니다..."
            tmux attach-session -t $session_name
        else
            echo "새 $session_name 세션을 생성합니다..."
            tmux new-session -s $session_name -n "$cli_name" \; \
                send-keys "cd ~/ai-orchestra-dashboard" C-m \; \
                send-keys "export PS1='$emoji $cli_name> '" C-m \; \
                send-keys "clear" C-m \; \
                send-keys "echo '$emoji $cli_name CLI 준비 완료!'" C-m \; \
                send-keys "echo '명령 대기 중...'" C-m
        fi
        ;;
        
    *)
        echo -e "${RED}잘못된 선택입니다${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}================================${NC}"
echo -e "${BLUE}설정 완료!${NC}"
echo ""
echo "💡 다음 단계:"
echo "1. 각 터미널에서 이 스크립트를 실행하세요"
echo "2. PM Claude 터미널에서: claude 실행"
echo "3. Worker 터미널에서: 해당 CLI 실행"
echo "4. Control Center에서: 대시보드 모니터링"
echo ""
echo "📌 tmux 명령어:"
echo "  • 세션 나가기: Ctrl+b, d"
echo "  • 세션 재연결: tmux attach -t [세션명]"
echo "  • 세션 목록: tmux list-sessions"