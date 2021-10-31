import requests
from bs4 import BeautifulSoup


def download(url: str):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    print(soup)
