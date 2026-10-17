
import io
import json
from pathlib import Path

from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
    HTTPException,
)
from sqlalchemy.orm import Session
from pydantic import BaseModel
from pypdf import PdfReader

from database import get_db
from schemas import IngestRequest
from services.ingestion_service import ingest_sources
from crud import get_all_records, get_ingestion_runs
from ai.assistant import process_question

router = APIRouter()

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"
UPLOAD_TEXT_PATH = DOCS_DIR / "uploaded_document.txt"


@router.post("/ingest")
def ingest_data(
    request: IngestRequest,
    db: Session = Depends(get_db),
):
    results = ingest_sources(db, request.sources)

    return {
        "message": "Ingestion completed",
        "results": results,
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
            "response": json.loads(record.response),
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
            ),
        })

    return result


class QuestionRequest(BaseModel):
    question: str


@router.post("/ai/chat")
def ai_chat(
    request: QuestionRequest,
    db: Session = Depends(get_db),
):
    return process_question(request.question, db)


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    filename = file.filename or "uploaded.pdf"

    # Validate the file extension
    if Path(filename).suffix.lower() != ".pdf":
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF file.",
        )

    # Read the uploaded file directly from memory.
    # Its original C: or D: drive location does not matter.
    contents = await file.read()

    print("Uploaded filename:", filename)
    print("Uploaded file size:", len(contents))
    print("PDF signature:", contents[:8])

    if not contents:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty.",
        )

    if not contents.startswith(b"%PDF-"):
        raise HTTPException(
            status_code=400,
            detail="The uploaded file does not appear to be a valid PDF.",
        )

    # Extract text from the PDF
    try:
        reader = PdfReader(io.BytesIO(contents))

        if reader.is_encrypted:
            raise HTTPException(
                status_code=400,
                detail="The PDF is encrypted. Please upload an unprotected PDF.",
            )

        text_parts = []

        for page_number, page in enumerate(reader.pages, start=1):
            page_text = page.extract_text()

            if page_text and page_text.strip():
                text_parts.append(page_text.strip())

        text = "\n\n".join(text_parts).strip()

    except HTTPException:
        raise
    except Exception as exc:
        print("PDF extraction error:", repr(exc))
        raise HTTPException(
            status_code=400,
            detail="Could not read this PDF. Please check that it is valid and not corrupted.",
        )

    # pypdf cannot extract text embedded only in page images.
    if not text:
        raise HTTPException(
            status_code=422,
            detail=(
                "The PDF was uploaded, but no selectable text could be "
                "extracted. If the pages contain scanned images, OCR is needed."
            ),
        )

    # Save the latest uploaded document for ai/rag.py
    try:
        DOCS_DIR.mkdir(parents=True, exist_ok=True)
        UPLOAD_TEXT_PATH.write_text(text, encoding="utf-8")
    except OSError as exc:
        print("Could not save extracted text:", repr(exc))
        raise HTTPException(
            status_code=500,
            detail="Text was extracted, but could not be saved for AI retrieval.",
        )

    print("Extracted characters:", len(text))
    print("Saved extracted text to:", UPLOAD_TEXT_PATH)

    return {
        "filename": filename,
        "content_type": file.content_type,
        "size": len(contents),
        "pages": len(reader.pages),
        "characters_extracted": len(text),
        "extracted_text_preview": text[:1000],
        "message": "PDF uploaded, text extracted, and saved for AI retrieval.",
    }
