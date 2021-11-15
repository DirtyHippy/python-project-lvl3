import requests
from typing import Union
from page_loader.exceptions import AppInternalError
from page_loader.logging_utils import init_logger


logger = init_logger()


def get_url(url: str) -> Union[requests.Response, None]:
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.debug(e)
        raise AppInternalError(f"Can't download url {url}") from e
    return response


def save_content(content: bytes, to_file_name: str, mode: str):
    try:
        with open(to_file_name, mode) as f:
            f.write(content)
    except OSError as e:
        logger.debug(e)
        raise AppInternalError(f"Can't save to {to_file_name}") from e
