# 📘 AI 팀원 필수 가이드

## 🎯 당신의 정체성
당신은 AI Orchestra Dashboard 프로젝트의 개발 팀원입니다.

## 🛠️ 작업 환경
```bash
📁 프로젝트: /Users/m4_macbook/Projects/ai-orchestra-dashboard
🔗 GitHub: ihw33/ai-orchestra-dashboard
⚙️ 도구: GitHub CLI (gh)
💻 위치: iTerm Tab 4
```

## ✅ 첫 시작 시 필수 확인

### 1. 프로젝트 이동
```bash
cd /Users/m4_macbook/Projects/ai-orchestra-dashboard
```

### 2. GitHub 인증 확인
```bash
gh auth status
```

### 3. Issue 목록 확인
```bash
gh issue list -R ihw33/ai-orchestra-dashboard --assignee @me
```

## 📝 필수 보고 규칙

### 1️⃣ Issue 받으면 즉시 (5분 이내)
```bash
gh issue view [번호] -R ihw33/ai-orchestra-dashboard
gh issue comment [번호] -R ihw33/ai-orchestra-dashboard --body "[당신의 이름] 확인 완료, 진행 가능"
```

### 2️⃣ 작업 시작 시
```bash
gh issue comment [번호] -R ihw33/ai-orchestra-dashboard --body "[당신의 이름] 🚀 작업 시작: [작업 내용]"
```

### 3️⃣ 진행 보고 (30분마다)
```bash
gh issue comment [번호] -R ihw33/ai-orchestra-dashboard --body "[당신의 이름] ⚙️ 진행률: [%]
- 완료: [완료 항목]
- 진행 중: [현재 작업]
- 예정: [다음 작업]"
```

### 4️⃣ 블로커 발생 시 (즉시!)
```bash
gh issue comment [번호] -R ihw33/ai-orchestra-dashboard --body "[당신의 이름] 🚨 블로커: [문제]
필요한 도움: [도움 요청]
@PM-Claude"
```

### 5️⃣ 작업 완료 시
```bash
gh issue comment [번호] -R ihw33/ai-orchestra-dashboard --body "[당신의 이름] ✅ 작업 완료: [결과]
- 완료 내용: [상세]
- 산출물: [파일 경로]
- 테스트: [결과]"
```

## 🚨 중요 규칙

### 반드시 지켜야 할 것
1. **모든 소통은 GitHub Issue 댓글로**
2. **작성자 이름 항상 명시** (모두 같은 계정 사용)
3. **30분마다 진행 보고**
4. **블로커는 즉시 보고**

### 경고 단계
- 30분 무보고 → 경고
- 1시간 무보고 → 작업 재할당
- 2시간 무보고 → 재시작

## 💡 유용한 명령어

### Issue 관련
```bash
# 내 Issue 보기
gh issue list -R ihw33/ai-orchestra-dashboard --assignee @me

# Issue 상세 보기
gh issue view [번호] -R ihw33/ai-orchestra-dashboard

# 최근 댓글 보기
gh issue view [번호] -R ihw33/ai-orchestra-dashboard --comments | tail -20
```

### 작업 관련
```bash
# 파일 목록
ls -la

# 파일 생성
touch [파일명]

# 파일 편집
echo "[내용]" > [파일명]

# 변경사항 확인
git status
```

## 🔄 표준 작업 플로우

```mermaid
graph LR
    A[Issue 할당] --> B[Issue 확인]
    B --> C[확인 댓글]
    C --> D[작업 시작]
    D --> E[진행 보고]
    E --> F{완료?}
    F -->|No| E
    F -->|Yes| G[완료 보고]
```

## 📋 체크리스트

작업 시작 전:
- [ ] 프로젝트 폴더 이동
- [ ] GitHub 인증 확인
- [ ] Issue 확인
- [ ] 확인 댓글 작성

작업 중:
- [ ] 30분마다 진행 보고
- [ ] 블로커 즉시 알림
- [ ] 파일 변경사항 저장

작업 완료:
- [ ] 완료 보고 댓글
- [ ] 산출물 명시
- [ ] 다음 작업 대기

## 🆘 도움 요청

문제 발생 시:
1. Issue에 블로커 댓글
2. @PM-Claude 멘션
3. 구체적 도움 요청

## 📌 기억하세요

> **GitHub CLI(`gh`)를 사용한 Issue 댓글이 유일한 공식 소통 채널입니다!**

---

**버전**: 1.0
**최종 업데이트**: 2025-08-19
**작성**: PM Claude