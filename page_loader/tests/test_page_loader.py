import tempfile
import os
import pytest
from requests.models import HTTPError
from page_loader.loader import download, PARSER, POSTFIX_RESOURCE_PATH
from bs4 import BeautifulSoup  # type: ignore
from requests_mock import ANY
from page_loader.exceptions import AppInternalError
from urllib.parse import urlparse, urljoin


SIMPLE_URL = 'http://www.simplehtmlguide.com/examples/images2.html'
COURCES_URL = 'https://ru.hexlet.io/courses'

SIMPLE_RESOURCES = [
    (
        '/examples/photo.jpg',
        'www-simplehtmlguide-com-examples-photo.jpg'
    )
]

COURCES_RESOURCES = [
    (
        '/courses',
        'ru-hexlet-io-courses.html'
    ),
    (
        '/assets/application.css',
        'ru-hexlet-io-assets-application.css'
    ),
    (
        '/assets/professions/nodejs.png',
        'ru-hexlet-io-assets-professions-nodejs.png'
    ),
    (
        '/packs/js/runtime.js',
        'ru-hexlet-io-packs-js-runtime.js'
    ),
]


def get_fixture_path(file_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, 'fixtures', file_name)


def read(file_path, mode='r'):
    with open(file_path, mode) as f:
        result = f.read()
    return result


def test_app_internal_error(requests_mock):
    requests_mock.get(COURCES_URL, exc=HTTPError)
    with pytest.raises(AppInternalError):
        with tempfile.TemporaryDirectory():
            download(COURCES_URL)


@pytest.mark.parametrize("output_path", ['', os.path.abspath(__file__)])
def test_os_error(requests_mock, output_path):
    requests_mock.get(ANY, text='any resourse')
    with pytest.raises(AppInternalError):
        with tempfile.TemporaryDirectory():
            download(SIMPLE_URL, output_path)


@pytest.mark.parametrize("test_file, result_expected, resources_expected, url, resources", [
    ('simple.html', 'simple_expected.html', 'simple_resources_expected.txt', SIMPLE_URL, SIMPLE_RESOURCES),         # noqa E501
    ('courses.html', 'courses_expected.html', 'courses_resources_expected.txt', COURCES_URL, COURCES_RESOURCES)])   # noqa E501
def test_download(requests_mock, test_file, result_expected, resources_expected, url, resources):
    netloc = urlparse(url).netloc
    for resource in resources:
        resource_path, downloaded_resource = resource
        requests_mock.get(urljoin(netloc, resource_path), content=read(
            get_fixture_path(downloaded_resource), 'rb'))
    requests_mock.get(url, text=read(get_fixture_path(test_file)))
    with tempfile.TemporaryDirectory() as tmpdirname:
        file_name = download(url, tmpdirname)
        soup_expected = BeautifulSoup(
            read(get_fixture_path(result_expected)), PARSER)
        assert read(file_name) == soup_expected.prettify()
        name, _ = os.path.splitext(file_name)
        resources_list = os.listdir(name + POSTFIX_RESOURCE_PATH)
        resources_expected = read(get_fixture_path(resources_expected)).split()
        assert sorted(resources_list) == sorted(resources_expected)
        for resource in resources:
            _, downloaded_resource = resource
            assert read(get_fixture_path(downloaded_resource), 'rb') == read(
                os.path.join(name + POSTFIX_RESOURCE_PATH, downloaded_resource), 'rb',)
