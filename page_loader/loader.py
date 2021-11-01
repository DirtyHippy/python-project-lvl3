import requests
import re
import os
from bs4 import BeautifulSoup  # type: ignore
from urllib.parse import urlparse


PATH_TO_IMAGES = '_files'
FILE_EXT = '.html'


def remove_scheme_from_url(url: str) -> str:
    parsed_url = urlparse(url)
    scheme = f"{parsed_url.scheme}://"
    return parsed_url.geturl().replace(scheme, '', 1)


def replace_characters(url: str) -> str:
    return re.sub(r"[^0-9a-zA-Z]", "-", url)


def gen_output_file_name(url: str, output_path: str) -> str:
    file_name = remove_scheme_from_url(url)
    file_name = replace_characters(file_name)
    return os.path.join(output_path, file_name + FILE_EXT)


def download(url: str, output_path: str):
    if not os.path.exists(output_path):
        raise FileNotFoundError(output_path)
    elif not os.path.isdir(output_path):
        raise IsADirectoryError(output_path)

    page = requests.get(url)
    if page.status_code == 200:
        soup = BeautifulSoup(page.text, "html.parser")
        output_file_name = gen_output_file_name(url, output_path)
        with open(output_file_name, 'w', encoding='utf-8') as f:
            f.write(soup.prettify())
