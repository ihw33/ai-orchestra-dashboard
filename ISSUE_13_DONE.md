Codex ✅ 작업 완료: Issue #13 — GitHub API 클라이언트 구현

- 완료 내용:
  - PyGithub 기반 `GitHubClient` 래퍼 보강: `test_connection`, `list_issues`, `list_pull_requests`, `rate_limit` 등
  - 에러 메시지 개선 및 토큰 미설정 시 명확한 예외 처리
- 산출물:
  - `backend/app/services/github_client.py`
- 테스트/검증:
  - 토큰 필요. 네트워크 제한 환경에선 실제 호출 차단될 수 있으나, 로컬 토큰 설정 시 정상 동작 예상
- 비고:
  - 서비스 계층(`github_service`)과 중복 기능 일부 존재 → 후속 정리 제안(의존성 주입 통일)
- PR: 준비 중 (로컬 변경사항)

