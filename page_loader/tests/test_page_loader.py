from page_loader.loader import download
import pytest
import os
import tempfile

TEST_URL = 'https://ru.hexlet.io/courses'


def get_fixture_path(file_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, 'fixtures/', file_name)


def read(file_path):
    with open(file_path, 'r') as f:
        result = f.read()
    return result


def test_file_not_found_error():
    with pytest.raises(FileNotFoundError):
        download(TEST_URL, '')


def test_is_a_directory_error():
    with pytest.raises(IsADirectoryError):
        download(TEST_URL, os.path.abspath(__file__))


def test_replaced_src():
    with tempfile.TemporaryDirectory():
        pass


def test_image():
    with tempfile.TemporaryDirectory():
        pass
