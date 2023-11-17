import os
from code.database import add_row, create_table_links, create_table_website, get_id
from code.requestor import get_content, get_links, get_title

if __name__ == "__main__":
    # create a table to store the data
    database = "internet.db"
    path = os.getcwd()
    create_table_website(path, "internet", "websites")
    create_table_links(path, "internet", "links")

    url_stack = []
    url_stack.append("https://google.com")

    url = url_stack.pop()
    content = get_content(url)
    title = get_title(content)
    links = get_links(content)

    add_row(database=database, table="websites", title=title, url=url)

    for link in links:
        if link.startswith("/"):
            link = url + link
        url_stack.append(link)
        link_content = get_content(link)
        link_title = get_title(content)

        add_row(database=database, table="websites", title=link_title, url=link)
        id_current = get_id(database=database, table="websites", title=title, url=url)
        id_link = get_id(
            database=database, table="websites", title=link_title, url=link
        )
        add_row(
            database=database,
            table="links",
            source=id_current,
            destination=id_link,
        )
