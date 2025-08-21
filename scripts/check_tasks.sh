#!/bin/bash

# CLI가 자신의 작업을 확인하는 스크립트
CLI_NAME=$1

if [ -z "$CLI_NAME" ]; then
    echo "사용법: ./check_tasks.sh [cli_name]"
    exit 1
fi

TASK_DIR="/Users/m4_macbook/.ai-orchestra/tasks/$CLI_NAME"

echo "📋 $CLI_NAME의 할당된 작업:"
echo "================================"

if [ -d "$TASK_DIR" ] && [ "$(ls -A $TASK_DIR)" ]; then
    for task_file in $TASK_DIR/*.json; do
        if [ -f "$task_file" ]; then
            echo ""
            echo "🔹 $(basename $task_file):"
            cat "$task_file" | python3 -m json.tool
            echo "--------------------------------"
        fi
    done
else
    echo "할당된 작업이 없습니다."
fi