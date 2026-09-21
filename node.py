class Node:
    def __init__(self, id, node_type_id, content):
        self.id = id
        self.node_type_id = node_type_id
        self.content = content


class NodeType:
    def __init__(self, id, name, scheme, scheme_font):
        self.id = id
        self.name = name
        self.scheme = scheme
        self.scheme_font = scheme_font


class Edge:
    def __init__(self, id, edge_type_id, source_node_id, target_node_id):
        self.id = id
        self.edge_type_id = edge_type_id
        self.source_node_id = source_node_id
        self.target_node_id = target_node_id


class EdgeType:
    def __init__(self, id, name):
        self.id = id
        self.name = name
