# 📋 AI Orchestra 작업 프로세스 체크리스트

## ✅ 이슈 작업 시작 시 (MUST DO)

### 1. Branch 생성
- [ ] `git checkout -b feature/issue-{번호}-{설명}`
- [ ] 예: `feature/issue-53-iterm2-api`

### 2. GitHub Issue 확인
- [ ] 이슈 번호 확인
- [ ] 담당자 할당 확인
- [ ] 라벨 확인

### 3. AI 팀원 할당 시
- [ ] 작업 내용 명확히 전달
- [ ] GitHub Issue 번호 포함
- [ ] 예상 시간 명시
- [ ] 우선순위 전달

### 4. 작업 진행 중
- [ ] 30분마다 진행 상황 체크
- [ ] 블로커 확인
- [ ] GitHub Issue 댓글 업데이트

### 5. 작업 완료 시
- [ ] 코드 커밋
- [ ] PR 생성
- [ ] Issue 링크 연결
- [ ] 리뷰어 할당

## 🚨 자주 놓치는 것들

1. **Branch 생성 잊음** ← 가장 많이 놓침!
2. **PR 생성 안함**
3. **Issue 댓글 업데이트 안함**
4. **엔터키 자동 전송 안됨**
5. **토큰 만료 체크 안함**

## 📝 Round 3 현재 상황

| 작업 | 담당 | Branch | PR |
|------|------|--------|-----|
| #53 iTerm2 API | Claude | feature/issue-53-iterm2-api | ❌ 생성 필요 |
| #45 라벨→세션 | Codex | ❌ 필요 | ❌ |
| #46 세션 ID | Gemini | ❌ 필요 | ❌ |

## 🔄 프로세스 개선 필요

- PL Bot으로 자동 체크
- Branch 자동 생성
- PR 템플릿 활용
- 체크리스트 자동화