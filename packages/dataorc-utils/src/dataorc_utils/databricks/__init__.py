"""Databricks utilities for DataOrc.

Public API re-exports a small, stable surface for mounting ADLS Gen2 in
Databricks.

Usage:
    from dataorc_utils.databricks import ensure_mount
"""

from .mounts import OAuthConfig, ensure_mount

__all__ = ["OAuthConfig", "ensure_mount"]
