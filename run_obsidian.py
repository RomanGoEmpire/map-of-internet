import asyncio
import logging
import os
import time
from code.obsidian import Obsidian, cleanup_links
from collections import deque

import aiohttp
import keyboard
from bs4 import BeautifulSoup
from colorlog import ColoredFormatter


def cmd_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

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


async def fetch_content(url, session):
    await asyncio.sleep(0.1)
    try:
        logger.debug(f"Requesting {url}")
        url_link = f"https://{url}"
        async with session.get(url_link) as response:
            logger.debug(f"Received {url}")
            return await response.text(), url
    except Exception as e:
        logger.warning(f"Error for {url} - {e}")
        return None, url


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


def save_visited(visited):
    with open("visited.txt", "w") as f:
        for url in visited:
            f.write(f"{url}\n")


async def main():
    path = "C:\\Users\\gerlo\\CORE\\6 Obsidian\\Internet"
    url = "www.netthelp.de"

    obsidian = Obsidian(path)

    if os.path.exists("visited.txt") and input("Load visited? (y/n)") == "y":
        with open("visited.txt", "r") as f:
            visited = set(f.read().splitlines())
    else:
        visited = set()

    async with aiohttp.ClientSession() as session:
        tasks = {asyncio.create_task(fetch_content(url, session))}
        while tasks:
            if keyboard.is_pressed("q"):
                logger.info("Saving visited")
                save_visited(visited)
                session.close()
                break

            logger.info(f"Tasks: {len(tasks)}")
            done, tasks = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
            logger.info(f"Done: {len(done)}")
            for future in done:
                html, url = future.result()
                visited.add(url)

                if not html:
                    continue

                links = get_links(html)
                title = get_title(html)
                new_urls = cleanup_links(url, links)

                obsidian.save_node(title, url, links, new_urls)

                if new_urls:
                    logger.debug(f"Adding {len(new_urls)} new urls")
                    for new_url in new_urls:
                        if new_url not in visited:
                            tasks.add(
                                asyncio.create_task(fetch_content(new_url, session))
                            )
                        else:
                            logger.debug(f"{new_url} already visited")
            logger.info(f"Sleeping for 2 seconds")
            time.sleep(2)


if __name__ == "__main__":
    logger = cmd_logger()
    asyncio.run(main())
