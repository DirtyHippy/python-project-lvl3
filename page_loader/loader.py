import requests
import re
import os
from bs4 import BeautifulSoup  # type: ignore
from urllib.parse import urlparse, urljoin
import logging
from progress.bar import Bar  # type: ignore
from typing import Dict, Any


POSTFIX_RESOURCE_PATH = '_files'
FILE_EXT = '.html'
DELIMETER = '-'
RESOURCES = {'img': 'src',
             'link': 'href',
             'script': 'src'}


def remove_scheme_from_url(url: str) -> str:
    parsed_url = urlparse(url)
    if parsed_url.scheme:
        scheme = f"{parsed_url.scheme}://"
        return parsed_url.geturl().replace(scheme, '', 1)
    return parsed_url.geturl()


def replace_characters(url: str) -> str:
    return re.sub(r"[^0-9a-zA-Z]", DELIMETER, url)


def format_url(url: str) -> str:
    formatted_url = remove_scheme_from_url(url)
    formatted_url = replace_characters(formatted_url)
    return formatted_url


def format_res_name(url: str, res_path: str):
    parsed_url = urlparse(url)
    res_name, res_ext = os.path.splitext(res_path)
    parsed_res = urlparse(res_name)
    if res_ext == '':
        res_ext = FILE_EXT
    parsed_path = parsed_res.path
    if not parsed_path.startswith('/'):
        parsed_path = '/' + parsed_path
    return replace_characters(f'{parsed_url.hostname}{parsed_path}') + res_ext


def get_url(url: str) -> Any:
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException:
        error_msg = f"Can't download url {url}"
        logging.error(error_msg)
        raise Exception(error_msg)
    return response


def download(url: str, output_path: str = os.getcwd()):
    if not os.path.exists(output_path):
        raise FileNotFoundError(output_path)
    elif not os.path.isdir(output_path):
        raise IsADirectoryError(output_path)

    response = get_url(url)

    soup = BeautifulSoup(response.text, "html.parser")
    formatted_url = format_url(url)
    full_file_name = os.path.join(output_path, formatted_url + FILE_EXT)
    resource_path = formatted_url + POSTFIX_RESOURCE_PATH
    save_resources(soup, url, output_path, resource_path)
    save_html(soup, full_file_name)
    return full_file_name


def save_html(soup: BeautifulSoup, full_file_name: str):
    with open(full_file_name, 'w', encoding='utf-8') as f:
        f.write(soup.prettify())


def save_resources(soup: BeautifulSoup,
                   url: str,
                   output_path: str,
                   resource_path: str):
    full_resource_path = os.path.join(output_path, resource_path)
    try:
        os.mkdir(full_resource_path)
    except OSError:
        error_msg = f"Can't create directory {full_resource_path}"
        logging.error(error_msg)
        raise OSError(error_msg)

    found_resources = {}
    for tag in RESOURCES:
        found_resources[tag] = soup.findAll(tag)
    get_resource(found_resources, url, full_resource_path)


def get_resource(found_resources: Dict[str, list],
                 url: str,
                 resource_path: str):
    bar = Bar('Processing', max=sum([len(val) for val in found_resources.values()]))
    for tag, resources in found_resources.items():
        inner_tag = RESOURCES[tag]
        for res in resources:
            res_path_orig = res.get(inner_tag)
            parsed_res = urlparse(res_path_orig)
            parsed_url = urlparse(url)
            if not parsed_res.netloc or parsed_url.netloc == parsed_res.netloc:
                res_path_new = format_res_name(url, res_path_orig)
                res_url = urljoin(url, res_path_orig)
                full_res_path = os.path.join(resource_path, res_path_new)
                res[inner_tag] = os.path.join(os.path.basename(resource_path), res_path_new)
                if not os.path.isfile(full_res_path):
                    response = get_url(res_url)
                    with open(full_res_path, 'wb') as file:
                        file.write(response.content)
            bar.next()
