from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List
import time
import logging
from database import SessionLocal, RequestLog, init_db
from algorithm import largest_rectangle

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Largest Rectangle in Matrix API", version="1.0.0")

@app.on_event("startup")
def startup_event():
    init_db()
    logger.info("Database initialized")

class MatrixRequest(BaseModel):
    matrix: List[List[int]]

class MatrixResponse(BaseModel):
    number: int
    area: int
    turnaround_time_ms: float

@app.post("/largest-rectangle", response_model=MatrixResponse)
async def find_largest_rectangle(request: Request, body: MatrixRequest):
    start_time = time.time()
    logger.info(f"Received matrix of shape {len(body.matrix)}x{len(body.matrix[0])}")

    number, area = largest_rectangle(body.matrix)

    elapsed_ms = round((time.time() - start_time) * 1000, 4)

    # Log to DB
    db = SessionLocal()
    try:
        log_entry = RequestLog(
            matrix=str(body.matrix),
            result_number=number,
            result_area=area,
            turnaround_time_ms=elapsed_ms,
        )
        db.add(log_entry)
        db.commit()
        logger.info(f"Response: number={number}, area={area}, time={elapsed_ms}ms")
    finally:
        db.close()

    return MatrixResponse(number=number, area=area, turnaround_time_ms=elapsed_ms)

@app.get("/logs")
def get_logs():
    """View all logged requests."""
    db = SessionLocal()
    try:
        logs = db.query(RequestLog).order_by(RequestLog.id.desc()).all()
        return [
            {
                "id": log.id,
                "matrix": log.matrix,
                "result_number": log.result_number,
                "result_area": log.result_area,
                "turnaround_time_ms": log.turnaround_time_ms,
                "created_at": str(log.created_at),
            }
            for log in logs
        ]
    finally:
        db.close()
