# 📝 Issue 보고 규칙 (필수)

## 🔴 절대 규칙: Issue 댓글이 생명

모든 팀원은 **반드시** GitHub Issue에 다음을 보고해야 합니다:

## 1️⃣ 작업 시작 시 (즉시)
```bash
gh issue comment [ISSUE_NUMBER] --body "[팀원명 보고] 🚀 작업 시작: [작업 내용]
예상 완료 시간: [시간]
현재 상태: [상태]"
```

## 2️⃣ 진행 중 (30분마다)
```bash
gh issue comment [ISSUE_NUMBER] --body "[팀원명 보고] ⚙️ 진행 중: 
- 완료: [완료된 작업]
- 진행중: [현재 작업]
- 남은 작업: [남은 작업]
- 진행률: [%]"
```

## 3️⃣ 블로커 발생 시 (즉시)
```bash
gh issue comment [ISSUE_NUMBER] --body "🚨 블로커: 
문제: [문제 설명]
필요한 도움: [도움 요청]
@PM-Claude"
```

## 4️⃣ 작업 완료 시 (즉시)
```bash
gh issue comment [ISSUE_NUMBER] --body "✅ 작업 완료:
- 완료 내용: [완료 내용]
- 산출물: [파일 경로]
- 테스트 결과: [결과]
- PR: #[PR 번호]"
```

## 📊 PM 모니터링 체크리스트

### 5분마다 체크
- [ ] 모든 Issue에 최근 30분 내 댓글이 있는가?
- [ ] 블로커 댓글이 있는가?
- [ ] 진행률이 정체되어 있지 않은가?

### 댓글이 없으면
1. CLI에 직접 확인 요청
2. 10분 대기
3. 응답 없으면 작업 재할당

## 🎯 예시

### Codex (Issue #4)
```bash
# 시작
gh issue comment 4 --body "🚀 작업 시작: Backend API 구현
예상 완료 시간: 1시간
현재 상태: FastAPI 라우터 설정 중"

# 30분 후
gh issue comment 4 --body "⚙️ 진행 중:
- 완료: projects router 생성
- 진행중: GitHub service 구현
- 남은 작업: WebSocket 설정
- 진행률: 60%"

# 완료
gh issue comment 4 --body "✅ 작업 완료:
- 완료 내용: 모든 API 엔드포인트 구현
- 산출물: backend/app/routers/projects.py
- 테스트 결과: 200 OK
- PR: #9"
```

## ⚠️ 경고

**30분 이상 보고가 없으면:**
1. 경고 메시지 발송
2. 1시간 무응답 시 작업 재할당
3. 2시간 무응답 시 CLI 재시작

---

**이 규칙은 필수입니다. 준수하지 않으면 프로젝트에서 제외됩니다.**

작성: PM Claude
적용: 즉시