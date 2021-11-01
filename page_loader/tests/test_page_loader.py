from page_loader.loader import download
import pytest
import os

TEST_URL = 'https://ru.hexlet.io/courses'


def test_file_not_found_error():
    with pytest.raises(FileNotFoundError):
        download(TEST_URL, '')


def test_is_a_directory_error():
    with pytest.raises(IsADirectoryError):
        download(TEST_URL, os.path.abspath(__file__))
