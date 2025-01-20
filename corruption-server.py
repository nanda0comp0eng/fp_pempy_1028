from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, List
import uvicorn
from core import DatabaseManager, CorruptionCaseManager, CaseType, CaseStatus

app = FastAPI(title="Corruption Cases Management API")
db_manager = DatabaseManager("data.db")
case_manager = CorruptionCaseManager(db_manager)

@app.get("/cases")
def get_all_cases() -> List[dict]:
    """Mendapatkan semua data kasus"""
    return case_manager.get_all_cases()

@app.get("/cases/{case_id}")
def get_case(case_id: int) -> dict:
    """Detail kasus spesifik"""
    case = case_manager.get_case(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case


@app.get("/cases/types")
def get_case_types():
    """Daftar jenis kasus"""
    return [type.value for type in CaseType]

@app.post("/cases")
def create_case(case_data: dict) -> dict:
    """Menambah kasus baru"""
    try:
        return case_manager.add_case(case_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/cases/{case_id}")
def update_case(case_id: int, new_status: str, timeline_desc: str) -> dict:
    """Update status kasus"""
    case = case_manager.update_case_status(case_id, new_status, timeline_desc)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case

@app.delete("/cases/{case_id}")
def delete_case(case_id: int):
    """Menghapus kasus"""
    if case_manager.delete_case(case_id):
        return {"message": f"Case {case_id} deleted successfully"}
    raise HTTPException(status_code=404, detail="Case not found")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)