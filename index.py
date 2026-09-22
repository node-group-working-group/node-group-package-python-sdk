from .sql import SqliteDatabase


def initialize(path):
    pass


def insert_node(path, url, _type=None):
    pass


def delete_node_by_id(path, id):
    pass


def get_all_nodes(path, _type=None):
    pass


def get_node_by_id(path, id):
    pass


def get_nodes_by_url_match(path, url_match):
    pass


def set_node_by_id(path, id, url=None, _type=None, content=None):
    pass


def create_node_type(path, name):
    pass


def delete_node_type_by_name(path, name):
    pass


def get_node_type_by_name(path, name):
    pass


def get_all_node_types(path):
    pass


def update_node_type_by_name(
    path, current_name, name=None, scheme=None, scheme_font=None
):
    pass


def insert_edge(path, source_node_id, target_node_id, _type=None):
    pass


def delete_edge_by_id(path, id):
    pass


def get_all_edges(path):
    pass


def get_edges_by_edge_type_name(path, edge_type_name):
    pass


def get_edge_by_id(path, id):
    pass


def get_edges_by_node_id(path, node_id):
    pass


def set_edge_by_id(
    path, id, source_node_id=None, _type=None, target_node_id=None
):
    pass


def create_edge_type(path, name):
    pass


def delete_edge_type_by_name(path, name):
    pass


def get_edge_type_by_name(path, name):
    pass


def get_all_edge_types(path):
    pass


def update_edge_type_by_name(path, current_name, name=None):
    pass
