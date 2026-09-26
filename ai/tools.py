from models import IngestionRun


def get_latest_ingestion_run(db):
    run = (
        db.query(IngestionRun)
        .order_by(IngestionRun.id.desc())
        .first()
    )

    if not run:
        return None

    return {
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
    }


def get_ingestion_history(db):
    runs = (
        db.query(IngestionRun)
        .order_by(IngestionRun.id.desc())
        .all()
    )

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


def get_failed_ingestions(db):
    runs = (
        db.query(IngestionRun)
        .filter(IngestionRun.failed_sources > 0)
        .order_by(IngestionRun.id.desc())
        .all()
    )

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