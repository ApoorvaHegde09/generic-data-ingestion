import json
from models import ApiData


def save_api_data(
    db,
    source_name,
    api_url,
    status_code,
    response_data
):
    record = ApiData(
        source_name=source_name,
        api_url=str(api_url),
        status_code=status_code,
        response=json.dumps(response_data)
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record

def get_all_records(db):
    return db.query(ApiData).all()

def get_ingestion_runs(db):
    from models import IngestionRun

    return (
        db.query(IngestionRun)
        .order_by(IngestionRun.id.desc())
        .all()
    )