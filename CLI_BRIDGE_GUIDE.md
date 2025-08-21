# 🌉 AI Orchestra CLI Bridge - 진짜 자동 메시징!

## 🎯 드디어 해결! 

ChatGPT가 제시한 방법으로 **진짜 자동 메시징**이 가능합니다!

### 이전 vs 현재
- **이전**: "메시지 확인해" → 수동
- **현재**: 출력 자동 감지 → 자동 전달!

## 🚀 60초 설정

### 1. tmux 세션 확인
```bash
tmux list-sessions
# pm-claude, gemini-cli, codex-cli 있어야 함
```

### 2. 파이프 설정 (각 CLI 출력을 파일로)
```bash
cd ~/ai-orchestra-dashboard/cli-bridge

# PM Claude 출력 캡처
./setup_pipe.sh pm-claude:0 pm-claude

# Gemini 출력 캡처  
./setup_pipe.sh gemini-cli:0 gemini

# Codex 출력 캡처
./setup_pipe.sh codex-cli:0 codex
```

### 3. 릴레이 시작 (별도 터미널에서)
```bash
cd ~/ai-orchestra-dashboard/cli-bridge
python3 relay.py
```

## 🎭 테스트 시나리오

### PM Claude에서:
```
@gemini: Issue #3 사용자 가이드를 작성해주세요
@codex: Issue #2 API 최적화를 시작하세요
```

### 자동으로 일어나는 일:
1. PM이 "@gemini:" 출력 → relay.py가 감지
2. "Issue #3 사용자 가이드를 작성해주세요"가 Gemini CLI에 자동 입력!
3. Gemini가 작업 시작

### Gemini/Codex에서 보고:
```
@pm: 작업 완료했습니다. PR #45 생성됨
```

## 🔥 핵심 차이점

### 수동 방식 (이전)
```
PM: 파일에 메시지 저장
You: "Gemini야 확인해"
Gemini: 파일 읽기
```

### 자동 방식 (현재)
```
PM: "@gemini: 메시지" 출력
relay.py: 자동 감지 & 전달
Gemini: 메시지 자동 수신!
```

## 📝 라우팅 규칙 (routes.txt)

현재 설정:
- `pm-claude -> gemini` : PM이 @gemini: 출력 시
- `pm-claude -> codex` : PM이 @codex: 출력 시  
- `gemini -> pm-claude` : Gemini가 @pm: 출력 시
- `codex -> pm-claude` : Codex가 @pm: 출력 시
- `gemini <-> codex` : 서로 협업 가능

## 🎬 실제 사용 예시

**PM Claude:**
```
다음 메시지를 출력해주세요:
@gemini: 프로젝트 문서화를 시작하세요
@codex: 백엔드 API 구현을 시작하세요
```

**자동 전달됨!** 

Gemini와 Codex CLI에 메시지가 자동으로 입력됩니다!

## ⚠️ 주의사항

1. tmux 세션이 활성화되어 있어야 함
2. pipe-pane 설정 후 relay.py 실행
3. "@target:" 형식 준수 필요

## 🎉 결론

**드디어 진짜 자동화!** PM이 메시지를 출력하면 자동으로 팀원 CLI에 전달됩니다!