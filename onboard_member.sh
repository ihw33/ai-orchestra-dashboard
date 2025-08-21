#!/bin/bash

# 새 팀원 온보딩 스크립트
# 사용법: ./onboard_member.sh [session_number] [member_name] [role]

SESSION=$1
NAME=$2
ROLE=$3

if [ -z "$SESSION" ] || [ -z "$NAME" ] || [ -z "$ROLE" ]; then
    echo "사용법: ./onboard_member.sh [session_number] [member_name] [role]"
    echo "예시: ./onboard_member.sh 2 Gemini 'Data Collection'"
    exit 1
fi

echo "🚀 새 팀원 온보딩 시작: $NAME"
echo "   역할: $ROLE"
echo "   세션: Tab 4, Session $SESSION"

# AppleScript 실행
osascript /Users/m4_macbook/Projects/ai-orchestra-dashboard/onboard_new_member.applescript "$SESSION" "$NAME" "$ROLE"

echo "✅ 온보딩 메시지 전송 완료"

# GitHub Issue 생성
gh issue create -R ihw33/ai-orchestra-dashboard \
    --title "🎉 신규 팀원: $NAME" \
    --body "## 새로운 팀원이 참가했습니다

**이름**: $NAME
**역할**: $ROLE
**세션**: Tab 4, Session $SESSION

### 온보딩 체크리스트
- [x] 환영 메시지 전송
- [x] 프로젝트 정보 제공
- [x] GitHub 정보 제공
- [x] 역할 안내
- [x] 가이드 문서 안내
- [ ] 첫 작업 할당

### 팀원 확인 사항
$NAME님, 이 Issue에 댓글로 확인 부탁드립니다:
\`\`\`bash
gh issue comment [이 Issue 번호] -R ihw33/ai-orchestra-dashboard --body '$NAME 온보딩 완료, 작업 준비 완료'
\`\`\`

@PM-Claude"

echo "✅ 온보딩 Issue 생성 완료"
echo "📋 팀원이 가이드를 숙지하고 확인 댓글을 남기기를 기다리세요"