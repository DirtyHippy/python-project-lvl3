import tempfile
import os
import pytest
from requests.models import HTTPError
from page_loader.loader import download, PARSER, POSTFIX_RESOURCE_PATH
from bs4 import BeautifulSoup  # type: ignore
from requests_mock import ANY
from page_loader.exceptions import AppInternalError


SIMPLE_URL = 'http://www.simplehtmlguide.com/examples/images2.html'
COURCES_URL = 'https://ru.hexlet.io/courses'


def get_fixture_path(file_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, 'fixtures', file_name)


def read(file_path):
    with open(file_path, 'r') as f:
        result = f.read()
    return result


def test_app_internal_error(requests_mock):
    requests_mock.get(COURCES_URL, exc=HTTPError)
    with pytest.raises(AppInternalError):
        with tempfile.TemporaryDirectory():
            download(COURCES_URL)


@pytest.mark.parametrize("output_path, exception", [
    ('', FileNotFoundError),
    (os.path.abspath(__file__), IsADirectoryError)])
def test_os_error(requests_mock, output_path, exception):
    requests_mock.get(ANY, text='any resourse')
    with pytest.raises(exception):
        with tempfile.TemporaryDirectory():
            download(SIMPLE_URL, output_path)


@pytest.mark.parametrize("test_file, result_expected, resources_expected, url", [
    ('simple.html', 'simple_expected.html', 'simple_resources_expected.txt', SIMPLE_URL),
    ('courses.html', 'courses_expected.html', 'courses_resources_expected.txt', COURCES_URL)])
def test_download(requests_mock, test_file, result_expected, resources_expected, url):
    requests_mock.get(ANY, text='any resourse')
    requests_mock.get(url, text=read(get_fixture_path(test_file)))
    with tempfile.TemporaryDirectory() as tmpdirname:
        file_name = download(url, tmpdirname)
        soup_expected = BeautifulSoup(
            read(get_fixture_path(result_expected)), PARSER)
        assert read(file_name) == soup_expected.prettify()
        name, _ = os.path.splitext(file_name)
        resources = os.listdir(name + POSTFIX_RESOURCE_PATH)
        resources_expected = read(get_fixture_path(resources_expected)).split()
        assert sorted(resources) == sorted(resources_expected)
