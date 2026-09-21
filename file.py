import index
import os
import shutil
import tarfile
import tempfile

from .constants import METADATA_FILE
from compression import zstd
from .metadata import Contributor, Metadata


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

    def open(self, force=False, path=None):
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
