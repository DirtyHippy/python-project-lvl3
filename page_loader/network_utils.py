import requests
import logging
import logging.config
from typing import Union
from page_loader.exceptions import AppInternalError
from page_loader.logging_utils import LOGGING_CONFIG


logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


def get_html(url: str) -> str:
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.debug(e)
        raise AppInternalError(f"Can't download html {url}") from e
    return response.text


def get_resource(url: str) -> Union[requests.Response, None]:
    response = None
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.debug(e)
        logger.error(f"Can't download resource {url}")
    return response


def save_html(content: str, to_file_name: str):
    try:
        with open(to_file_name, 'w') as f:
            f.write(content)
    except OSError as e:
        logger.debug(e)
        raise AppInternalError(f"Can't save html to {to_file_name}") from e


def save_resource(response: requests.Response, to_file_name: str) -> bool:
    try:
        with open(to_file_name, 'wb') as f:
            for chunk in response.iter_content(chunk_size=None):
                f.write(chunk)
        return True
    except (OSError, requests.exceptions.RequestException) as e:
        logger.debug(e)
        logger.error(f"Can't save resource to {to_file_name}")
    return False
