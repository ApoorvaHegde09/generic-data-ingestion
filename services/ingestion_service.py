from datetime import datetime

from fastapi import HTTPException
from requests.exceptions import RequestException

from services.api_service import fetch_api_data
from crud import save_api_data
from models import IngestionRun


def ingest_sources(db, sources):

    # Create ingestion run
    run = IngestionRun(
        status="running",
        total_sources=len(sources),
        successful_sources=0,
        failed_sources=0
    )

    db.add(run)
    db.commit()
    db.refresh(run)

    results = []

    for source in sources:

        try:

            response = fetch_api_data(
                url=source.url,
                headers=source.headers,
                params=source.params
            )

            record = save_api_data(
                db=db,
                source_name=source.name,
                api_url=source.url,
                status_code=response["status_code"],
                response_data=response["data"]
            )

            results.append({
                "source": source.name,
                "record_id": record.id,
                "status": "success"
            })

            run.successful_sources += 1

        except RequestException:

            run.failed_sources += 1

            results.append({
                "source": source.name,
                "status": "failed"
            })

    # Update final run status
    if run.failed_sources == 0:
        run.status = "success"
    elif run.successful_sources == 0:
        run.status = "failed"
    else:
        run.status = "partial_success"

    run.completed_at = datetime.utcnow()

    db.commit()

    return {
        "run_id": run.id,
        "status": run.status,
        "total_sources": run.total_sources,
        "successful_sources": run.successful_sources,
        "failed_sources": run.failed_sources,
        "results": results
    }