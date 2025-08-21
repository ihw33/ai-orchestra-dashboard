# ✅ PM 필수 체크리스트

## 🔴 Thomas님 지시사항 (절대 준수)

### 1. CLI 프롬프트 입력 시
- [ ] 프롬프트 텍스트 입력
- [ ] **반드시 엔터키 실행** (keystroke return)
- [ ] 응답 확인

### 2. Issue 관리
- [ ] 모든 소통은 GitHub Issue 댓글로
- [ ] AppleScript는 Issue 번호만 알려주기
- [ ] 댓글 작성 후 팀원에게 "Issue #X 확인" 알림

### 3. 모니터링 (5분마다)
- [ ] 각 팀원 CLI 화면 확인
- [ ] Issue 댓글 확인
- [ ] 파일 변경 확인
- [ ] 5분 이상 동작 없으면 즉시 체크

### 4. 보고 체계
- [ ] 작업 시작: 🚀 댓글
- [ ] 30분마다: ⚙️ 진행 상황
- [ ] 블로커: 🚨 즉시 보고
- [ ] 완료: ✅ 완료 보고

### 5. 의사결정
- [ ] 모든 결정은 초안 → 검토 → 승인
- [ ] 문서로 남기기 (DECISION_LOG.md)
- [ ] Thomas 승인 없이 진행 금지

### 6. 팀원 관리
- [ ] 30분 무보고 → 경고
- [ ] 1시간 무보고 → 작업 재할당
- [ ] 2시간 무보고 → CLI 재시작

## 📋 매 작업 시 체크

### AppleScript 실행 시
```applescript
1. tell application "iTerm"
2. tell session X
3. write text "프롬프트"
4. end tell
5. tell application "System Events"
6. keystroke return  ← 절대 잊지 말 것!
7. end tell
```

### Issue 댓글 후
1. GitHub에 댓글 작성
2. 팀원 CLI에 "Issue #X 확인" 프롬프트
3. 엔터키 실행
4. 5분 후 응답 확인

### 모니터링 스크립트
```bash
./monitor_team.sh  # 5분마다 실행
```

## 🚨 자주 하는 실수

### ❌ 하지 말아야 할 것
- PM/PD인데 직접 코딩
- 팀원에게 긴 지시 (Issue 번호만!)
- 엔터키 빼먹기
- Thomas 승인 없이 진행

### ✅ 반드시 해야 할 것
- 5분마다 모니터링
- Issue 댓글 확인
- 파일 변경 추적
- 팀원 응답 체크

## 📊 현재 진행 상황 추적

### Round 1 (오늘)
- [ ] Issue #4: Backend API (Codex) - 진행 중
- [ ] Issue #5: Data Collection (Gemini) - 진행 중
- [ ] Issue #6: Frontend (VSCode Claude) - 시작 대기
- [ ] Issue #7: Design (Cursor) - 시작 대기
- [ ] Issue #8: Round 1 Epic - 관리 중
- [ ] Issue #9: 보고 규칙 - 공지 완료

## 🔄 5분마다 실행

1. **CLI 상태 체크**
```bash
osascript -e 'tell app "iTerm" to get name of sessions of tab 4'
```

2. **Issue 댓글 체크**
```bash
for i in 4 5 6 7; do
  gh issue view $i --comments | tail -5
done
```

3. **파일 변경 체크**
```bash
find . -name "*.py" -o -name "*.ts" -mmin -5
```

---

**마지막 업데이트**: 2025-08-19 12:32
**다음 체크**: 5분 후 (12:37)