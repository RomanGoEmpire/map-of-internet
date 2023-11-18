import os
from urllib.parse import urlparse


def get_domain_name(url):
    parsed_url = urlparse(url)
    domain_name = parsed_url.netloc
    return domain_name


def cleanup_links(url, links):
    new_links = []
    for link in links:
        if link and link.startswith("http" or "https" or "www"):
            new_links.append(format_url_to_valid_path(get_domain_name(link)))
    set_links = set(new_links)
    set_links.discard(url)
    return list(set_links)


def format_url_to_valid_path(url):
    url_headline = (
        url.replace("https://", "").replace("www.", "").replace("http://", "")
    )
    return url_headline


def template_website(title, url, links, cleaned_links):
    original_links = [
        f"- {link}" for link in links if link and not link.startswith("/" or "#")
    ]
    return f"""---
url: {get_domain_name(url)}
---
# {title}
---
## Links
---
{"\n".join([f"- [[{link}]]" for link in cleaned_links])}

## Original links
---
{"\n".join(original_links)}
"""


class Obsidian:
    def __init__(self, path) -> None:
        self.path = path

    def save_node(self, title, url, links, cleaned_links):
        url_headline = format_url_to_valid_path(url)

        with open(
            f"{os.path.join(self.path, url_headline)}.md", "w", encoding="utf-8"
        ) as f:
            f.write(template_website(title, url, links, cleaned_links))

    def format_links(self, links):
        return [format_url_to_valid_path(link) for link in links]

    def is_in_directory(self, url):
        url = format_url_to_valid_path(url)
        return os.path.exists(os.path.join(self.path, url))
