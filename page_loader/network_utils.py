import requests
from typing import Union
from page_loader.exceptions import AppInternalError
from page_loader.logging_utils import init_logger


logger = init_logger()


def get_html(url: str) -> str:
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.debug(e)
        raise AppInternalError(f"Can't download html {url}") from e
    return response.text


def get_res(url: str) -> Union[requests.Response, None]:
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


def save_res(response: requests.Response, to_file_name: str):
    try:
        with open(to_file_name, 'wb') as f:
            for chunk in response.iter_content(chunk_size=None):
                f.write(chunk)
                f.flush()
    except OSError as e:
        logger.debug(e)
        logger.error(f"Can't save resource to {to_file_name}")
