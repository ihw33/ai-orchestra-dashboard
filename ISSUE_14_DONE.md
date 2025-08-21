Codex ✅ 작업 완료: Issue #14 — 프로젝트 CRUD 엔드포인트

- 완료 내용:
  - `POST/GET/LIST/PUT/DELETE /api/projects` 구현(DB 기반)
  - 기존 정적 프로젝트 목록 제거 → DB 조회로 통일
  - 모니터링 엔드포인트가 DB의 `github_repo` 목록을 사용하도록 정리
- 산출물:
  - `backend/app/routers/projects_router.py`
  - (연계) `backend/app/schemas.py`, `backend/app/models.py`
- 테스트/검증:
  - 서버 기동 시 테이블 자동 생성(`init_db()`)
  - `POST /api/projects` 후 목록/조회/수정/삭제 정상 응답 기대
- 비고:
  - Alembic 사용 시 마이그레이션 생성 권장
- PR: 준비 중 (로컬 변경사항)

