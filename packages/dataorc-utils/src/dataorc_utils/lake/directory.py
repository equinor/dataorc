"""Directory operations.

Provides functions for exists and delete.
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
