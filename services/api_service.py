import requests
from requests.exceptions import RequestException

from utils.logger import logger


def fetch_api_data(url, headers=None, params=None):

    try:

        logger.info(f"Fetching data from {url}")

        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        logger.info(
            f"Success ({response.status_code}) : {url}"
        )

        return {
            "status_code": response.status_code,
            "data": response.json()
        }

    except RequestException as e:

        logger.error(
            f"Failed to fetch {url} : {str(e)}"
        )

        raise