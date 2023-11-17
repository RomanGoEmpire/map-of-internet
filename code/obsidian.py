import asyncio
import os

import aiofiles


def template_website(title, url, links):
    links_string = "\n".join([f"- [[{link}]]" for link in links])
    return f"""---
Title: "[[{title}]]"
url: {url}
tags:
    - website
---
# {title}
---
## Links
---
{links_string}
"""


def no_title_template(url, links):
    links_string = "\n".join([f"- [[{link}]]" for link in links])
    return f"""---
url: {url}
tags:
    - website
---
## Links
---
{links_string}
"""


def template_title_page(title):
    return f"""---
Title: {title}
tags:
    - website_title
---
# {title}
"""


class Obsidian:
    def __init__(self, path) -> None:
        self.path = path

    def save_node(self, title, url, links):
        url_headline = url.replace("https://", "")
        url_headline = url_headline.replace("/", "_")

        if title:
            # cleanu up title
            title = title.replace("|", " ")
            title = title.replace(":", " ")
            title = title.replace("?", " ")
            title = title.replace("*", " ")
            title = title.replace('"', " ")
            title = title.replace("<", " ")
            title = title.replace(">", " ")
            title = title.replace("\\", " ")
            title = title.replace("/", " ")
            title = title.replace("  ", " ")
            title = title.replace("\n", " ")
            title = title.replace("\t", " ")
            title = title.replace("\r", " ")

            with open(
                f"{os.path.join(self.path, url_headline)}.md", "w", encoding="utf-8"
            ) as f:
                f.write(template_website(title, url, links))
            with open(
                f"{os.path.join(self.path, title)}.md", "w", encoding="utf-8"
            ) as f:
                f.write(template_title_page(title))
        else:
            with open(
                f"{os.path.join(self.path, url_headline)}.md", "w", encoding="utf-8"
            ) as f:
                f.write(no_title_template(url, links))

    def format_url_to_valid_path(self, url):
        url_headline = url.replace("https://", "")
        url_headline = url_headline.replace("/", "_")
        return url_headline

    def format_links(self, links):
        return [self.format_url_to_valid_path(link) for link in links]

    def is_in_directory(self, url):
        url = self.format_url_to_valid_path(url)
        return os.path.exists(os.path.join(self.path, url))
