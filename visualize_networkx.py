import sqlite3

import networkx as nx
from pyvis.network import Network


def get_connection():
    conn = sqlite3.connect("internet.db")
    return conn


def close_connection(conn):
    conn.close()


def execute_query(query):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query)
    result = cur.fetchall()
    close_connection(conn)
    return result


def get_websites():
    query = "SELECT * FROM websites"
    return execute_query(query)


def get_links():
    query = "SELECT * FROM links"
    return execute_query(query)


def get_url(website_id):
    query = f"SELECT url FROM websites WHERE id = {website_id}"
    result = execute_query(query)
    return result[0][0]


# Get websites and links
websites = get_websites()
links = get_links()

# Create a graph
G = nx.DiGraph()

# Add nodes
for website in websites:
    G.add_node(website[1])

# Add edges
for link in links:
    source = get_url(link[1])
    destination = get_url(link[2])
    G.add_edges_from([(source, destination)])

# Create a network graph
nt = Network(notebook=True)

# Pass NetworkX graph to pyvis
nt.from_nx(G)

# Show the graph
nt.show("graph.html")
