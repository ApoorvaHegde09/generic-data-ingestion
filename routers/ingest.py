import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas import IngestRequest
from services.ingestion_service import ingest_sources
from crud import get_all_records, get_ingestion_runs
from models import IngestionRun

from pydantic import BaseModel
from ai.assistant import process_question

router = APIRouter()


@router.post("/ingest")
def ingest_data(request: IngestRequest, db: Session = Depends(get_db)):

    results = ingest_sources(db, request.sources)

    return {
        "message": "Ingestion completed",
        "results": results
    }


@router.get("/records")
def get_records(db: Session = Depends(get_db)):

    records = get_all_records(db)

    result = []

    for record in records:
        result.append({
            "id": record.id,
            "source_name": record.source_name,
            "api_url": record.api_url,
            "status_code": record.status_code,
            "created_at": record.created_at.isoformat(),
            "response": json.loads(record.response)
        })

    return result

@router.get("/ingestion-runs")
def get_ingestion_history(db: Session = Depends(get_db)):

    runs = get_ingestion_runs(db)

    result = []

    for run in runs:
        result.append({
            "run_id": run.id,
            "status": run.status,
            "total_sources": run.total_sources,
            "successful_sources": run.successful_sources,
            "failed_sources": run.failed_sources,
            "started_at": run.started_at.isoformat(),
            "completed_at": (
                run.completed_at.isoformat()
                if run.completed_at
                else None
            )
        })

    return result

class QuestionRequest(BaseModel):
    question: str


@router.post("/ai/chat")
def ai_chat(
    request: QuestionRequest,
    db: Session = Depends(get_db)
):

    return process_question(
        request.question,
        db
    )