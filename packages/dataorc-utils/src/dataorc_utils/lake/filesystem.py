"""LakeFileSystem - unified interface for data lake operations.

Path-agnostic file operations for Databricks pipelines.
Callers are responsible for providing correct absolute paths.
On Databricks with FUSE mount, paths should include /dbfs/ prefix.
"""

from __future__ import annotations

import fsspec

from .protocols import BaseLakeFileSystem


class LakeFileSystem(BaseLakeFileSystem):
    """Unified interface for data lake file operations.

    Example:
        fs = LakeFileSystem(base_path="/dbfs/mnt/datalake/bronze")
        fs.write_json("data.json", {"key": "value"})
        data = fs.read_json("data.json")
    """

    def __init__(self, base_path: str | None = None):
        """Initialize with optional base path prepended to all operations."""
        self._base_path = base_path.rstrip("/") if base_path else ""
        self._fs: fsspec.AbstractFileSystem | None = None

    @property
    def fs(self) -> fsspec.AbstractFileSystem:
        """Lazy initialization of fsspec filesystem."""
        if self._fs is None:
            self._fs = fsspec.filesystem("file")
        return self._fs

    # --- Directory Operations ---

    def exists(self, path: str) -> bool:
        """Check if a file or directory exists."""
        return self.fs.exists(self._resolve(path))

    def delete(self, path: str) -> bool:
        """Delete a file. Returns True if deleted, False if didn't exist."""
        resolved = self._resolve(path)
        if not self.fs.exists(resolved):
            return False
        self.fs.rm(resolved)
        return True

    # --- Text Operations ---

    def read_text(self, path: str) -> str | None:
        """Read a text file. Returns None if file doesn't exist."""
        resolved = self._resolve(path)
        if not self.fs.exists(resolved):
            return None
        with self.fs.open(resolved, "r", encoding="utf-8") as f:
            return f.read()

    def write_text(self, path: str, content: str) -> None:
        """Write a text file, creating parent directories if needed."""
        resolved = self._resolve(path)
        parent = self.fs._parent(resolved)
        if parent:
            self.fs.makedirs(parent, exist_ok=True)
        with self.fs.open(resolved, "w", encoding="utf-8") as f:
            f.write(content)
