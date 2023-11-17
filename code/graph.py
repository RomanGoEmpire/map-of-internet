import nographs as nog


def create_node(node_name):
    return nog.Node(node_name)


def create_directed_edge(node1, node2):
    return nog.DirectedEdge(node1, node2)


def save_graph(graph, filename):
    nog.save_graph(graph, filename)


def load_graph(filename):
    return nog.load_graph(filename)


def create_graph():
    return nog.Graph()
