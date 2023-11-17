import os
import sqlite3
from code.database import (
    add_row,
    create_table_links,
    create_table_website,
    get_id,
    is_in_db,
)
from code.requestor import get_content, get_links, get_title


def scrape(url, url_stack, database):
    
    # get the content of the url
    url = url_stack.pop(0)
    url = url.rstrip("/")

    print(f"Scraping: {url}")
    content = get_content(url)
    links = get_links(url, content)

    # add the url to the database
    add_row(database=database, table="websites", url=url)

    if not links:
        return url_stack
        
    for link in links:
        if link is None:
            continue
        # elif link.startswith("#"):
        #     continue
        # elif link.startswith("/"):
        #     # TODO add some logic to handle that link = url + link works
        #     continue

        # only keep the links that start with http

        if not link.startswith("http" or "https" or "www" or "ftp"):
            continue
        link = link.rstrip("/")
        
        if is_in_db(database=database, table="websites", url=link):
            continue
            
        print(f"Added: {link}")
        url_stack.append(link)

        # add the link to the database
        add_row(database=database, table="websites", url=link)
        
        # add the connection to the database
        id_current = get_id(database=database, table="websites", url=url)
        id_link = get_id(database=database, table="websites", url=link)
        add_row(
            database=database,
            table="links",
            source=id_current,
            destination=id_link,
        )
    return url_stack


if __name__ == "__main__":
    # create a table to store the data
    database = "internet.db"
    path = os.getcwd()

    # create database if it doesnt exist
    if not database in os.listdir(path):
        conn = sqlite3.connect(database)
        conn.close()
    # reset tables (temporary)
    create_table_website(path, "internet", "websites")
    create_table_links(path, "internet", "links")

    # it would go forever otherwise.
    counter = 100
    
    url_stack = []
    url_stack.append("https://www.riotgames.com/")

    while counter > 0:
        print("###############################################")
        print(len(url_stack))
        url_stack = scrape(url_stack=url_stack, url=url_stack, database=database)
        counter -= 1
