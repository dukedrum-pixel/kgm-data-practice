# KGM 교육용 Codex × GitHub 공공데이터 대시보드

**완전 가상데이터 데모**. 실제 KGM 데이터가 아니며 가격지수 역시 임의로 생성했습니다.

## 기본 실행 (API 키 / pip 설치 불필요)
```bash
python scripts/build.py
python -m unittest discover -s tests
```
`site/index.html`을 브라우저에서 열면 품목·연도 필터, 그래프, CSV 다운로드가 작동합니다.

## GitHub 및 Pages
1. GitHub에 새 저장소를 생성하고 이 프로젝트 폴더의 파일을 업로드 또는 push.
2. Settings → Pages → Build and deployment → Source: **GitHub Actions**.
3. main으로 push/PR merge하면 Pages 워크플로가 빌드·배포합니다. PR은 빌드/테스트만 합니다.
4. 워크플로의 Actions 로그와 Pages URL을 확인합니다. 공개 저장소의 Pages는 외부 공개될 수 있습니다.

## 공식 공공데이터 API로 전환 (선택)
1. https://www.data.go.kr 에서 분석할 **실제 JSON OpenAPI**를 선정하여 활용 신청 및 인증키 발급.
2. API 명세에 따라 `config/api_mapping.json`의 URL, 인증 파라미터, 요청 파라미터, JSON 응답 경로, 필드명을 수정.
3. `DATA_GO_KR_API_KEY` 환경 변수를 로컬 셸에 설정한다(키를 파일에 넣거나 GitHub에 커밋하지 말 것).
4. `python scripts/import_api.py` → `python scripts/build.py` 실행.
5. 응답 구조, 지수 단위, 기준연도, 품목 매핑, 페이징 및 이용약관을 검증한다.

**주의:** 모든 데이터포털 API가 동일한 JSON 형식으로 응답하지 않습니다. XML 전용, 인증 방식 차이, 페이지 분할, CORS 등의 경우 해당 API 명세에 맞춰 importer를 수정해야 합니다. 이 예시는 형식 매핑을 위한 교육용 범용 골격이며 특정 실제 API 호출 성공을 보장하지 않습니다.

## 실습 규칙
- `AGENTS.md`: 저장소 프로젝트 규칙
- `.agents/skills/public-data-dashboard/SKILL.md`: 반복 분석 스킬
- `scripts/build.py`: 정적 HTML 빌드
- `.github/workflows/pages.yml`: PR 빌드 검증 및 main Pages 배포
- `tests/test_build.py`: 자동 테스트
