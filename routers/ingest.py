import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas import IngestRequest
from services.ingestion_service import ingest_sources
from crud import get_all_records

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