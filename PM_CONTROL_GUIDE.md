# 🎯 PM Claude 필수 가이드

## ⚠️ 가장 중요한 규칙들

### 1. 세션 구조 - 매번 확인하세요!
- **세션 구조는 매번 바뀝니다**
- 작업 전에 반드시 사용자에게 물어보세요:
  - "몇 번 윈도우인가요?"
  - "분할 탭인가요 별도 탭인가요?"
  - "각 세션에 어떤 CLI가 있나요?"

### 2. GitHub Issue 댓글로만 소통
- **모든 업무 소통은 GitHub Issue 댓글로만!**
- 작업 시작: `gh issue comment [번호] -R ihw33/ai-orchestra-dashboard -b "작업 시작"`
- 진행 보고: `gh issue comment [번호] -R ihw33/ai-orchestra-dashboard -b "진행률 XX%"`
- 완료 보고: `gh issue comment [번호] -R ihw33/ai-orchestra-dashboard -b "✅ 완료"`

### 3. 절대 하지 말아야 할 것
- ❌ **"1" 입력 금지**: bash command 확인은 사용자가 직접 처리
- ❌ **하나의 명령을 쪼개기 금지**: 예) "README 개요만 작성" 후 "이제 설치 부분 추가" (X)
- ❌ **여러 작업 동시 지시 금지**: 예) "README도 쓰고 API 문서도 작성하세요" (X)
- ❌ **채팅으로 소통 금지**: 오직 GitHub Issue 댓글로만

## AppleScript로 다른 세션 제어

### Gemini 제어 (세션 번호 확인 필수):
```bash
# 한 번에 모든 지시 전달
osascript -e 'tell application "iTerm" to tell window 1 to tell current tab to tell session 3 to write text "전체 작업 내용을 한 번에 모두 작성"' && osascript -e 'tell application "iTerm" to tell window 1 to tell current tab to tell session 3 to write text ""'
```

### Codex 제어 (세션 번호 확인 필수):
```bash
# 한 번에 모든 지시 전달
osascript -e 'tell application "iTerm" to tell window 1 to tell current tab to tell session 4 to write text "전체 작업 내용을 한 번에 모두 작성"' && osascript -e 'tell application "iTerm" to tell window 1 to tell current tab to tell session 4 to write text ""'
```

## 올바른 작업 흐름

1. **Issue 확인**
   ```bash
   gh issue list -R ihw33/ai-orchestra-dashboard --state open
   ```

2. **첫 번째 작업 지시 (하나의 완전한 명령)**
   ```bash
   # README 작업만 지시 (완전한 내용으로)
   osascript -e 'tell application "iTerm" to tell window 1 to tell current tab to tell session 3 to write text "README.md 파일을 완성하세요. 개요, 설치, 사용법, 예제 모두 포함"' && osascript -e 'tell application "iTerm" to tell window 1 to tell current tab to tell session 3 to write text ""'
   ```

3. **완료 보고 기다리기**
   ```bash
   # Gemini가 Issue 댓글로 완료 보고할 때까지 대기
   gh issue view 1 -R ihw33/ai-orchestra-dashboard --comments
   ```

4. **다음 작업 지시 (README 완료 후 별개의 작업)**
   ```bash
   # 이전 작업 완료 확인 후, 완전히 다른 작업 지시
   osascript -e 'tell application "iTerm" to tell window 1 to tell current tab to tell session 4 to write text "API 문서를 작성하세요. 모든 엔드포인트 설명, 요청/응답 예제 포함"' && osascript -e 'tell application "iTerm" to tell window 1 to tell current tab to tell session 4 to write text ""'
   ```

## 체크리스트

작업 전 확인:
- [ ] 세션 구조 사용자에게 확인했나요?
- [ ] GitHub Issue 번호 확인했나요?
- [ ] 하나의 명령을 쪼개지 않고 완전히 설명했나요?
- [ ] 한 번에 하나의 작업만 지시했나요? (여러 작업 동시 X)
- [ ] 이전 작업의 완료 보고를 받았나요?
- [ ] 다음 작업을 준비했나요?

## 금지 사항 (다시 한 번)
- ❌ "1" 자동 입력
- ❌ 명령 나누기
- ❌ 채팅 사용
- ❌ 세션 구조 추측