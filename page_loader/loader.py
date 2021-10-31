import requests
from bs4 import BeautifulSoup  # type: ignore


PATH_TO_SOURCE = '_files'


def download(url: str, output: str):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    print(soup)
