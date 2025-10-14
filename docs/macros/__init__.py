"""MkDocs macros package (moved under docs/) for aggregated changelogs.

Placed inside the docs/ tree so CI can import it by extending PYTHONPATH
with the docs directory. Provides the define_env entrypoint required by
mkdocs-macros-plugin.
"""

from .discover import discover_changelogs


def define_env(env):  # MkDocs Macros entrypoint
    entries = discover_changelogs()
    env.variables["changelog_entries"] = entries
    env.variables["changelog_packages"] = sorted({e["package"] for e in entries})


__all__ = ["define_env"]
