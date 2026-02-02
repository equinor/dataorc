"""LakeFileSystem - unified interface for data lake operations.

This is the main public class that orchestrates all lake operations.
It delegates to specialized modules for specific operations.

IMPORTANT: This class does NOT perform path normalization. Callers are
responsible for providing correct absolute paths for their environment.
On Databricks with FUSE mount, paths should include /dbfs/ prefix.
"""

from __future__ import annotations

import logging
from typing import Any

import fsspec

from . import directory, text_io
from .backend import create_filesystem

logger = logging.getLogger(__name__)


class LakeFileSystem:
    """Unified interface for data lake file operations.

    This class is path-agnostic - it accepts paths as-is without normalization.
    Callers are responsible for providing correct paths for their environment.

    Example usage:
        # On Databricks (paths must include /dbfs/ prefix)
        fs = LakeFileSystem()
        fs.write_json("/dbfs/mnt/datalakestore/data.json", {"key": "value"})

        # With base path (paths are joined with base)
        fs = LakeFileSystem(base_path="/dbfs/mnt/datalakestore/bronze")
        fs.write_json("file.json", data)  # Writes to base_path/file.json
    """

    def __init__(self, base_path: str | None = None):
        """Initialize the filesystem.

        Args:
            base_path: Optional base path to prepend to all operations.
                       Useful for scoping to a specific domain/product.
                       Should be an absolute path valid for the runtime.
        """
        self._base_path = base_path.rstrip("/") if base_path else None
        self._fs: fsspec.AbstractFileSystem | None = None

    @property
    def fs(self) -> fsspec.AbstractFileSystem:
        """Lazy initialization of fsspec filesystem."""
        if self._fs is None:
            self._fs = create_filesystem()
        return self._fs

    def _resolve(self, path: str) -> str:
        """Join path with base_path if set. No normalization."""
        if self._base_path:
            return f"{self._base_path}/{path.lstrip('/')}"
        return path

    # --- Directory Operations ---

    def exists(self, path: str) -> bool:
        """Check if a file or directory exists."""
        return directory.exists(self.fs, self._resolve(path))

    def delete(self, path: str) -> bool:
        """Delete a file. Returns True if deleted, False if didn't exist."""
        return directory.delete(self.fs, self._resolve(path))

    def makedirs(self, path: str, exist_ok: bool = True) -> None:
        """Create directory and all parent directories."""
        directory.makedirs(self.fs, self._resolve(path), exist_ok=exist_ok)

    # --- Text Operations ---

    def read_text(self, path: str) -> str | None:
        """Read a text file. Returns None if file doesn't exist."""
        return text_io.read_text(self.fs, self._resolve(path))

    def write_text(self, path: str, content: str) -> None:
        """Write a text file, creating parent directories if needed."""
        text_io.write_text(self.fs, self._resolve(path), content)

    # --- JSON Operations ---

    def read_json(self, path: str) -> dict[str, Any] | None:
        """Read a JSON file. Returns None if file doesn't exist."""
        return text_io.read_json(self.fs, self._resolve(path))

    def write_json(self, path: str, data: dict[str, Any], indent: int = 2) -> None:
        """Write a JSON file."""
        text_io.write_json(self.fs, self._resolve(path), data, indent=indent)
