#!/bin/bash

# CLI에 메시지 전송하는 스크립트
# 사용법: ./send_to_cli.sh [cli_name] [message]

CLI_NAME=$1
MESSAGE=$2

if [ -z "$CLI_NAME" ] || [ -z "$MESSAGE" ]; then
    echo "사용법: ./send_to_cli.sh [cli_name] [message]"
    echo "예시: ./send_to_cli.sh gemini '작업을 시작하세요'"
    exit 1
fi

# 파일 기반 메시지 전달 방식
MESSAGE_DIR="/Users/m4_macbook/.ai-orchestra/messages"
mkdir -p "$MESSAGE_DIR"

# 메시지 파일 생성
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
MESSAGE_FILE="$MESSAGE_DIR/${CLI_NAME}_${TIMESTAMP}.txt"

echo "📋 PM Claude로부터 메시지:" > "$MESSAGE_FILE"
echo "$MESSAGE" >> "$MESSAGE_FILE"
echo "" >> "$MESSAGE_FILE"
echo "시간: $(date)" >> "$MESSAGE_FILE"

echo "✅ 메시지를 $CLI_NAME에게 전송했습니다: $MESSAGE_FILE"

# 알림 사운드 (macOS)
afplay /System/Library/Sounds/Glass.aiff 2>/dev/null || true

echo "📁 메시지 위치: $MESSAGE_FILE"