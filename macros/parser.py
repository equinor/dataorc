"""Parsing logic for CHANGELOG files into structured section dictionaries."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from .constants import ROOT, SEMVER_RE
from .renderer import render_lines_to_html


def parse_changelog(changelog_path: Path, package: str) -> List[Dict[str, Any]]:
    sections: List[Dict[str, Any]] = []
    current: Dict[str, Any] | None = None
    for line in changelog_path.read_text(encoding="utf-8").splitlines():
        semver_match = SEMVER_RE.match(line)
        if semver_match:
            if current:
                sections.append(current)
            version, date_str = semver_match.groups()
            current = {
                "version": version,
                "date": datetime.strptime(date_str, "%Y-%m-%d").date(),
                "lines": [],
                "package": package,
                "path": changelog_path.relative_to(ROOT).as_posix(),
            }
        elif current is not None:
            current["lines"].append(line)
    if current:
        sections.append(current)
    for section in sections:
        section["html"] = render_lines_to_html(section["lines"])
    return sections


__all__ = ["parse_changelog"]
