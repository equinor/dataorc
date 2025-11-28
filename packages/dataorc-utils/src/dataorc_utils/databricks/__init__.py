"""Databricks utilities for DataOrc.

Public API re-exports a small, stable surface for mounting ADLS Gen2 in
Databricks and parsing wheel-task arguments.

Usage:
    from dataorc_utils.databricks import ensure_mount, parse_args
"""

from .args import parse_args
from .mounts import OAuthConfig, ensure_mount

__all__ = ["OAuthConfig", "ensure_mount", "parse_args"]
