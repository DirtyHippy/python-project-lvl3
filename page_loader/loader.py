import requests
import re
import os
from bs4 import BeautifulSoup  # type: ignore
from urllib.parse import urlparse, urljoin
import logging
from progress.bar import Bar  # type: ignore


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


def download(url: str, output_path: str = os.getcwd()):
    if not os.path.exists(output_path):
        raise FileNotFoundError(output_path)
    elif not os.path.isdir(output_path):
        raise IsADirectoryError(output_path)

    try:
        response = requests.get(url)
    except requests.exceptions.RequestException:
        error_msg = f"Can't download url {url}"
        logging.error(error_msg)
        raise Exception(error_msg)

    soup = BeautifulSoup(response.text, "html.parser")
    formatted_url = format_url(url)
    full_file_name = os.path.join(output_path, formatted_url + FILE_EXT)
    resource_path = formatted_url + POSTFIX_RESOURCE_PATH
    save_all_resources(soup, url, output_path, resource_path)
    save_html(soup, full_file_name)
    return full_file_name


def save_html(soup: BeautifulSoup, full_file_name: str):
    with open(full_file_name, 'w', encoding='utf-8') as f:
        f.write(soup.prettify())


def save_all_resources(soup: BeautifulSoup,
                       url: str,
                       output_path: str,
                       resource_path: str):
    bar = Bar('Processing', max=len(soup.findAll(list(RESOURCES.keys()))))
    full_resource_path = os.path.join(output_path, resource_path)
    try:
        os.mkdir(full_resource_path)
    except OSError:
        error_msg = f"Can't create directory {full_resource_path}"
        logging.error(error_msg)
        raise OSError(error_msg)
    for tag, inner_tag in RESOURCES.items():
        save_resource(soup, tag, inner_tag, url, full_resource_path, bar)


def save_resource(soup: BeautifulSoup,
                  tag: str,
                  inner_tag: str,
                  url: str,
                  resource_path: str,
                  bar: Bar):

    for res in soup.findAll(tag):
        res_name = os.path.basename(res[inner_tag])
        hostname = urlparse(url).hostname
        if hostname is not None:
            hostname_replaced = replace_characters(hostname)
        res_name_new = f'{hostname_replaced}{DELIMETER}{res_name}'
        res_url = urljoin(url, res.get(inner_tag))
        res_path = os.path.join(resource_path, res_name)
        res[inner_tag] = os.path.join(os.path.basename(resource_path), res_name_new)
        if not os.path.isfile(res_path):
            response = requests.get(res_url)
            with open(res_path, 'wb') as file:
                file.write(response.content)
        bar.next()
