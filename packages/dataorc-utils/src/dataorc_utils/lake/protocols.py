"""Shared contracts for lake filesystem implementations."""

from __future__ import annotations

import json
import logging
from typing import Any, Protocol, runtime_checkable

logger = logging.getLogger(__name__)

JSONValue = dict[str, Any] | list[Any] | str | int | float | bool | None


@runtime_checkable
class LakeFileSystemProtocol(Protocol):
    """Structural contract *and* shared logic for lake filesystem backends.

    Use as a type hint when accepting any filesystem backend::

        def ingest(fs: LakeFileSystemProtocol, path: str) -> dict: ...

    Subclasses that explicitly inherit from this protocol get the
    concrete ``read_json``, ``write_json``, and ``_resolve``
    implementations for free — only the four primitives
    (``read_text``, ``write_text``, ``exists``, ``delete``)
    need to be provided by each backend.
    """

    _base_path: str

    # -- primitives (each backend implements these) --

    def read_text(self, path: str) -> str | None:
        """Read a UTF-8 text file, returning ``None`` when unavailable."""
        ...

    def write_text(self, path: str, content: str) -> None:
        """Write or overwrite a UTF-8 text file."""
        ...

    def exists(self, path: str) -> bool:
        """Check whether ``path`` exists."""
        ...

    def delete(self, path: str) -> bool:
        """Delete ``path`` and report if deletion happened."""
        ...

    # -- shared path resolution --

    def _resolve(self, path: str) -> str:
        """Prepend ``_base_path`` to *path*, stripping leading slashes."""
        path = path.lstrip("/")
        if self._base_path:
            return f"{self._base_path}/{path}"
        return path

    # -- shared JSON convenience built on the primitives above --

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
