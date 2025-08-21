# 🎼 AI Orchestra 실행 알고리즘

## 실행 플로우

```mermaid
flowchart TD
  subgraph User["상혁님 (최종 승인자)"]
    U1[지시/컨펌 제공]
    U2[결과 확인]
  end

  subgraph PM["PM-CLI (Claude)"]
    P1[지시 수신]
    P2[이슈 생성/파싱]
    P3[상혁님 컨펌 요청]
    P4[팀원 지시 전달]
    P5[진행 상황 모니터링]
    P6[보고서 생성]
  end

  subgraph Team["팀원-CLI (Codex, Gemini, Claude, Cursor)"]
    T1[PM 지시 대기]
    T2[이슈 확인 - ACK]
    T3[작업 실행 - START]
    T4[결과 보고 - DONE]
  end

  subgraph GitHub["GitHub Repository"]
    G1[Issues]
    G2[Pull Requests]
    G3[Project Board]
    G4[Actions/Workflows]
  end

  U1 --> P1
  P1 --> P2
  P2 --> G1
  P2 --> P3
  P3 --> U1
  U1 --> P4
  P4 --> T1
  T1 --> T2
  T2 --> G1
  T2 --> T3
  T3 --> T4
  T4 --> G2
  G1 --> P5
  G2 --> P5
  P5 --> P6
  P6 --> U2
```

## 단계별 상세 설명

### 1. 지시 단계
- 상혁님 → PM: 작업 지시
- PM: 작업을 이슈로 분해
- PM → 상혁님: 이슈 계획 컨펌 요청

### 2. 실행 단계
- 상혁님: 컨펌
- PM → 팀원: 프롬프트로 지시 전달
- 팀원: GitHub 이슈 확인 및 작업 수행

### 3. 보고 단계
- 팀원 → GitHub: 코멘트 시그널 ([ACK], [START], [DONE])
- PM: GitHub 모니터링
- PM → 상혁님: 진행 상황 보고

### 4. 완료 단계
- 팀원: PR 생성 (Fixes #이슈번호)
- PM: 라운드 보고서 생성
- PM → 상혁님: 최종 보고

## 시그널 타이밍

| 시그널 | 발생 시점 | 제한 시간 |
|--------|----------|-----------|
| [ACK] | 이슈 확인 시 | 30분 이내 |
| [START] | 작업 시작 시 | ACK 후 즉시 |
| [REPORT] | 중간 보고 필요시 | 필요시 |
| [BLOCK] | 블로커 발생 시 | 즉시 |
| [DONE] | PR 생성 완료 시 | 작업 완료 즉시 |

## 권한 및 책임

### PM (Claude)
- 이슈 생성/관리
- 팀원 작업 지시
- 진행 상황 모니터링
- 상혁님 보고

### 팀원 (Codex, Gemini, Claude, Cursor)
- 지시받은 작업만 수행
- GitHub 이슈 코멘트로 보고
- PR 생성 및 테스트

### 상혁님
- 최종 의사결정
- 계획 승인
- 결과 검증