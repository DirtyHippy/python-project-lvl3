import tempfile
import os
import pytest
from page_loader.loader import download, PARSER
from bs4 import BeautifulSoup  # type: ignore
from requests_mock import ANY

IMAGE_TAG = 'img'
LINK_TAG = 'link'
SCRIPT_TAG = 'script'
SRC_ATTR = 'src'
HREF_ATTR = 'href'
TAGS_ATTR = {
    IMAGE_TAG: SRC_ATTR,
    LINK_TAG: HREF_ATTR,
    SCRIPT_TAG: SRC_ATTR,
}

SIMPLE_URL = 'http://www.simplehtmlguide.com/examples/images2.html'
COURCES_URL = 'https://ru.hexlet.io/courses'


def get_fixture_path(file_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, 'fixtures', file_name)


def read(file_path, mode: str = 'r'):
    with open(file_path, mode) as f:
        result = f.read()
    return result


@ pytest.mark.parametrize("output_path", ['',                          # FileNotFoundError
                                          os.path.abspath(__file__)])  # IsADirectoryError
def test_os_error(requests_mock, output_path):
    requests_mock.get(ANY, text='any resourse')
    with pytest.raises(OSError):
        with tempfile.TemporaryDirectory():
            download(SIMPLE_URL, output_path)


@ pytest.mark.parametrize("test_file, result_expected, url", [
    ('page.html', 'page_expected.html', SIMPLE_URL),
    ('courses.html', 'courses_expected.html', COURCES_URL)])
def test_download(requests_mock, test_file, result_expected, url):
    requests_mock.get(ANY, text='any resourse')
    requests_mock.get(url, text=read(get_fixture_path(test_file)))
    with tempfile.TemporaryDirectory() as tmpdirname:
        file_name = download(url, tmpdirname)
        soup_expected = BeautifulSoup(
            read(get_fixture_path(result_expected)), PARSER)
        assert read(file_name) == soup_expected.prettify()
