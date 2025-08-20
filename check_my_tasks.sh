#\!/bin/bash

# AI 팀원이 자신의 작업을 확인하는 스크립트
TEAM_MEMBER=$1

if [ -z "$TEAM_MEMBER" ]; then
    echo "Usage: ./check_my_tasks.sh [codex|gemini|vscode-claude|cursor-chatgpt]"
    exit 1
fi

echo "🤖 $TEAM_MEMBER 작업 목록"
echo "========================"

# 라벨로 필터링하여 자신의 이슈만 보기
gh issue list -R ihw33/ai-orchestra-dashboard \
    --label "$TEAM_MEMBER" \
    --state open \
    --json number,title,labels,body \
    --jq '.[] | "Issue #\(.number): \(.title)\nPriority: \(.labels | map(select(.name | contains("p"))) | .[0].name // "none")\nStatus: TODO\n---"'

echo ""
echo "📋 작업 방법:"
echo "1. Issue 확인: gh issue view [번호] -R ihw33/ai-orchestra-dashboard"
echo "2. 작업 시작: gh issue comment [번호] -R ihw33/ai-orchestra-dashboard --body '[ACK] 작업 확인'"
echo "3. 진행 보고: gh issue comment [번호] -R ihw33/ai-orchestra-dashboard --body '[START] 작업 시작'"
echo "4. 완료 보고: gh issue comment [번호] -R ihw33/ai-orchestra-dashboard --body '[DONE] PR #번호'"
