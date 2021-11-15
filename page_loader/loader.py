import re
import os
from bs4 import BeautifulSoup  # type: ignore
from progress.bar import Bar  # type: ignore
from typing import Dict
from urllib.parse import ParseResult, urlparse, urljoin
from page_loader.network_utils import save_content, get_url
from page_loader.file_utils import check_output_path, make_dir


POSTFIX_RESOURCE_PATH = '_files'
FILE_EXT = '.html'
DELIMETER = '-'
RESOURCES = {'img': 'src',
             'link': 'href',
             'script': 'src'}
PARSER = "html.parser"


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


def download(url: str, output_path: str = os.getcwd()):
    check_output_path(output_path)
    response = get_url(url)
    soup = BeautifulSoup(response.text, PARSER)
    formatted_url = format_url(url)
    full_resource_path = os.path.join(output_path, formatted_url + POSTFIX_RESOURCE_PATH)
    make_dir(full_resource_path)
    save_resources(find_resources(soup), url, full_resource_path)
    full_file_name = os.path.join(output_path, formatted_url + FILE_EXT)
    save_content(soup.prettify(), full_file_name, 'w')
    return full_file_name


def find_resources(soup: BeautifulSoup) -> Dict[str, list]:
    return {tag: soup.findAll(tag) for tag in RESOURCES}


def is_local_res(parsed_res: ParseResult, parsed_url: ParseResult) -> bool:
    return not parsed_res.netloc or parsed_url.netloc == parsed_res.netloc


def save_resources(found_resources: Dict[str, list], url: str, resource_path: str):
    bar = Bar('Processing', max=sum([len(val) for val in found_resources.values()]))
    for tag, resources in found_resources.items():
        inner_tag = RESOURCES[tag]
        for res in resources:
            res_path_orig = res.get(inner_tag)
            if not res_path_orig:
                bar.next()
                continue
            parsed_res = urlparse(res_path_orig)
            parsed_url = urlparse(url)
            if not is_local_res(parsed_res, parsed_url):
                bar.next()
                continue
            res_path_new = format_res_name(url, res_path_orig)
            res_url = urljoin(url, res_path_orig)
            full_res_path = os.path.join(resource_path, res_path_new)
            res[inner_tag] = os.path.join(os.path.basename(resource_path), res_path_new)
            if not os.path.isfile(full_res_path):
                response = get_url(res_url)
                save_content(response.content, full_res_path, 'wb')
            bar.next()
