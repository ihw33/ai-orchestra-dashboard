#!/bin/bash

# Smart Auto Confirm - Bash Command 자동 확인 스크립트
# 백그라운드에서 실행하여 주기적으로 체크하고 자동 응답

# PID 파일로 중복 실행 방지
PIDFILE="/tmp/ai_orchestra_auto_confirm.pid"

# 이미 실행 중인지 확인
if [ -f "$PIDFILE" ]; then
    if ps -p $(cat "$PIDFILE") > /dev/null 2>&1; then
        echo "Already running with PID $(cat $PIDFILE)"
        exit 1
    fi
fi

# PID 저장
echo $$ > "$PIDFILE"

# 종료 시 PID 파일 삭제
trap "rm -f $PIDFILE" EXIT

echo "🤖 Smart Auto Confirm 시작"
echo "모니터링 세션: 2(PM Claude), 3(Gemini), 4(Codex)"
echo "체크 간격: 5초"
echo "중지하려면: kill $$"
echo "================================"

# 각 세션의 마지막 응답 시간 추적
declare -A last_response
last_response[2]=0
last_response[3]=0
last_response[4]=0

# 메인 루프
while true; do
    current_time=$(date +%s)
    
    for session in 2 3 4; do
        # 각 세션의 이름
        case $session in
            2) name="PM_Claude" ;;
            3) name="Gemini" ;;
            4) name="Codex" ;;
        esac
        
        # 마지막 응답으로부터 경과 시간
        elapsed=$((current_time - last_response[$session]))
        
        # 10초 이상 경과했으면 체크 (너무 자주 체크하지 않도록)
        if [ $elapsed -gt 10 ]; then
            echo "[$(date '+%H:%M:%S')] Checking $name (Session $session)..."
            
            # 세션에 Enter 보내서 프롬프트 확인
            osascript -e "
            tell application \"iTerm\"
                tell window 1
                    tell current tab
                        if (count of sessions) ≥ $session then
                            tell session $session
                                write text \"\"
                                delay 1
                                -- Bash command 프롬프트가 나타났을 가능성
                                write text \"1\"
                                write text \"\"
                            end tell
                        end if
                    end tell
                end tell
            end tell
            " 2>/dev/null
            
            # 응답 시간 업데이트
            last_response[$session]=$current_time
            
            # 알림 (선택적)
            # osascript -e "display notification \"Auto confirmed for $name\" with title \"AI Orchestra\""
        fi
    done
    
    # 5초 대기
    sleep 5
done