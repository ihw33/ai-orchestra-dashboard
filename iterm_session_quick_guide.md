# 🗂️ iTerm2 세션 ID 시스템

## 🎯 목적
각 세션에 고유 ID를 부여해서 헷갈리지 않고 빠르게 찾기

## 📋 세션 ID 맵

### Tab 1: Home 🏠
| 세션 | ID | CLI | 역할 |
|------|----|----|------|
| 1-1 | HOME_MAIN | Terminal | 일반 작업 |
| 1-2 | HOME_MONITOR | Monitor | 모니터링 |

### Tab 2: AI Engine 🤖
| 세션 | ID | CLI | 역할 |
|------|----|----|------|
| 2-1 | ENGINE_GEMINI | Gemini | 데이터 처리 |
| 2-2 | ENGINE_CODEX | Codex | 백엔드 개발 |
| 2-3 | ENGINE_TERMINAL | Terminal | 테스트 |

### Tab 3: IWL Project 📚
| 세션 | ID | CLI | 역할 |
|------|----|----|------|
| 3-1 | IWL_PM | PM Claude | 프로젝트 관리 |
| 3-2 | IWL_CURSOR | Cursor | 프론트엔드 |
| 3-3 | IWL_GEMINI | Gemini | 콘텐츠 |
| 3-4 | IWL_CODEX | Codex | API |

### Tab 4: Orchestra Board 🎼
| 세션 | ID | CLI | 역할 |
|------|----|----|------|
| 4-1 | ORCH_CLAUDE | Claude | 백엔드 |
| 4-2 | ORCH_TERMINAL | Terminal | 테스트 |
| 4-3 | ORCH_GEMINI | Gemini | 데이터 |
| 4-4 | ORCH_CODEX | Codex | 백엔드 |

## 🔍 빠른 찾기

### Gemini 위치
- Tab 2-1: ENGINE_GEMINI (AI Engine)
- Tab 3-3: IWL_GEMINI (IWL Project)
- Tab 4-3: ORCH_GEMINI (Orchestra)

### Codex 위치
- Tab 2-2: ENGINE_CODEX (AI Engine)
- Tab 3-4: IWL_CODEX (IWL Project)
- Tab 4-4: ORCH_CODEX (Orchestra)

### Claude 위치
- Tab 3-1: IWL_PM (PM Claude)
- Tab 4-1: ORCH_CLAUDE (Orchestra)

## 💡 사용법

### 1. ID로 세션 찾기
```python
python3 iterm_session_manager.py
# ORCH_GEMINI 입력 → Tab 4, Session 3
```

### 2. CLI 이름으로 찾기
```python
# "Gemini" 검색 → 3개 위치 표시
```

### 3. 세션으로 이동
```applescript
osascript find_session_by_id.applescript ORCH_GEMINI
```

## 🚀 장점
- 세션 위치 헷갈림 해결
- 빠른 네비게이션
- 명확한 역할 구분
- 자동화 가능

---

**작성일**: 2025-08-20
**업데이트**: 실시간