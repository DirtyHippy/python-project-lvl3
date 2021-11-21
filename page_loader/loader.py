import re
import os
from bs4 import BeautifulSoup  # type: ignore
from progress.bar import Bar  # type: ignore
from urllib.parse import urlparse, urljoin
from page_loader.network_utils import save_resource, get_html, save_html, get_resource
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


def format_resource_name(url: str, resource_path: str):
    resource_name, resource_ext = os.path.splitext(resource_path)
    parsed_resource = urlparse(resource_name)
    if resource_ext == '':
        resource_ext = FILE_EXT
    parsed_path = parsed_resource.path
    return format_url(urljoin(url, parsed_path)) + resource_ext


def download(url: str, output_path: str = os.getcwd()):
    check_output_path(output_path)
    soup = BeautifulSoup(get_html(url), PARSER)
    formatted_url = format_url(url)
    full_resource_path = os.path.join(output_path, formatted_url + POSTFIX_RESOURCE_PATH)
    make_dir(full_resource_path)
    replace_resources(soup, url, full_resource_path)
    full_file_name = os.path.join(output_path, formatted_url + FILE_EXT)
    save_html(soup.prettify(), full_file_name)
    return full_file_name


def is_local_resource(resource_path: str, url: str) -> bool:
    parsed_resource_path = urlparse(resource_path)
    parsed_url = urlparse(url)
    return not parsed_resource_path.netloc or parsed_url.netloc == parsed_resource_path.netloc


def replace_resources(soup: BeautifulSoup, url: str, resource_path: str):
    downloaded_resources = set()
    found_resources = soup.findAll(list(RESOURCES.keys()))
    bar = Bar('Processing', max=len(found_resources))
    for resource in found_resources:
        inner_tag = RESOURCES[resource.name]
        resource_path_orig = resource.get(inner_tag)
        if not resource_path_orig or not is_local_resource(resource_path_orig, url):
            bar.next()
            continue
        resource_path_new = format_resource_name(url, resource_path_orig)
        resource_url = urljoin(url, resource_path_orig)
        full_resource_path = os.path.join(resource_path, resource_path_new)
        resource[inner_tag] = os.path.join(os.path.basename(resource_path), resource_path_new)
        if full_resource_path not in downloaded_resources:
            response = get_resource(resource_url)
            if response:
                if save_resource(response, full_resource_path):
                    downloaded_resources.add(full_resource_path)
        bar.next()
