---
name: public-data-dashboard
description: Validate the virtual sample CSV, build and test the static dashboard, prepare a Draft PR, and deploy GitHub Pages only after human approval.
---

# 공공데이터 대시보드 반복 워크플로우

교육용 가상 샘플로 데이터 검증부터 Pages 배포 검토까지 수행한다. 저장소 규칙은 프로젝트 루트의 `AGENTS.md`를 우선한다.

## 1. 시작 전 확인

- `AGENTS.md`와 이 스킬을 읽고 현재 브랜치와 작업 트리 상태를 확인한다.
- 작업 브랜치는 `codex/` 접두사를 사용한다. `main`에 직접 커밋하지 않는다.
- 기본 입력은 `data/sample_prices.csv`의 교육용 가상 데이터다. 실제 KGM 구매 데이터, 개인 정보, 회사 기밀, 비공개 원본을 사용하거나 공개 경로에 넣지 않는다.
- 외부 API는 공식 명세와 인증키, 데이터 반출 허용 여부를 사용자가 확인한 경우에만 호출한다. 키는 `DATA_GO_KR_API_KEY` 환경 변수로만 관리하며 파일이나 로그, 커밋, Pages에 넣지 않는다.

## 2. 데이터 검증

프로젝트 루트에서 실행한다.

```bash
python scripts/data_quality.py
```

검증기는 기본 CSV의 필수 컬럼 `month,item_code,item_name,index_value,source`, 데이터 행 존재, 결측값, `(month,item_code)` 중복, `YYYY-MM` 형식과 01~12 월 범위, 유한한 양수 `index_value`를 검사하고 요약 보고서를 출력한다. 다른 CSV를 점검할 때는 `python scripts/data_quality.py 경로`로 입력 경로를 지정한다.

누락 컬럼·값, 중복 키, 잘못된 월·지수값 또는 빈 데이터가 있으면 작업을 중단하고 원인을 수정한다. 검증 결과가 `PASS`여도 데이터 출처와 샘플/실데이터 여부를 별도로 확인한다.

## 3. 대시보드 빌드

```bash
python scripts/build.py
```

Python 표준 라이브러리만 사용해 `data/sample_prices.csv`를 읽고 `site/index.html`을 생성한다. 빌드 전 품질 검증이 자동 실행되며 검증 실패 시 빌드가 중단되어야 한다. 출력된 레코드 수와 생성 파일을 확인한다.

## 4. 테스트

```bash
python -m unittest discover -s tests
```

모든 테스트가 통과해야 한다. 데이터 진단기 변경은 정상 데이터와 결측·중복·잘못된 월·수치·빈 데이터 사례를 포함한다. 빌드/화면 변경은 생성 HTML, 필터, 차트·전월비, CSV 다운로드, HTML 삽입 안전성에 영향을 주는 동작을 확인한다.

## 5. diff와 배포물 검토

```bash
git diff --check
git diff --stat
git status --short
```

전체 diff와 미추적 파일도 확인해 의도하지 않은 데이터, 키, 산출물, 대량 변경이 포함되지 않았는지 점검한다. 생성된 `site/index.html`이 변경 대상이 아니면 PR에 포함하지 않는다. 대시보드는 품목·연도 필터, 결과 없음 표시, 월별 차트와 연말/연초 전월비, 키보드 포커스, CSV 인용과 수식 시작 문자 처리, 모바일 레이아웃을 확인한다. 검토용 스크린샷은 실제 브라우저에서 확인한 경우에만 첨부한다.

## 6. Draft PR 검토

- 변경 파일과 목적, 실행 명령 및 테스트 결과, 데이터가 가상 샘플인지, 위험과 제한 사항을 PR 본문에 기록한다.
- 화면 변경이면 검토한 브라우저 크기와 필터·차트·다운로드 상태를 기록하고, 필요한 스크린샷 검토 항목을 남긴다.
- GitHub 인증이나 저장소 연결이 없으면 PR을 생성하지 않는다. 브랜치를 게시할 수 있도록 저장소 관리자에게 연결을 요청하거나 GitHub 웹 화면에서 비교 브랜치를 선택해 Draft PR을 만든다.
- 자동화나 에이전트가 승인으로 간주하지 않는다. 사람의 검토와 명시적 승인 전에는 머지하거나 배포하지 않는다.

## 7. 승인 후 Pages 배포 확인

사람의 승인 후에만 PR을 머지하거나 배포 절차를 진행한다. `.github/workflows/pages.yml`은 PR에서 테스트하고, `main` 반영 후 빌드·Pages 배포를 수행한다. 승인된 변경이 반영된 뒤 Actions 실행 결과, 배포 환경 상태, Pages URL을 확인한다. 실패하면 로그와 원인을 보고하고 재배포 전에 수정·재검증한다.
