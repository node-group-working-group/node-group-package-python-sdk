from sql import SqliteDatabase
from node import Edge, EdgeType, Node, NodeType

_NODE_COLUMNS = "id, url, node_type_id, content"
_NODE_TYPE_COLUMNS = "id, name, scheme, scheme_font"
_EDGE_COLUMNS = "id, edge_type_id, source_node_id, target_node_id"
_EDGE_TYPE_COLUMNS = "id, name"


def _to_node(row):
    if row is None:
        return None
    return Node(*row)


def _to_node_type(row):
    if row is None:
        return None
    return NodeType(*row)


def _to_edge(row):
    if row is None:
        return None
    return Edge(*row)


def _to_edge_type(row):
    if row is None:
        return None
    return EdgeType(*row)


def _resolve_node_type_id(database, name):
    database.execute("SELECT id FROM node_type WHERE name = ?", (name,))
    row = database.fetch_one()
    if row is None:
        raise ValueError(f"Node type '{name}' does not exist.")
    return row[0]


def _resolve_edge_type_id(database, name):
    database.execute("SELECT id FROM edge_type WHERE name = ?", (name,))
    row = database.fetch_one()
    if row is None:
        raise ValueError(f"Edge type '{name}' does not exist.")
    return row[0]


def initialize(path):
    with SqliteDatabase(path) as database:
        database.execute(
            "CREATE TABLE IF NOT EXISTS node_type ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "name TEXT NOT NULL UNIQUE, "
            "scheme TEXT, "
            "scheme_font TEXT)",
            (),
        )
        database.execute(
            "CREATE TABLE IF NOT EXISTS node ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "node_type_id INTEGER REFERENCES node_type(id), "
            "content TEXT, "
            "url TEXT)",
            (),
        )
        database.execute(
            "CREATE TABLE IF NOT EXISTS edge_type ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "name TEXT NOT NULL UNIQUE)",
            (),
        )
        database.execute(
            "CREATE TABLE IF NOT EXISTS edge ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "edge_type_id INTEGER REFERENCES edge_type(id), "
            "source_node_id INTEGER REFERENCES node(id), "
            "target_node_id INTEGER REFERENCES node(id))",
            (),
        )


def insert_node(path, url, _type=None):
    with SqliteDatabase(path) as database:
        if _type is None:
            database.execute("INSERT INTO node (url) VALUES (?)", (url,))
        else:
            database.execute(
                "INSERT INTO node (node_type_id, url) VALUES (?, ?)",
                (_resolve_node_type_id(database, _type), url),
            )
        return database.cursor.lastrowid


def delete_node_by_id(path, id):
    with SqliteDatabase(path) as database:
        database.execute(
            "DELETE FROM edge WHERE source_node_id = ? OR target_node_id = ?",
            (id, id),
        )
        database.execute("DELETE FROM node WHERE id = ?", (id,))
        return database.cursor.rowcount


def get_all_nodes(path, _type=None):
    with SqliteDatabase(path) as database:
        if _type is None:
            database.execute(f"SELECT {_NODE_COLUMNS} FROM node", ())
        else:
            database.execute(
                f"SELECT n.{_NODE_COLUMNS} FROM node AS n "
                "JOIN node_type AS t ON t.id = n.node_type_id "
                "WHERE t.name = ?",
                (_type,),
            )
        return [_to_node(row) for row in database.fetch_all()]


def get_node_by_id(path, id):
    with SqliteDatabase(path) as database:
        database.execute(
            f"SELECT {_NODE_COLUMNS} FROM node WHERE id = ?", (id,)
        )
        return _to_node(database.fetch_one())


def get_nodes_by_url_match(path, url_match):
    with SqliteDatabase(path) as database:
        database.execute(
            f"SELECT {_NODE_COLUMNS} FROM node WHERE url LIKE ?",
            (f"%{url_match}%",),
        )
        return [_to_node(row) for row in database.fetch_all()]


def set_node_by_id(path, id, url=None, _type=None, content=None):
    with SqliteDatabase(path) as database:
        sets = []
        params = []
        if url is not None:
            sets.append("url = ?")
            params.append(url)
        if _type is not None:
            sets.append("node_type_id = ?")
            params.append(_resolve_node_type_id(database, _type))
        if content is not None:
            sets.append("content = ?")
            params.append(content)
        if not sets:
            return 0
        params.append(id)
        database.execute(
            f"UPDATE node SET {', '.join(sets)} WHERE id = ?", tuple(params)
        )
        return database.cursor.rowcount


def create_node_type(path, name):
    with SqliteDatabase(path) as database:
        database.execute("INSERT INTO node_type (name) VALUES (?)", (name,))
        return database.cursor.lastrowid


def delete_node_type_by_name(path, name):
    with SqliteDatabase(path) as database:
        database.execute("SELECT id FROM node_type WHERE name = ?", (name,))
        row = database.fetch_one()
        if row is None:
            return 0

        node_type_id = row[0]
        database.execute(
            "SELECT COUNT(*) FROM node WHERE node_type_id = ?", (node_type_id,)
        )
        count = database.fetch_one()[0]
        if count:
            raise ValueError(
                f"Cannot delete node type '{name}': {count} node(s) reference it."
            )

        database.execute("DELETE FROM node_type WHERE id = ?", (node_type_id,))
        return database.cursor.rowcount


def get_node_type_by_name(path, name):
    with SqliteDatabase(path) as database:
        database.execute(
            f"SELECT {_NODE_TYPE_COLUMNS} FROM node_type WHERE name = ?",
            (name,),
        )
        return _to_node_type(database.fetch_one())


def get_all_node_types(path):
    with SqliteDatabase(path) as database:
        database.execute(f"SELECT {_NODE_TYPE_COLUMNS} FROM node_type", ())
        return [_to_node_type(row) for row in database.fetch_all()]


def update_node_type_by_name(
    path, current_name, name=None, scheme=None, scheme_font=None
):
    with SqliteDatabase(path) as database:
        sets = []
        params = []
        if name is not None:
            sets.append("name = ?")
            params.append(name)
        if scheme is not None:
            sets.append("scheme = ?")
            params.append(scheme)
        if scheme_font is not None:
            sets.append("scheme_font = ?")
            params.append(scheme_font)
        if not sets:
            return 0
        params.append(current_name)
        database.execute(
            f"UPDATE node_type SET {', '.join(sets)} WHERE name = ?",
            tuple(params),
        )
        return database.cursor.rowcount


def insert_edge(path, source_node_id, target_node_id, _type=None):
    with SqliteDatabase(path) as database:
        if _type is None:
            edge_type_id = None
        else:
            edge_type_id = _resolve_edge_type_id(database, _type)
        database.execute(
            "INSERT INTO edge (edge_type_id, source_node_id, target_node_id) "
            "VALUES (?, ?, ?)",
            (edge_type_id, source_node_id, target_node_id),
        )
        return database.cursor.lastrowid


def delete_edge_by_id(path, id):
    with SqliteDatabase(path) as database:
        database.execute("DELETE FROM edge WHERE id = ?", (id,))
        return database.cursor.rowcount


def get_all_edges(path, _type):
    with SqliteDatabase(path) as database:
        if _type is None:
            database.execute(f"SELECT {_EDGE_COLUMNS} FROM edge", ())
        else:
            database.execute(
                f"SELECT e.{_EDGE_COLUMNS} FROM edge AS e "
                "JOIN edge_type AS t ON t.id = e.edge_type_id "
                "WHERE t.name = ?",
                (_type,),
            )
        return [_to_edge(row) for row in database.fetch_all()]


def get_edges_by_edge_type_name(path, edge_type_name):
    with SqliteDatabase(path) as database:
        database.execute(
            f"SELECT e.{_EDGE_COLUMNS} FROM edge AS e "
            "JOIN edge_type AS t ON t.id = e.edge_type_id "
            "WHERE t.name = ?",
            (edge_type_name,),
        )
        return [_to_edge(row) for row in database.fetch_all()]


def get_edge_by_id(path, id):
    with SqliteDatabase(path) as database:
        database.execute(
            f"SELECT {_EDGE_COLUMNS} FROM edge WHERE id = ?", (id,)
        )
        return _to_edge(database.fetch_one())


def get_edges_by_node_id(path, node_id):
    with SqliteDatabase(path) as database:
        database.execute(
            f"SELECT {_EDGE_COLUMNS} FROM edge "
            "WHERE source_node_id = ? OR target_node_id = ?",
            (node_id, node_id),
        )
        return [_to_edge(row) for row in database.fetch_all()]


def set_edge_by_id(
    path, id, source_node_id=None, _type=None, target_node_id=None
):
    with SqliteDatabase(path) as database:
        sets = []
        params = []
        if source_node_id is not None:
            sets.append("source_node_id = ?")
            params.append(source_node_id)
        if target_node_id is not None:
            sets.append("target_node_id = ?")
            params.append(target_node_id)
        if _type is not None:
            sets.append("edge_type_id = ?")
            params.append(_resolve_edge_type_id(database, _type))
        if not sets:
            return 0
        params.append(id)
        database.execute(
            f"UPDATE edge SET {', '.join(sets)} WHERE id = ?", tuple(params)
        )
        return database.cursor.rowcount


def create_edge_type(path, name):
    with SqliteDatabase(path) as database:
        database.execute("INSERT INTO edge_type (name) VALUES (?)", (name,))
        return database.cursor.lastrowid


def delete_edge_type_by_name(path, name):
    with SqliteDatabase(path) as database:
        database.execute("SELECT id FROM edge_type WHERE name = ?", (name,))
        row = database.fetch_one()
        if row is None:
            return 0

        edge_type_id = row[0]
        database.execute(
            "SELECT COUNT(*) FROM edge WHERE edge_type_id = ?", (edge_type_id,)
        )
        count = database.fetch_one()[0]
        if count:
            raise ValueError(
                f"Cannot delete edge type '{name}': {count} edge(s) reference it."
            )

        database.execute("DELETE FROM edge_type WHERE id = ?", (edge_type_id,))
        return database.cursor.rowcount


def get_edge_type_by_name(path, name):
    with SqliteDatabase(path) as database:
        database.execute(
            f"SELECT {_EDGE_TYPE_COLUMNS} FROM edge_type WHERE name = ?",
            (name,),
        )
        return _to_edge_type(database.fetch_one())


def get_all_edge_types(path):
    with SqliteDatabase(path) as database:
        database.execute(f"SELECT {_EDGE_TYPE_COLUMNS} FROM edge_type", ())
        return [_to_edge_type(row) for row in database.fetch_all()]


def update_edge_type_by_name(path, current_name, name=None):
    with SqliteDatabase(path) as database:
        if name is None:
            return 0
        database.execute(
            "UPDATE edge_type SET name = ? WHERE name = ?",
            (name, current_name),
        )
        return database.cursor.rowcount
