"""Discovery of changelog files across the repository packages."""

from pathlib import Path
from typing import Any, Dict, List

from .constants import CHANGELOG_FILENAME, ROOT
from .parser import parse_changelog


def discover_changelogs() -> List[Dict[str, Any]]:
    changelog_files: List[Path] = []
    root_changelog = ROOT / CHANGELOG_FILENAME
    if root_changelog.exists():
        changelog_files.append(root_changelog)
    packages_dir = ROOT / "packages"
    if packages_dir.exists():
        for pkg in packages_dir.iterdir():
            if not pkg.is_dir():
                continue
            candidate = pkg / CHANGELOG_FILENAME
            if candidate.exists():
                changelog_files.append(candidate)
    entries: List[Dict[str, Any]] = []
    for file in changelog_files:
        package = "dataorc" if file.parent == ROOT else file.parent.name
        entries.extend(parse_changelog(file, package))
    entries.sort(key=lambda e: (e["date"], e["version"]), reverse=True)
    return entries


__all__ = ["discover_changelogs"]
