# 마이 헬스 로그 API

매일의 건강 수치(몸무게, 키, 혈압, 혈당 등)를 기록하면 BMI를 자동 계산하고 건강 상태를 분류해주는 API입니다. 기록을 누적해서 검색하고 통계도 확인할 수 있습니다.

## 기능 목록

| 메서드 | 경로 | 설명 |
|---|---|---|
| POST | /records | 건강 기록 추가 (BMI/분류/경고 자동 계산) |
| GET | /records | 전체 기록 조회 |
| GET | /records/{id} | 기록 단건 조회 |
| PUT | /records/{id} | 기록 수정 |
| DELETE | /records/{id} | 기록 삭제 |
| GET | /search | 날짜 범위로 기록 검색 |
| GET | /stats | 평균 체중, 평균 BMI 등 통계 조회 |

## 실행 방법

### 로컬 실행

\`\`\`bash
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
uvicorn main:app --reload
\`\`\`

실행 후 `http://127.0.0.1:8000/docs` 접속

### Docker 실행

\`\`\`bash
docker build -t my-health-api .
docker run -p 8000:8000 my-health-api
\`\`\`

실행 후 `http://127.0.0.1:8000/docs` 접속

## 기술 스택

- Python 3.11
- FastAPI
- Pydantic
- Uvicorn
- Docker

## 참고

건강 분류 기준은 학습용으로 단순화된 값이며, 실제 의학적 진단이 아닙니다.