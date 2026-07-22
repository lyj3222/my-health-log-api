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
def calc_bmi(weight: float, height: float) -> float:
    height_m = height / 100
    bmi = weight / (height_m * height_m)
    return round(bmi, 1)
def classify_bmi(bmi: float) -> str:
    if bmi < 18.5:
        return "저체중"
    elif bmi < 23:
        return "정상"
    elif bmi < 25:
        return "과체중"
    else:
        return "비만"
def classify_bp(systolic: int, diastolic: int) -> str:
    if systolic >= 140 or diastolic >= 90:
        return "고혈압"
    elif systolic >= 120 or diastolic >= 80:
        return "주의"
    else:
        return "정상"
def classify_sugar(blood_sugar: int) -> str:
    if blood_sugar >= 126:
        return "당뇨 의심"
    elif blood_sugar >= 100:
        return "공복혈당장애"
    else:
        return "정상"
def make_warnings(bmi_category: str, bp_category: str, sugar_category: str) -> list:
    warnings = []
    if bmi_category == "비만":
        warnings.append("BMI가 비만 범위입니다. 체중 관리가 필요합니다.")
    if bp_category == "고혈압":
        warnings.append("혈압이 고혈압 범위입니다. 병원 상담을 권장합니다.")
    if sugar_category == "당뇨 의심":
        warnings.append("혈당이 당뇨 의심 범위입니다. 병원 상담을 권장합니다.")
    return warnings

@app.get("/")
def read_root():
    return {"message": "마이 헬스 로그 API"}

# TODO: POST   /records            - 기록 추가 (BMI/분류 자동 계산)
@app.post("/records")
def create_record(record: RecordIn):
    new_record = record.dict()
    new_record["id"] = len(records) + 1

    bmi = calc_bmi(record.weight, record.height)
    bmi_category = classify_bmi(bmi)
    bp_category = classify_bp(record.systolic, record.diastolic)
    sugar_category = classify_sugar(record.blood_sugar)
    warnings = make_warnings(bmi_category, bp_category, sugar_category)

    new_record["bmi"] = bmi
    new_record["bmi_category"] = bmi_category
    new_record["bp_category"] = bp_category
    new_record["sugar_category"] = sugar_category
    new_record["warnings"] = warnings

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

            bmi = calc_bmi(updated.weight, updated.height)
            bmi_category = classify_bmi(bmi)
            bp_category = classify_bp(updated.systolic, updated.diastolic)
            sugar_category = classify_sugar(updated.blood_sugar)
            warnings = make_warnings(bmi_category, bp_category, sugar_category)

            new_data["bmi"] = bmi
            new_data["bmi_category"] = bmi_category
            new_data["bp_category"] = bp_category
            new_data["sugar_category"] = sugar_category
            new_data["warnings"] = warnings

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