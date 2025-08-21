Codex ✅ 작업 완료: Issue #12 — 프로젝트 모델 스키마 정의

- 완료 내용:
  - `ProjectCreate/Update/Out` 및 `Task` 관련 Pydantic v2 스키마 추가
  - ORM 매핑을 위한 `from_attributes=True` 구성 적용
  - `slug`, `github_repo` 등 기본 필드 밸리데이션(Pattern/Length) 반영
- 산출물:
  - `backend/app/schemas.py`
  - (연계) `backend/app/models.py`에 `Project.slug` 컬럼 추가
- 테스트/검증:
  - FastAPI 앱 기동 시 스키마 import 정상, DB 초기화 경로에서 테이블 생성 확인(콘솔 로그)
- 비고:
  - 마이그레이션 사용 시 `alembic revision --autogenerate`로 `slug` 컬럼 반영 권장
- PR: 준비 중 (로컬 변경사항)

