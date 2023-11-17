import os
import sqlite3


def create_table_website(
    path,
    database_name,
    name,
):
    path = os.path.join(path, f"{database_name}.db")
    conn = sqlite3.connect(path)
    cur = conn.cursor()

    # create a table to store the data
    # drop the table if it already exists
    cur.execute(f"DROP TABLE IF EXISTS {name}")
    cur.execute(
        f"""CREATE TABLE IF NOT EXISTS {name} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT NOT NULL
        )"""
    )
    conn.commit()
    conn.close()


def create_table_links(
    path,
    database_name,
    name,
):
    path = os.path.join(path, f"{database_name}.db")
    conn = sqlite3.connect(path)
    cur = conn.cursor()

    # create a table to store the data
    cur.execute(f"DROP TABLE IF EXISTS {name}")
    cur.execute(
        f"""CREATE TABLE IF NOT EXISTS {name} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source INTEGER NOT NULL,
        destination INTEGER NOT NULL,
        FOREIGN KEY (source) REFERENCES websites(id),
        FOREIGN KEY (destination) REFERENCES websites(id)
        )"""
    )
    conn.commit()
    conn.close()


def add_row(database, table, **kwargs):
    conn = sqlite3.connect(database)
    cur = conn.cursor()

    # add a row to the table
    values = tuple(kwargs.values())
    columns = ", ".join(kwargs.keys())

    # Prepare the placeholders for the values
    placeholders = ", ".join("?" * len(values))

    # Prepare the SQL command
    sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

    # Execute the SQL command
    cur.execute(sql, values)

    conn.commit()
    conn.close()


def get_id(database, table, url):
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute(f"SELECT id FROM {table} WHERE url = '{url}'")
    result = cur.fetchone()
    conn.close()
    return result[0]


def is_in_db(database, table, url):
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute(f"SELECT id FROM {table} WHERE url = '{url}'")
    result = cur.fetchone()
    conn.close()
    return bool(result)
