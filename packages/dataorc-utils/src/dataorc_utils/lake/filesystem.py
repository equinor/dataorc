"""LakeFileSystem - unified interface for data lake operations.

Path-agnostic file operations for Databricks pipelines.
Callers are responsible for providing correct absolute paths.
On Databricks with FUSE mount, paths should include /dbfs/ prefix.
"""

from __future__ import annotations

import json
import logging
from pathlib import PurePosixPath
from typing import Any

import fsspec

logger = logging.getLogger(__name__)

# Type alias for JSON-serializable data
JSONValue = dict[str, Any] | list[Any] | str | int | float | bool | None


class LakeFileSystem:
    """Unified interface for data lake file operations.

    Example:
        fs = LakeFileSystem(base_path="/dbfs/mnt/datalake/bronze")
        fs.write_json("data.json", {"key": "value"})
        data = fs.read_json("data.json")
    """

    def __init__(self, base_path: str | None = None):
        """Initialize with optional base path prepended to all operations."""
        self._base_path = PurePosixPath(base_path) if base_path else None
        self._fs: fsspec.AbstractFileSystem | None = None

    @property
    def fs(self) -> fsspec.AbstractFileSystem:
        """Lazy initialization of fsspec filesystem."""
        if self._fs is None:
            self._fs = fsspec.filesystem("file")
        return self._fs

    def _resolve(self, path: str) -> str:
        """Join path with base_path if set."""
        if self._base_path:
            return str(self._base_path / path.lstrip("/"))
        return path

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

    # --- JSON Operations ---

    def read_json(self, path: str) -> JSONValue:
        """Read a JSON file. Returns None if file doesn't exist or parse fails."""
        content = self.read_text(path)
        if content is None:
            return None
        try:
            return json.loads(content)
        except json.JSONDecodeError as exc:
            logger.warning("Failed to parse JSON from %s: %s", path, exc)
            return None

    def write_json(self, path: str, data: JSONValue, indent: int = 2) -> None:
        """Write a JSON file."""
        self.write_text(path, json.dumps(data, indent=indent, default=str))
