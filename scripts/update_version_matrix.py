#!/usr/bin/env python3
"""Regenerate ``docs/version-matrix.md`` from project ``pyproject.toml`` files.

Usage
-----
Rewrite the file:
    python scripts/update_version_matrix.py

Check (CI mode) and fail if out of date:
    python scripts/update_version_matrix.py --check
"""

from __future__ import annotations

import argparse
import difflib
import pathlib
import sys
import tomllib

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
DOC_FILE = REPO_ROOT / "docs" / "version-matrix.md"


def find_pyprojects() -> list[pathlib.Path]:
    """Return all pyproject.toml paths (root plus first-level packages).

    Currently only the root project exists, but this keeps future multi-package
    expansion trivial without deep recursion.
    """

    projects: list[pathlib.Path] = []
    packages_dir = REPO_ROOT / "packages"
    if packages_dir.is_dir():
        for child in packages_dir.iterdir():
            if not child.is_dir():
                continue
            candidate = child / "pyproject.toml"
            if candidate.exists():
                projects.append(candidate)

    root_pp = REPO_ROOT / "pyproject.toml"
    if root_pp.exists():
        projects.append(root_pp)
    # Deduplicate & stable order
    return sorted({p.resolve() for p in projects})


def parse_project(path: pathlib.Path) -> tuple[str, str]:
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    project = data.get("project", {})
    name = project.get("name", path.parent.name)
    version = project.get("version", "0.0.0")
    return name, version


def generate_table(rows: list[tuple[str, str]]) -> str:
    header = ["# Version Matrix", "", "| Package | Version |", "|---------|---------|"]
    body = [f"| {name} | {version} |" for name, version in sorted(rows)]
    return "\n".join((*header, *body, ""))


def diff(existing: str, new: str) -> str:
    return "\n".join(
        difflib.unified_diff(
            existing.splitlines(),
            new.splitlines(),
            fromfile="current",
            tofile="expected",
            lineterm="",
            n=3,
        )
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check", action="store_true", help="Fail if matrix out of date"
    )
    args = parser.parse_args()

    rows = [parse_project(p) for p in find_pyprojects()]
    if not rows:
        print("No pyproject.toml files found; nothing to do.", file=sys.stderr)
        return 0 if args.check else 1

    content = generate_table(rows)
    existing = DOC_FILE.read_text(encoding="utf-8") if DOC_FILE.exists() else ""

    if args.check:
        if existing != content:
            print(
                "version-matrix.md is outdated. Run the update script.", file=sys.stderr
            )
            print(diff(existing, content), file=sys.stderr)
            return 1
        print("version-matrix.md up to date.")
        return 0

    DOC_FILE.write_text(content, encoding="utf-8")
    print(f"Updated {DOC_FILE.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
