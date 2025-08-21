# 📋 AI Orchestra 소통 규칙

## 🚨 핵심 원칙
**모든 업무 소통은 GitHub Issue 댓글로만 진행**

## 필수 규칙

### 1. 작업 시작 시
```bash
gh issue comment [ISSUE_NUMBER] -R ihw33/ai-orchestra-dashboard -b "[이름]: 작업 시작합니다. [작업 내용]"
```

### 2. 진행 상황 보고 (매 30분)
```bash
gh issue comment [ISSUE_NUMBER] -R ihw33/ai-orchestra-dashboard -b "[이름]: 진행률 XX%. [현재 작업 내용]"
```

### 3. 완료 보고
```bash
gh issue comment [ISSUE_NUMBER] -R ihw33/ai-orchestra-dashboard -b "[이름]: ✅ 작업 완료. [결과 요약]"
```

### 4. 문제/블로커 보고
```bash
gh issue comment [ISSUE_NUMBER] -R ihw33/ai-orchestra-dashboard -b "[이름]: ⚠️ 이슈 발생. [문제 설명]. 도움 필요."
```

### 5. 질문/확인 요청
```bash
gh issue comment [ISSUE_NUMBER] -R ihw33/ai-orchestra-dashboard -b "[이름]: ❓ 질문. [질문 내용] @[담당자]"
```

## 역할별 책임

- **PM Claude**: Issue 모니터링, 팀원 작업 조율
- **Codex**: 백엔드 개발 진행 상황 보고
- **Gemini**: 문서화 진행 상황 보고
- **Orchestra (나)**: Issue 댓글 확인 후 지시/승인

## 금지 사항
- ❌ 채팅으로 업무 논의
- ❌ 직접 파일 수정 without Issue 보고
- ❌ Issue 댓글 없이 작업 진행