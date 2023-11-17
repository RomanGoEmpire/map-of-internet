import requests
from bs4 import BeautifulSoup


def get_content(url, logger):
    try:
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            logger.error(f"Error {r.status_code} for url {url}")
            return None
    except requests.exceptions.ConnectionError:
        logger.error(f"Connection error for url {url}")
        return None
    except requests.exceptions.Timeout:
        logger.error(f"Timeout error for url {url}")
        return None
    return r.text


def get_links(html):
    soup = BeautifulSoup(html, "html.parser")
    links = soup.findAll("a")
    links = [link.get("href") for link in links]
    return links


def get_title(html):
    soup = BeautifulSoup(html, "html.parser")
    try:
        title = soup.title.string
    except AttributeError:
        return None
    return title
