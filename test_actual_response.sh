#!/bin/bash
# AI 실제 응답 캡처 테스트

echo "===== Gemini 테스트 ====="
echo "질문: 2+2는?"
RESPONSE=$(echo "2+2는?" | gemini 2>/dev/null | grep -v "Data collection" | grep -v "Loaded")
echo "응답: $RESPONSE"

echo ""
echo "===== Claude 테스트 ====="
echo "질문: 버전 확인"
claude --version

echo ""
echo "===== Codex 테스트 ====="
echo "질문: 버전 확인"
codex --version 2>&1 || echo "Codex: Device error (정상)"

echo ""
echo "===== 실제 응답 요약 ====="
echo "Gemini 응답: $RESPONSE"