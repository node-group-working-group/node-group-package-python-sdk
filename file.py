import index
import os
import shutil
import tarfile
import tempfile

from .constants import ASSETS_DIRECTORY, INDEX_FILE, METADATA_FILE
from compression import zstd
from .metadata import Contributor, Metadata
from pathlib import Path


class File:
    def __init__(self):
        self._folder = None
        self.is_modified = False
        self.path = None

    def close(self):
        if self.folder and os.path.exists(self._folder):
            shutil.rmtree(self._folder)
        self._folder = None
        self.is_modified = False
        self.path = None

    def commit(self, path=None):
        _path = path or self.path

        if not _path:
            raise ValueError(
                "No saving location was provided. Try commit(path)."
            )

        if not self._folder or not os.path.exists(self._folder):
            raise RuntimeError("No active working directory.")

        with tarfile.open(_path, "w:zst") as tar:
            tar.add(self._folder, arcname=".")

        self.path = _path

    def insert_node(self, url, _type="article"):
        node_id = index.insert_node(Path(self._folder) / INDEX_FILE, url)

        if not self.get_node_type_by_name(_type):
            self.create_node_type(_type)

        self.set_node_by_id(node_id, _type_name=_type)

        return node_id

    def create_node_type(self, name):
        index.create_node_type(Path(self._folder) / INDEX_FILE, name)

    def insert_edge(self, source_node_id, target_node_id, _type="has_child"):
        if not (
            self.get_node_by_id(source_node_id)
            or self.get_node_by_id(target_node_id)
        ):
            return

        edge_id = index.insert_edge(
            Path(self._folder) / INDEX_FILE, source_node_id, target_node_id
        )

        if not self.get_edge_type_by_name(_type):
            self.create_edge_type(_type)

        self.set_edge_by_id(edge_id, _type_name=_type)

        return edge_id

    def create_edge_type(self, name):
        if not self.get_edge_type_by_name(name):
            index.create_edge_type(Path(self._folder) / INDEX_FILE, name)

    def delete_node_by_id(self, id):
        if self.get_node_by_id(id):
            index.delete_node_by_id(Path(self._folder) / INDEX_FILE, id)

    def delete_node_type_by_name(self, name):
        if self.get_node_type_by_name(name):
            index.delete_node_type_by_name(
                Path(self._folder) / INDEX_FILE, name
            )

    def delete_edge_by_id(self, id):
        if self.get_edge_by_id(id):
            index.delete_edge_by_id(Path(self._folder) / INDEX_FILE, id)

    def delete_edge_type_by_name(self, name):
        if self.get_edge_type_by_name(name):
            index.delete_edge_type_by_name(
                Path(self._folder) / INDEX_FILE, name
            )

    def get_node_by_id(self, id):
        return index.get_node_by_id(Path(self._folder) / INDEX_FILE, id)

    def get_all_nodes(self, _type=None):
        return index.get_all_nodes(Path(self._folder) / INDEX_FILE, _type)

    def match_nodes_by_url(self, url):
        return index.get_nodes_by_url_match(
            Path(self._folder) / INDEX_FILE, url
        )

    def get_node_type_by_name(self, name):
        return index.get_node_type_by_name(
            Path(self._folder) / INDEX_FILE, name
        )

    def get_all_node_types(self):
        return index.get_all_node_types(Path(self._folder) / INDEX_FILE)

    def get_edge_by_id(self, id):
        return index.get_edge_by_id(Path(self._folder) / INDEX_FILE, id)

    def get_all_edges(self):
        return index.get_all_edges(Path(self._folder) / INDEX_FILE)

    def get_edges_by_edge_type_name(self, edge_type_name):
        return index.get_edges_by_edge_type_name(
            Path(self._folder) / INDEX_FILE, edge_type_name
        )

    def get_edges_by_node_id(self, node_id):
        return index.get_edges_by_node_id(
            Path(self._folder) / INDEX_FILE, node_id
        )

    def get_edge_type_by_name(self, name):
        return index.get_edge_type_by_name(
            Path(self._folder) / INDEX_FILE, name
        )

    def get_all_edge_types(self):
        return index.get_all_edge_types(Path(self._folder) / INDEX_FILE)

    def get_node_asset_directory(self, id):
        pass

    def open_node_asset_directory(self, id):
        pass

    def upload_node_asset(self, id, asset_path):
        pass

    def set_node_by_id(self, id, url=None, _type_name=None, content=None):
        if self.get_node_by_id(id):
            index.set_node_by_id(
                Path(self._folder) / INDEX_FILE, id, url, _type_name, content
            )

    def update_node_type(
        self, current_name, name=None, scheme=None, scheme_font=None
    ):
        if self.get_node_type_by_name(current_name):
            index.update_node_type_by_name(
                current_name, name, scheme, scheme_font
            )

    def set_edge_by_id(
        self, id, source_node_id=None, _type_name=None, target_node_id=None
    ):
        if self.get_edge_by_id(id):
            index.set_edge_by_id(
                Path(self._folder) / INDEX_FILE,
                id,
                source_node_id,
                _type_name,
                target_node_id,
            )

    def update_edge_type(self, current_name, name=None):
        if self.get_edge_type_by_name(current_name):
            index.update_edge_type_by_name(
                Path(self._folder) / INDEX_FILE, current_name, name
            )

    def open(self, path=None, force=False):
        if not force and (self.path or self._folder):
            raise RuntimeError(
                "A .ngpk file is already loaded. Override with open(force=True, ...)."
            )
        else:
            self.close()

        self.path = path
        self._folder = tempfile.mkdtemp()

        if path:
            if not os.path.exists(path):
                raise FileNotFoundError(f"File '{path}' not found.")

            with tarfile.open(path, "r:zst") as tar:
                tar.extractall(path=self._folder)

        index.initialize(self._folder)
