"""Constants and compiled regular expressions for changelog macro parsing.

Separated from the original monolithic main.py to keep parsing / rendering
modules focused and easier to test or extend.
"""

from __future__ import annotations

import re
from pathlib import Path

# Repository root (macros/ lives directly under the repo root)
ROOT = Path(__file__).resolve().parent.parent

# Accepted filename casings for changelog discovery
CHANGELOG_FILENAMES = ["CHANGELOG.md", "Changelog.md", "changelog.md"]

# Regex patterns
SEMVER_RE = re.compile(r"^## \[?([0-9]+\.[0-9]+\.[0-9]+)\]?.*?\((\d{4}-\d{2}-\d{2})\)")
CATEGORY_RE = re.compile(
    r"^###\s+(Added|Changed|Fixed|Removed|Security|Deprecated|Breaking|Bug Fixes|Features)\s*$",
    re.IGNORECASE,
)
# General markdown link pattern
MARKDOWN_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^\)]+)\)")
# Specifically commit markdown links; we pre-capture the short/long SHAs
COMMIT_MARKDOWN_LINK_RE = re.compile(
    r"\[([0-9a-f]{7,40})\]\((https://github\.com/[^/]+/[^/]+/commit/([0-9a-f]{7,40}))\)"
)

__all__ = [
    "ROOT",
    "CHANGELOG_FILENAMES",
    "SEMVER_RE",
    "CATEGORY_RE",
    "MARKDOWN_LINK_RE",
    "COMMIT_MARKDOWN_LINK_RE",
]
