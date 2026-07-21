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
@app.post("/records")
def create_record(record: RecordIn):
    new_record = record.dict()
    new_record["id"] = len(records) + 1
    records.append(new_record)
    return new_record
# TODO: GET    /records            - 전체 조회
@app.get("/records")
def get_records():
    return {"count": len(records), "records": records}
# TODO: GET    /records/{record_id} - 단건 조회 (없으면 404)
@app.get("/records/{record_id}")
def get_record(record_id: int):
    for r in records:
        if r["id"] == record_id:
            return r
    raise HTTPException(status_code=404, detail="기록을 찾을 수 없습니다")
# TODO: PUT    /records/{record_id} - 수정
@app.put("/records/{record_id}")
def update_record(record_id: int, updated: RecordIn):
    for i, r in enumerate(records):
        if r["id"] == record_id:
            new_data = updated.dict()
            new_data["id"] = record_id
            records[i] = new_data
            return new_data
    raise HTTPException(status_code=404, detail="기록을 찾을 수 없습니다")
# TODO: DELETE /records/{record_id} - 삭제
@app.delete("/records/{record_id}")
def delete_record(record_id: int):
    for i, r in enumerate(records):
        if r["id"] == record_id:
            records.pop(i)
            return {"message": f"{record_id}번 기록이 삭제되었습니다"}
    raise HTTPException(status_code=404, detail="기록을 찾을 수 없습니다")
# TODO: GET    /search             - 날짜 범위 검색
# TODO: GET    /stats              - 통계