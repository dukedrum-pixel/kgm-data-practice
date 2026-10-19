---
name: public-data-dashboard
description: Validate a local public-data CSV, generate and test a static analytics dashboard, and summarize safe GitHub Pages deployment steps.
---
# 공공데이터 대시보드 반복 업무
1. 프로젝트 루트의 AGENTS.md 규칙 확인
2. `data/sample_prices.csv`의 컬럼·기간·결측·양수 여부 검증
3. `python scripts/build.py` 실행
4. `python -m unittest discover -s tests` 실행
5. `site/index.html` 생성과 품목/연도 필터 및 CSV 다운로드 코드 확인
6. 변경사항 diff, 샘플/실제 데이터 여부, 보안 위험 검토
7. Draft PR용 제목/설명/테스트 내역 초안 작성
8. 승인 후 main 머지 및 Pages 배포 여부 확인(자동 승인 금지)
