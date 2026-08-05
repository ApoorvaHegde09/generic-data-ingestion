from fastapi import HTTPException
from requests.exceptions import RequestException

from services.api_service import fetch_api_data
from crud import save_api_data


def ingest_sources(db, sources):

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

        except RequestException:

            raise HTTPException(
                status_code=502,
                detail=f"Unable to fetch data from {source.url}"
            )

    return results