import hashlib
import index
import json
import os
import shutil
import tarfile
import tempfile

from constants import ASSETS_DIRECTORY, INDEX_FILE, METADATA_FILE
from metadata import Contributor, Metadata
from pathlib import Path


class File:
    def __init__(self):
        self._folder = None
        self.is_modified = False
        self.path = None
        self._clean()

    def _prepare_working_folder(self):
        folder = tempfile.mkdtemp()
        metadata_path = Path(folder) / METADATA_FILE

        index.initialize(Path(folder) / INDEX_FILE)

        if not os.path.exists(metadata_path):
            with open(metadata_path, "w") as metadata_file:
                json.dump({}, metadata_file)

        return folder

    def _clean(self):
        if self._folder and os.path.exists(self._folder):
            shutil.rmtree(self._folder)
        self._folder = self._prepare_working_folder()
        self.is_modified = False
        self.path = None

    def _database_path(self):
        if not self._folder:
            raise RuntimeError("No file is open. Run 'open' first.")
        return Path(self._folder) / INDEX_FILE

    def close(self):
        self._clean()

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
        node_id = index.insert_node(self._database_path(), url)

        if not self.get_node_type_by_name(_type):
            self.create_node_type(_type)

        self.set_node_by_id(node_id, _type_name=_type)

        self.get_node_asset_directory(node_id).mkdir(
            parents=True, exist_ok=True
        )

        return node_id

    def create_node_type(self, name):
        index.create_node_type(self._database_path(), name)

    def insert_edge(self, source_node_id, target_node_id, _type="has_child"):
        if not (
            self.get_node_by_id(source_node_id)
            or self.get_node_by_id(target_node_id)
        ):
            return

        edge_id = index.insert_edge(
            self._database_path(), source_node_id, target_node_id
        )

        if not self.get_edge_type_by_name(_type):
            self.create_edge_type(_type)

        self.set_edge_by_id(edge_id, _type_name=_type)

        return edge_id

    def create_edge_type(self, name):
        if not self.get_edge_type_by_name(name):
            index.create_edge_type(self._database_path(), name)

    def delete_node_by_id(self, id):
        if self.get_node_by_id(id):
            index.delete_node_by_id(self._database_path(), id)

    def delete_node_type_by_name(self, name):
        if self.get_node_type_by_name(name):
            index.delete_node_type_by_name(self._database_path(), name)

    def delete_edge_by_id(self, id):
        if self.get_edge_by_id(id):
            index.delete_edge_by_id(self._database_path(), id)

    def delete_edge_type_by_name(self, name):
        if self.get_edge_type_by_name(name):
            index.delete_edge_type_by_name(self._database_path(), name)

    def get_node_by_id(self, id):
        return index.get_node_by_id(self._database_path(), id)

    def get_all_nodes(self, _type=None):
        return index.get_all_nodes(self._database_path(), _type)

    def match_nodes_by_url(self, url):
        return index.get_nodes_by_url_match(self._database_path(), url)

    def get_node_type_by_name(self, name):
        return index.get_node_type_by_name(self._database_path(), name)

    def get_all_node_types(self):
        return index.get_all_node_types(self._database_path())

    def get_edge_by_id(self, id):
        return index.get_edge_by_id(self._database_path(), id)

    def get_all_edges(self, _type):
        return index.get_all_edges(self._database_path(), _type)

    def get_edges_by_edge_type_name(self, edge_type_name):
        return index.get_edges_by_edge_type_name(
            self._database_path(), edge_type_name
        )

    def get_edges_by_node_id(self, node_id):
        return index.get_edges_by_node_id(self._database_path(), node_id)

    def get_edge_type_by_name(self, name):
        return index.get_edge_type_by_name(self._database_path(), name)

    def get_all_edge_types(self):
        return index.get_all_edge_types(self._database_path())

    def get_node_asset_directory(self, id):
        digest = hashlib.sha256(str(id).encode("utf-8")).hexdigest()
        return (
            self._database_path().parent
            / ASSETS_DIRECTORY
            / digest[0]
            / digest[1]
            / digest
        )

    def open_node_asset_directory(self, id):
        # Should open with default explorer (open, xdg-open, etc.)
        pass

    def upload_node_asset(self, id, asset_path):
        # Uploads a file to the asset folder of this node (id)
        pass

    def set_node_by_id(self, id, url=None, _type_name=None, content=None):
        if self.get_node_by_id(id):
            index.set_node_by_id(
                self._database_path(), id, url, _type_name, content
            )

    def update_node_type(
        self, current_name, name=None, scheme=None, scheme_font=None
    ):
        if self.get_node_type_by_name(current_name):
            index.update_node_type_by_name(
                self._database_path(),
                current_name,
                name,
                scheme,
                scheme_font,
            )

    def set_edge_by_id(
        self, id, source_node_id=None, _type_name=None, target_node_id=None
    ):
        if self.get_edge_by_id(id):
            index.set_edge_by_id(
                self._database_path(),
                id,
                source_node_id,
                _type_name,
                target_node_id,
            )

    def update_edge_type(self, current_name, name=None):
        if self.get_edge_type_by_name(current_name):
            index.update_edge_type_by_name(
                self._database_path(), current_name, name
            )

    def open(self, path=None, force=False):
        if path is None:
            self._clean()
            return

        if not os.path.exists(path):
            raise FileNotFoundError(f"File '{path}' not found.")

        if self.path is not None and not force:
            raise RuntimeError(
                "A .ngpk file is already loaded. Override with open(force=True, ...)."
            )

        folder = tempfile.mkdtemp()

        try:
            with tarfile.open(path, "r:zst") as tar:
                tar.extractall(path=folder)

            index.initialize(Path(folder) / INDEX_FILE)

            metadata_path = Path(folder) / METADATA_FILE
            if not os.path.exists(metadata_path):
                with open(metadata_path, "w") as metadata_file:
                    json.dump({}, metadata_file)

        except Exception:
            shutil.rmtree(folder, ignore_errors=True)
            raise

        if self._folder and os.path.exists(self._folder):
            shutil.rmtree(self._folder)

        self._folder = folder
        self.is_modified = False
        self.path = path
