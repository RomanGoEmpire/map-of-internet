import asyncio
import logging
from code.obsidian import Obsidian
from code.requestor import get_content, get_links, get_title
from collections import deque
from urllib.parse import urlparse

import keyboard
from colorlog import ColoredFormatter


def get_domain_name(url):
    parsed_url = urlparse(url)
    # The netloc attribute contains the domain name
    domain_name = parsed_url.netloc
    return domain_name


def cleanup_links(url, links):
    links = [get_domain_name(link) for link in links]
    # Remove empty links
    links = [link for link in links if link]
    set_links = set(links)
    # remove the url itself
    set_links.discard(url)
    return list(set_links)


def scrape(url_stack, obsidian, visited, logger):
    url = url_stack.popleft()
    if url in visited:
        logger.debug(f"Already visited {url}")
        return url_stack, visited
    url_search = f"https://{url}"
    logger.info(f"Requesting {url_search}")

    content = get_content(url_search, logger)
    if not content:
        return url_stack, visited
    title = get_title(content)
    links = get_links(content)

    visited.append(url)

    if links:
        links = cleanup_links(url, links)
        url_stack.extend(links)
    logger.debug(f"Links : {links}")

    if not obsidian.is_in_directory(url):
        logger.debug(f"New url: {url}")
        obsidian.save_node(title, url, links)

    return url_stack, visited


def cmd_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Create a console handler with colored output using colorlog
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # Define a colored formatter
    formatter = ColoredFormatter(
        "%(log_color)s%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        },
    )
    console_handler.setFormatter(formatter)

    # Add the console handler to the logger
    logger.addHandler(console_handler)
    return logger


def main():
    logger = cmd_logger()
    path = None  # path to your obsidian vault
    starting_url = "www.googl.com"
    url_stack = deque([starting_url])

    obsidian = Obsidian(path)
    counter = 0  # if you want to stop the script after x iterations
    visited = []
    while url_stack:
        if keyboard.is_pressed("esc"):
            break
        logger.info(f"Stack size: {len(url_stack)}")
        url_stack, visited = scrape(url_stack, obsidian, visited, logger)
        if counter > 1000:
            break
        counter += 1


if __name__ == "__main__":
    main()
