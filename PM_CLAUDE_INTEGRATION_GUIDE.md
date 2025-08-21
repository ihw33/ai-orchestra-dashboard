# 🎯 AI Orchestra Dashboard - PM Claude 통합 실전 시나리오

## 📋 전체 워크플로우 개요
PM Claude(터미널)가 중앙 지휘자가 되어 다른 AI CLI들을 관리하는 시스템

---

## 🚀 Step 1: PM Claude 연동 (가장 중요!)

### 1-1. PM Claude 터미널 준비
```bash
# 1. 새 터미널 창 열기
# 2. tmux 세션 생성 (이름: claude-cli)
tmux new-session -s claude-cli

# 3. 프로젝트 디렉토리로 이동
cd ~/ai-orchestra-dashboard

# 4. Claude Code 실행
claude
```

### 1-2. PM Claude 역할 인식시키기
Claude에게 다음 메시지 전송:
```
당신은 이제 PM AI입니다. 다음 역할을 수행합니다:
- GitHub 이슈 관리 및 분석
- 다른 AI CLI들에게 작업 할당
- 프로젝트 전체 진행 상황 모니터링
- ai-orchestra-dashboard를 통해 모든 것을 제어

현재 저장소: ihw33/iwl-v5-rebuild
```

### 1-3. 대시보드에서 PM Claude 등록 확인
```bash
# 브라우저에서 http://localhost:3000 접속
# PM Control 탭 클릭
# "Detect CLIs" 버튼 클릭
# claude-cli가 감지되었는지 확인
```

---

## 🔍 Step 2: 다른 AI CLI 감지 및 등록

### 2-1. 다른 AI CLI들 실행
각각 새 터미널에서:
```bash
# Cursor CLI (ChatGPT-5)
tmux new-session -s cursor-cli
cursor

# Codex CLI 
tmux new-session -s codex-cli
codex

# Gemini CLI
tmux new-session -s gemini-cli
gemini

# VSCode Claude
code .  # VSCode에서 Claude 확장 활성화
```

### 2-2. 대시보드에서 전체 CLI 감지
```
1. PM Control 탭에서 "Detect CLIs" 클릭
2. 감지된 CLI 목록 확인:
   - ✅ claude-cli (PM)
   - ✅ cursor-cli (기획/설계)
   - ✅ codex-cli (백엔드)
   - ✅ gemini-cli (콘텐츠)
   - ✅ vscode (프론트엔드)
```

---

## 📝 Step 3: GitHub 이슈 기반 작업 할당

### 3-1. 이슈 생성 (예시)
```markdown
# GitHub에서 새 이슈 생성
제목: "사용자 대시보드 기능 구현"
내용:
- 사용자 통계 위젯 추가
- 실시간 데이터 업데이트
- 반응형 디자인 적용
- API 엔드포인트 구현
```

### 3-2. PM Claude가 이슈 분석 및 분배
대시보드에서:
```
1. PM Control > Issue 선택
2. "Analyze & Assign" 클릭
3. PM Claude가 자동으로 분석:
   - 프론트엔드 작업 → VSCode Claude
   - 백엔드 API → Codex CLI
   - UX 디자인 → Gemini CLI
   - 전체 설계 → Cursor CLI
```

### 3-3. 각 CLI에 작업 푸시
```bash
# PM Claude가 각 CLI에 자동으로 메시지 전송:

# VSCode Claude에게:
"📋 Issue #23 할당: 사용자 통계 위젯 컴포넌트 구현
 파일: components/Dashboard/StatsWidget.tsx"

# Codex CLI에게:
"📋 Issue #23 할당: /api/stats 엔드포인트 구현
 FastAPI router 추가 필요"
```

---

## 🤝 Step 4: 협업 시작

### 4-1. 협업 세션 시작
PM Control에서:
```
1. Collaboration 섹션으로 이동
2. 주제 입력: "사용자 대시보드 v1.0"
3. 템플릿 선택: "feature_planning"
4. "Start Collaboration" 클릭
```

### 4-2. PM Claude가 협업 조율
```bash
# PM Claude가 모든 CLI에 브로드캐스트:
"🚀 협업 세션 시작: 사용자 대시보드 v1.0
 - 각자 맡은 부분 30분 내 초안 작성
 - PR #45에 코멘트로 진행상황 공유
 - 완료 시 PM에게 알림"
```

---

## 📊 Step 5: 실시간 모니터링

### 5-1. 작업 진행 상황 확인
대시보드 Monitoring Panel에서:
```
활성 작업:
├── VSCode Claude: StatsWidget.tsx 작성 중 (45%)
├── Codex CLI: API 엔드포인트 구현 중 (60%)
├── Gemini CLI: UX 문서 작성 완료 ✅
└── Cursor CLI: 아키텍처 설계 검토 중 (80%)
```

### 5-2. PM Claude의 중간 점검
```bash
# PM Claude가 진행 상황 체크:
gh issue comment 23 -b "진행 상황 업데이트:
- 프론트엔드: 45% 완료
- 백엔드: 60% 완료
- 예상 완료 시간: 2시간"
```

---

## ✅ Step 6: 작업 완료 및 PR 생성

### 6-1. 각 CLI 작업 완료 보고
```bash
# 각 CLI가 완료 시 PM에게 보고:
VSCode Claude: "✅ StatsWidget 구현 완료"
Codex CLI: "✅ API 엔드포인트 완료 및 테스트 통과"
```

### 6-2. PM Claude가 최종 PR 생성
```bash
# PM Claude 명령:
gh pr create --title "feat: 사용자 대시보드 구현" \
  --body "## 구현 내용
  - 통계 위젯 컴포넌트
  - API 엔드포인트
  - 반응형 디자인
  
  Closes #23"
```

---

## 🎯 실제 사용 팁

### 빠른 시작 체크리스트
- [ ] 백엔드 서버 실행 중 (port 8000)
- [ ] 프론트엔드 실행 중 (port 3000)
- [ ] PM Claude tmux 세션 활성화
- [ ] GitHub Token 설정 완료
- [ ] API 키들 .env에 설정

### 문제 해결
1. **CLI가 감지 안 될 때**: tmux 세션 이름 확인
2. **메시지 전달 안 될 때**: tmux send-keys 권한 확인
3. **GitHub 연동 실패**: Token 권한 확인 (repo, workflow 필요)

### 고급 활용
```bash
# PM Claude에게 복잡한 프로젝트 관리 요청:
"전체 리팩토링 작업을 관리해줘:
1. 코드 분석은 Cursor에게
2. 리팩토링은 Codex에게
3. 테스트는 VSCode Claude에게
4. 문서화는 Gemini에게"
```

---

## 📞 다음 단계

1. **더 많은 AI 추가**: Mistral, Llama 등
2. **자동화 강화**: GitHub Actions 연동
3. **분석 대시보드**: 생산성 메트릭 추적
4. **AI 간 직접 통신**: 중간 조율 없이 협업

이제 PM Claude를 중심으로 AI 팀을 운영할 준비가 완료되었습니다! 🚀