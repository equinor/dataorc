"""Backend detection and fsspec initialization.

Detects whether code is running on Databricks or locally,
and initializes the appropriate fsspec filesystem.
"""

from __future__ import annotations

import logging
import os
from functools import lru_cache

import fsspec

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def _is_databricks() -> bool:
    """Check if running on Databricks.

    Cached for performance - environment doesn't change during runtime.
    """
    return os.path.exists("/dbfs")


def create_filesystem() -> fsspec.AbstractFileSystem:
    """Create and return an fsspec filesystem instance.

    On Databricks with /dbfs/ paths, uses local filesystem (FUSE mount).
    This requires paths to already include /dbfs/ prefix when on Databricks.

    Returns:
        A configured fsspec filesystem for the current environment.
    """
    fs = fsspec.filesystem("file")
    logger.debug("Created fsspec local filesystem (databricks=%s)", _is_databricks())
    return fs
