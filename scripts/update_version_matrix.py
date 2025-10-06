#!/usr/bin/env python3
"""Regenerate docs/version-matrix.md from package pyproject.toml files.

Usage:
  python scripts/update_version_matrix.py            # rewrite file
  python scripts/update_version_matrix.py --check    # exit 1 if file differs
"""
from __future__ import annotations

import argparse
import pathlib
import sys
import tomllib

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
DOC_FILE = REPO_ROOT / "docs" / "version-matrix.md"
PACKAGES_DIRS = [REPO_ROOT / "packages", REPO_ROOT]  # include root project


def find_pyprojects() -> list[pathlib.Path]:
    pyprojects: list[pathlib.Path] = []
    for base in PACKAGES_DIRS:
        if base.is_dir():
            if (base / "pyproject.toml").exists() and base != REPO_ROOT:
                # package directory that directly contains pyproject
                pass
            # Search immediate children for pyproject.toml
            for child in base.iterdir():
                if child.is_dir():
                    pp = child / "pyproject.toml"
                    if pp.exists():
                        pyprojects.append(pp)
    # Add root pyproject if present
    root_pp = REPO_ROOT / "pyproject.toml"
    if root_pp.exists():
        pyprojects.append(root_pp)
    return pyprojects


def parse_project(path: pathlib.Path) -> tuple[str, str]:
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    name = data.get("project", {}).get("name", path.parent.name)
    version = data.get("project", {}).get("version", "0.0.0")
    return name, version


def generate_table(rows: list[tuple[str, str]]) -> str:
    header = ["# Version Matrix", "", "| Package | Version |", "|---------|---------|"]
    body = [f"| {name} | {version} |" for name, version in sorted(rows)]
    return "\n".join(header + body + [""])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Fail if matrix out of date")
    args = parser.parse_args()

    rows = [parse_project(p) for p in find_pyprojects()]
    content = generate_table(rows)

    if DOC_FILE.exists():
        existing = DOC_FILE.read_text(encoding="utf-8")
    else:
        existing = ""

    if args.check:
        if existing != content:
            print("version-matrix.md is outdated. Run the update script.", file=sys.stderr)
            return 1
        print("version-matrix.md up to date.")
        return 0

    DOC_FILE.write_text(content, encoding="utf-8")
    print(f"Updated {DOC_FILE.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
