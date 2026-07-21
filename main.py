from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="마이 헬스 로그 API", version="1.0")

records = []  # TODO: Day 3에서 파일 저장으로 발전

class RecordIn(BaseModel):
    date: str
    weight: float
    height: float
    systolic: int
    diastolic: int
    blood_sugar: int
    steps: int = 0
    sleep_hours: float = 0.0
    memo: str = ""

# TODO: BMI 계산 / 분류 / 경고 함수를 작성 (기준표 참고)

@app.get("/")
def read_root():
    return {"message": "마이 헬스 로그 API"}

# TODO: POST   /records            - 기록 추가 (BMI/분류 자동 계산)
# TODO: GET    /records            - 전체 조회
# TODO: GET    /records/{record_id} - 단건 조회 (없으면 404)
# TODO: PUT    /records/{record_id} - 수정
# TODO: DELETE /records/{record_id} - 삭제
# TODO: GET    /search             - 날짜 범위 검색
# TODO: GET    /stats              - 통계