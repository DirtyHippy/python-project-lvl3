import tempfile
import os
import pytest
from page_loader.loader import download
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

URL = 'http://www.simplehtmlguide.com/examples/images2.html'
IMAGE_URL = 'http://www.simplehtmlguide.com/examples/photo.jpg'
COURCES_URL = 'https://ru.hexlet.io/courses'


def get_fixture_path(file_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, 'fixtures', file_name)


def read(file_path, mode: str = 'r'):
    with open(file_path, mode) as f:
        result = f.read()
    return result


def read_image(file_path):
    with open(file_path, 'rb') as f:
        result = f.read()
    return result


def test_file_not_found_error():
    with pytest.raises(FileNotFoundError):
        download(URL, '')


def test_is_a_directory_error():
    with pytest.raises(IsADirectoryError):
        download(URL, os.path.abspath(__file__))


def test_simple_page(requests_mock):
    requests_mock.get(URL, text=read(get_fixture_path('page.html')))
    requests_mock.get(IMAGE_URL, content=read(get_fixture_path('image_expected.jpg'), 'rb'))
    with tempfile.TemporaryDirectory() as tmpdirname:
        file_name = download(URL, tmpdirname)
        soup_expected = BeautifulSoup(
            read(get_fixture_path('page_expected.html')), "html.parser")
        assert read(file_name) == soup_expected.prettify()


def test_cources(requests_mock):
    requests_mock.get(ANY, text='any resourse')
    requests_mock.get(COURCES_URL, text=read(get_fixture_path('courses.html')))
    with tempfile.TemporaryDirectory() as tmpdirname:
        file_name = download(COURCES_URL, tmpdirname)
        soup_expected = BeautifulSoup(
            read(get_fixture_path('courses_expected.html')), "html.parser")
        assert read(file_name) == soup_expected.prettify()
