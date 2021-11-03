import requests
import re
import os
from bs4 import BeautifulSoup  # type: ignore
from urllib.parse import urlparse


END_PATH_TO_IMAGES = '_files'
FILE_EXT = '.html'
DELIMETER = '-'
INDENT = '   '


def remove_scheme_from_url(url: str) -> str:
    parsed_url = urlparse(url)
    scheme = f"{parsed_url.scheme}://"
    return parsed_url.geturl().replace(scheme, '', 1)


def replace_characters(url: str) -> str:
    return re.sub(r"[^0-9a-zA-Z]", DELIMETER, url)


def format_url(url: str) -> str:
    formatted_url = remove_scheme_from_url(url)
    formatted_url = replace_characters(formatted_url)
    return formatted_url


def download(url: str, output_path: str):
    if not os.path.exists(output_path):
        raise FileNotFoundError(output_path)
    elif not os.path.isdir(output_path):
        raise IsADirectoryError(output_path)

    page = requests.get(url)
    if page.status_code == 200:
        soup = BeautifulSoup(page.text, "html.parser")
        formatted_url = format_url(url)
        file_name = os.path.join(output_path, formatted_url + FILE_EXT)
        # path_to_images = os.path.join(output_path, formatted_url + END_PATH_TO_IMAGES)
        replace_img_src(soup, url, formatted_url + END_PATH_TO_IMAGES)
        save_html(soup, file_name)
        return file_name


def save_html(soup: BeautifulSoup, file_name: str):
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(soup.prettify())


def replace_img_src(soup: BeautifulSoup, url: str, path_to_images: str):
    images = soup.findAll('img')
    hostname = urlparse(url).hostname
    if hostname:
        hostname = hostname.replace('.', DELIMETER)
    for img in images:
        new_src = hostname + img['src'].replace('/', DELIMETER)
        img['src'] = os.path.join(path_to_images, new_src)


def save_images():
    pass
