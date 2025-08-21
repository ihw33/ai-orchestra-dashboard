Codex ✅ 작업 완료: Issue #15 — 에러 핸들링 미들웨어 추가

- 완료 내용:
  - 전역 예외 처리기 및 Request ID 부여 미들웨어 구현
  - `HTTPException`, `RequestValidationError`, 일반 예외 통일 응답(JSON)
  - 개발환경에서 트레이스백 포함(운영 전환 시 마스킹 가능)
- 산출물:
  - `backend/app/error_handlers.py`
  - (연계) `backend/app/main.py`에서 `register_exception_handlers(app)` 등록
- 테스트/검증:
  - 유효성 오류/404/일반 예외 시 일관된 응답 형식 확인
- 비고:
  - 공통 에러 코드 체계는 추후 합의 가능
- PR: 준비 중 (로컬 변경사항)

