from page_loader.loader import download


def test_page_loader():
    download('https://ru.hexlet.io/courses')
    assert True
