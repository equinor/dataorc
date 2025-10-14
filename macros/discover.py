"""Discovery of changelog files across the repository packages."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from .constants import CHANGELOG_FILENAMES, ROOT
from .parser import parse_changelog


def discover_changelogs() -> List[Dict[str, Any]]:
    changelog_files: List[Path] = []
    for name in CHANGELOG_FILENAMES:
        candidate = ROOT / name
        if candidate.exists():
            changelog_files.append(candidate)
            break
    packages_dir = ROOT / "packages"
    if packages_dir.exists():
        for pkg in packages_dir.iterdir():
            if not pkg.is_dir():
                continue
            for name in CHANGELOG_FILENAMES:
                candidate = pkg / name
                if candidate.exists():
                    changelog_files.append(candidate)
                    break
    entries: List[Dict[str, Any]] = []
    for file in changelog_files:
        package = "dataorc" if file.parent == ROOT else file.parent.name
        entries.extend(parse_changelog(file, package))
    entries.sort(key=lambda e: (e["date"], e["version"]), reverse=True)
    return entries


__all__ = ["discover_changelogs"]
