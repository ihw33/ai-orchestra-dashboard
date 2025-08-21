#!/bin/bash

# CLI가 메시지를 확인하는 스크립트
# 각 CLI 터미널에서 주기적으로 실행

CLI_NAME=$1

if [ -z "$CLI_NAME" ]; then
    echo "사용법: ./check_messages.sh [cli_name]"
    echo "예시: ./check_messages.sh gemini"
    exit 1
fi

MESSAGE_DIR="/Users/m4_macbook/.ai-orchestra/messages"
PROCESSED_DIR="/Users/m4_macbook/.ai-orchestra/processed"
mkdir -p "$MESSAGE_DIR" "$PROCESSED_DIR"

echo "📬 새 메시지 확인 중..."

# 새 메시지 찾기
shopt -s nullglob  # 파일이 없을 때 에러 방지
for file in "$MESSAGE_DIR"/${CLI_NAME}_*.txt; do
    if [ -f "$file" ]; then
        echo ""
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        cat "$file"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
        
        # 처리됨으로 이동
        mv "$file" "$PROCESSED_DIR/"
    fi
done

# 새 메시지가 없으면
if [ ! "$(ls -A $MESSAGE_DIR/${CLI_NAME}_*.txt 2>/dev/null)" ]; then
    echo "새 메시지가 없습니다."
fi