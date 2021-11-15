import os
from page_loader.exceptions import AppInternalError
from page_loader.logging_utils import init_logger


logger = init_logger()


def check_output_path(output_path: str) -> None:
    if not os.path.exists(output_path):
        raise AppInternalError(f"Path {output_path} not found")
    elif not os.path.isdir(output_path):
        raise AppInternalError(f"Path {output_path} is not a directory")


def make_dir(full_resource_path: str):
    try:
        os.mkdir(full_resource_path)
    except OSError as e:
        logger.debug(e)
        raise AppInternalError(f"Can't create directory {full_resource_path}") from e
