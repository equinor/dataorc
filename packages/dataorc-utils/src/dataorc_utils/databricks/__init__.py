"""Databricks helpers: mounts and argument parsing.

Provide a compact, typed public surface: `ensure_mount`, `OAuthConfig`, `parse_args`.
"""

from .args import parse_args
from .mounts import OAuthConfig, ensure_mount

# Public API
__all__ = ["OAuthConfig", "ensure_mount", "parse_args"]
