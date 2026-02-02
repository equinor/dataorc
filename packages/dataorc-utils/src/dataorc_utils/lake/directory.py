"""Directory operations.

Provides functions for exists, delete, and mkdir.
All paths should already be resolved before calling these functions.
"""

from __future__ import annotations

import logging

import fsspec

logger = logging.getLogger(__name__)


def exists(fs: fsspec.AbstractFileSystem, path: str) -> bool:
    """Check if a file or directory exists.

    Args:
        fs: fsspec filesystem instance
        path: Resolved path to check

    Returns:
        True if exists, False otherwise
    """
    try:
        return fs.exists(path)
    except Exception as exc:
        logger.warning("exists() failed for %s: %s", path, exc)
        return False


def delete(fs: fsspec.AbstractFileSystem, path: str) -> bool:
    """Delete a file.

    Args:
        fs: fsspec filesystem instance
        path: Resolved path to delete

    Returns:
        True if deleted, False if didn't exist
    """
    if not fs.exists(path):
        return False

    fs.rm(path)
    logger.debug("Deleted: %s", path)
    return True


def makedirs(fs: fsspec.AbstractFileSystem, path: str, exist_ok: bool = True) -> None:
    """Create directory and all parent directories.

    Args:
        fs: fsspec filesystem instance
        path: Resolved directory path
        exist_ok: If True, don't error if directory exists
    """
    fs.makedirs(path, exist_ok=exist_ok)
