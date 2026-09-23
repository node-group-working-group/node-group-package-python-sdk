class Edge:
    def __init__(self, id, edge_type_id, source_node_id, target_node_id):
        self.id = id
        self.edge_type_id = edge_type_id
        self.source_node_id = source_node_id
        self.target_node_id = target_node_id

    def __str__(self):
        return f"{self.id}, {self.edge_type_id}, {self.source_node_id}, {self.target_node_id}"


class EdgeType:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return f"{self.id}, {self.name}"


class Node:
    def __init__(self, id, url, node_type_id, content):
        self.id = id
        self.url = url
        self.node_type_id = node_type_id
        self.content = content

    def __str__(self):
        return f"{self.id}, {self.url}, {self.node_type_id}"


class NodeType:
    def __init__(self, id, name, scheme, scheme_font):
        self.id = id
        self.name = name
        self.scheme = scheme
        self.scheme_font = scheme_font

    def __str__(self):
        return f"{self.id}, {self.name}, {self.scheme}, {self.scheme_font}"
