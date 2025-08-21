# 🔍 실시간 모니터링 가이드

## 모니터링 주기
- **5-10분마다**: CLI 화면 체크
- **파일 변경 시**: 즉시 확인
- **에러 발생 시**: 즉시 조치

## 체크 포인트

### 1. CLI 상태 확인 (5분마다)
```bash
# Tab 4 전체 세션 상태
osascript -e 'tell app "iTerm" to ...'
```

### 2. 파일 시스템 모니터링
```bash
# Backend 작업 확인
ls -la backend/app/services/
ls -la backend/app/routers/

# Frontend 작업 확인  
ls -la frontend/src/components/
```

### 3. 프로세스 확인
```bash
# 실행 중인 서버
ps aux | grep uvicorn
ps aux | grep "npm run dev"
```

### 4. Git 상태
```bash
git status
git log --oneline -5
```

## 🚨 즉시 조치 필요 상황

1. **CLI 무응답**
   - Session restart
   - 작업 재할당

2. **파일 충돌**
   - Git conflict 해결
   - 팀원 조율

3. **서버 다운**
   - 프로세스 재시작
   - 로그 확인

4. **작업 중단**
   - 블로커 확인
   - 대체 방안 제시

## 📱 알림 설정

### 파일 변경 감지
```bash
# fswatch 사용
fswatch -o backend/app | xargs -n1 -I{} echo "Backend changed"
```

### 에러 로그 모니터링
```bash
tail -f backend/*.log
```

## 🎯 PM 체크리스트 (수시로)

- [ ] 모든 CLI 살아있는가?
- [ ] 파일이 생성/수정되고 있는가?
- [ ] 서버가 정상 작동하는가?
- [ ] 팀원들이 블로커에 막혀있지 않은가?
- [ ] PR/Issue 업데이트가 있는가?

---

**중요**: AI는 쉬지 않으므로 지속적 모니터링 필수!