"""Text and JSON file operations.

Provides read/write functions for text and JSON files.
All paths should already be resolved before calling these functions.
"""

from __future__ import annotations

import json
import logging
from typing import Any

import fsspec

logger = logging.getLogger(__name__)


def read_text(fs: fsspec.AbstractFileSystem, path: str) -> str | None:
    """Read a text file.

    Args:
        fs: fsspec filesystem instance
        path: Resolved path to read

    Returns:
        File content as string, or None if file doesn't exist
    """
    if not fs.exists(path):
        return None

    with fs.open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_text(fs: fsspec.AbstractFileSystem, path: str, content: str) -> None:
    """Write a text file.

    Creates parent directories if needed.

    Args:
        fs: fsspec filesystem instance
        path: Absolute path to write
        content: Text content to write
    """
    parent = _get_parent(path)
    if parent:
        fs.makedirs(parent, exist_ok=True)

    with fs.open(path, "w", encoding="utf-8") as f:
        f.write(content)


def _get_parent(path: str) -> str | None:
    """Get parent directory of a path."""
    parts = path.rstrip("/").rsplit("/", 1)
    return parts[0] if len(parts) > 1 and parts[0] else None


def read_json(fs: fsspec.AbstractFileSystem, path: str) -> dict[str, Any] | None:
    """Read a JSON file.

    Args:
        fs: fsspec filesystem instance
        path: Resolved path to read

    Returns:
        Parsed JSON as dict, or None if file doesn't exist or parse fails
    """
    content = read_text(fs, path)
    if content is None:
        return None

    try:
        return json.loads(content)
    except json.JSONDecodeError as exc:
        logger.warning("Failed to parse JSON from %s: %s", path, exc)
        return None


def write_json(
    fs: fsspec.AbstractFileSystem,
    path: str,
    data: dict[str, Any],
    indent: int = 2,
) -> None:
    """Write a JSON file.

    Args:
        fs: fsspec filesystem instance
        path: Resolved path to write
        data: Dictionary to serialize as JSON
        indent: Indentation level (default 2)
    """
    content = json.dumps(data, indent=indent, default=str)
    write_text(fs, path, content)
