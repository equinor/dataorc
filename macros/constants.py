"""Constants and compiled regular expressions for changelog macro parsing."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CHANGELOG_FILENAME = "CHANGELOG.md"

SEMVER_RE = re.compile(r"^## \[?([0-9]+\.[0-9]+\.[0-9]+)\]?.*?\((\d{4}-\d{2}-\d{2})\)")
CATEGORY_RE = re.compile(
    r"^###\s+(Added|Changed|Fixed|Removed|Security|Deprecated|Breaking|Bug Fixes|Features)\s*$",
    re.IGNORECASE,
)
MARKDOWN_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^\)]+)\)")
COMMIT_MARKDOWN_LINK_RE = re.compile(
    r"\[([0-9a-f]{7,40})\]\((https://github\.com/[^/]+/[^/]+/commit/([0-9a-f]{7,40}))\)"
)

__all__ = [
    "ROOT",
    "CHANGELOG_FILENAME",
    "SEMVER_RE",
    "CATEGORY_RE",
    "MARKDOWN_LINK_RE",
    "COMMIT_MARKDOWN_LINK_RE",
]
