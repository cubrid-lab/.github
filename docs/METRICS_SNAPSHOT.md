# 사용률 지표 스냅샷 — 발표 자료용

> 기준일: 2026-09-12 · 측정 방법: GitHub API + PyPI API (재측정 스크립트 포함)

## 핵심 숫자 (슬라이드 5·활용성 배점 대응)

| 지표 | pycubrid | sqlalchemy-cubrid | cubrid-mcp-server | cubrid-cookbook | **합계** |
|---|---:|---:|---:|---:|---:|
| GitHub 스타 | 21 | 28 | 21 | 17 | **87** |
| 유니크 클론 (14일) | 234 | 183 | 157 | 73 | **647** |
| 유니크 방문 (14일) | 21 | 17 | 14 | 10 | **62** |
| 병합된 PR | 154 | 148 | 78 | 52 | **432** |
| 활성 CI 워크플로 | 18 | 20 | — | — | **38+** |
| PyPI 릴리스 | 16 | 19 | (게시 대기) | — | **35** |
| 문서 사이트 | ✅ 200 | ✅ 200 | ✅ 200 | ✅ 200 | **4/4** |
| 외부 기여자 | 0 | 0 | 1 | 1 | **2** |

## 슬라이드에 넣을 핵심 메시지

### 지속성 지표 (가장 강한 증거)
```
유니크 클론 647회/14일 = 실제로 코드를 내려받는 사람이 주당 ~324명
  → 단순 "스타 누르고 끝"이 아니라 clone을 하는 개발자
  → CI 재현·실험·학습 목적으로 추정
```

### 완성도 지표
```
PR 432개 병합 = 하루 평균 7개 (2026-09 기준 2개월)
  → 두 유지보수자 + AI 에이전트가 산출한 검증된 변경
  → 전 PR CI 게이트 통과 (20 Python×CUBRID 조합 통합 테스트)
```

### 신뢰성 지표
```
PyPI v1.7.0 · 16+19회 릴리스 (첫 게시 2022-07 → 현재)
  → 4년간 지속 유지보수 (v0.x의 안정적 1.x 성숙)
  → 월 2~3회 정기 릴리스 주기
```

### AI/LLM 생태계
```
cubrid-mcp-server v0.4.0 (GitHub Release 게시 완료)
  → 12 MCP 도구 · 읽기 전용 화이트리스트 · 옵트인 쓰기
  → AI 에이전트 템플릿 5종 (cookbook templates/ai-agent/)
```

## 측정 방법 및 재측정

```bash
# GitHub 스타·클론·방문 (14일)
gh repo view cubrid-lab/pycubrid --json stargazerCount --jq .stargazerCount
gh api repos/cubrid-lab/pycubrid/traffic/clones?per=week --jq '{count,uniques}'
gh api repos/cubrid-lab/pycubrid/traffic/views?per=week --jq '{count,uniques}'

# PyPI 다운로드 (BigQuery 무료 쿼리)
# https://console.cloud.google.com → bigquery-public-data.pypi.file_downloads
SELECT COUNT(*) FROM `bigquery-public-data.pypi.file_downloads`
WHERE project = 'pycubrid' AND timestamp >= '2026-08-01'

# 병합 PR 수
gh pr list -R cubrid-lab/pycubrid --state merged --limit 1000 --json number --jq 'length'
```

## 부족한 지표 (발표 시 솔직하게 인정)

| 지표 | 현재 | 개선 방향 |
|---|---|---|
| PyPI 일별 다운로드 | 측정 대기 | BigQuery 무료 쿼리로 발표 전 확보 |
| 외부 기여자 | 2명 | GFI 5개 시드 → 대회 후 유입 유도 |
| 스타 대비 포크 비율 | 낮음 (포크 1~2) | 실사용자가 fork 없이 pip install로 사용 |
| 다운로드 → 설치 전환 | 측정 불가 | `pip install` 자체는 추적 안 됨 |

## 발표 전 재측정 스케줄

- [ ] 발표 1주 전: GitHub 트래픽 + 스타 재측정
- [ ] 발표 3일 전: PyPI BigQuery 다운로드 수 확보
- [ ] 발표 당일 아침: 최종 숫자 확정 (이 문서 갱신)
- [ ] CUBRID 공식 등재 답변 도착 시: "후원사 인정" 항목 추가

---
*이 파일은 cubrid-lab/.github에 저장하여 org 차원에서 관리*
