# 프로젝트 작업 규칙 (Codex)
- 이 프로젝트는 **교육용 가상데이터**로 기본 실행한다. 실제 KGM 구매 데이터 사용 금지.
- Python 표준 라이브러리로 `python scripts/build.py`를 실행해 `site/index.html`을 만든다.
- `python -m unittest discover -s tests`를 수행한 후 변경 사항을 제출한다.
- `data/sample_prices.csv` 컬럼은 month,item_code,item_name,index_value,source 이다.
- 외부 API는 사용자가 공식 명세/인증키 및 반출 허용 여부를 확인한 경우에만 실행한다.
- API 키, 개인/회사 기밀, 원본 비공개 자료를 커밋하거나 Pages에 넣지 않는다.
- `main`에 직접 커밋하지 않는다. 브랜치 이름은 `codex/` 접두사로 만든다.
- 작업 완료 시 변경 파일, 실행 명령, 테스트 결과, 샘플/실데이터 여부를 보고한다.
- PR은 우선 Draft로 제안하고 사람의 검토 없이 머지하거나 배포하지 않는다.
