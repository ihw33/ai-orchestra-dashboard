# AI Orchestra Dashboard - 빠른 설정 가이드

## 🚀 즉시 시작하기

### 1. API 키 설정 (필수!)

backend/.env 파일을 열고 다음 키들을 입력하세요:

```bash
# backend/.env 파일 편집
cd backend
nano .env  # 또는 원하는 편집기 사용
```

필요한 API 키:
- **GITHUB_TOKEN**: [GitHub Settings > Tokens](https://github.com/settings/tokens)에서 생성
  - 필요 권한: repo, workflow, admin:org
- **ANTHROPIC_API_KEY**: [Anthropic Console](https://console.anthropic.com/)에서 획득
- **OPENAI_API_KEY**: [OpenAI Platform](https://platform.openai.com/api-keys)에서 획득

### 2. 백엔드 서버 시작

```bash
# 백엔드 시작 스크립트 실행
./start_backend.sh
```

서버가 시작되면:
- API 서버: http://localhost:8000
- API 문서: http://localhost:8000/docs

### 3. 프론트엔드 시작 (이미 실행 중)

```bash
# 프론트엔드는 이미 실행 중입니다
# http://localhost:3000
```

## 🔧 수동 설정 (스크립트가 작동하지 않을 경우)

### 백엔드 수동 시작:

```bash
cd backend

# 가상환경 생성 및 활성화
python3 -m venv venv
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt

# 서버 시작
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📝 주요 기능 테스트

1. **CLI 감지**: PM Control 탭에서 "Detect CLIs" 버튼 클릭
2. **이슈 할당**: 이슈 선택 후 "Analyze & Assign" 클릭
3. **협업 시작**: 협업 주제 입력 후 "Start Collaboration" 클릭

## 🐛 문제 해결

### "Connection Refused" 오류:
- 백엔드 서버가 실행 중인지 확인
- .env 파일의 API 키가 올바른지 확인
- 포트 8000이 다른 프로세스에서 사용 중인지 확인

### CLI가 감지되지 않을 때:
- 터미널에서 CLI들이 실제로 실행 중인지 확인
- tmux 세션이 활성화되어 있는지 확인

## 🔗 연결된 프로젝트

현재 감지된 프로젝트들:
- ai-orchestra-dashboard (현재 프로젝트)
- personal-journal-hub
- iwl-v5-rebuild
- 기타 활성 프로젝트들

## 💡 PM AI 작동 방식

1. **이슈 기반 업무 분배**:
   - PM AI가 GitHub 이슈 분석
   - 적절한 CLI에 자동 할당
   - 진행 상황 실시간 모니터링

2. **PR 기반 협업**:
   - 챕터별 의견 수렴
   - PM AI가 종합하여 최종 문서 작성
   - GitHub PR로 자동 관리

## 📞 지원

문제가 지속되면 다음을 확인하세요:
- GitHub 토큰 권한이 충분한지
- API 키가 유효한지
- 네트워크 연결 상태