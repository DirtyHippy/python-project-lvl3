import logging
import sys
import requests
import traceback
import os
from functools import wraps
from typing import Union, Any


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(stream=sys.stderr)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def write_log(function):
    @wraps(function)
    def inner(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception as e:
            logger.debug(e)
            logger.error(traceback.format_exc())
            raise e
    return inner


@write_log
def get_url(url: str) -> Union[requests.Response, None]:
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        raise requests.exceptions.RequestException(f"Can't download url {url}")
    return response


@write_log
def is_valid_output_path(output_path: str) -> Union[bool, None]:
    if not os.path.exists(output_path):
        raise FileNotFoundError(f"Path {output_path} not found")
    elif not os.path.isdir(output_path):
        raise IsADirectoryError(f"Path {output_path} is not a directory")
    return True


@write_log
def make_dir(full_resource_path: str):
    try:
        os.mkdir(full_resource_path)
    except OSError:
        raise OSError(f"Can't create directory {full_resource_path}")


@write_log
def save_content(content: Any, to_file_name: str, mode: str):
    try:
        with open(to_file_name, mode) as f:
            f.write(content)
    except OSError:
        raise OSError(f"Can't save to {to_file_name}")
