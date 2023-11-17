import requests
from bs4 import BeautifulSoup


def get_content(url):
    print(f"Requesting {url}")
    r = requests.get(url)
    return r.text


def get_links(url, html):
    print(f"Getting links from {url}")
    soup = BeautifulSoup(html, "html.parser")
    links = soup.findAll("a")
    links = [link.get("href") for link in links]
    return links


def get_title(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.title.string
