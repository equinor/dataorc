"""MkDocs macros package for aggregated changelogs (root-level).

Provides the define_env entrypoint consumed by mkdocs-macros-plugin.
"""

from .discover import discover_changelogs


def define_env(env):
    entries = discover_changelogs()
    env.variables["changelog_entries"] = entries
    env.variables["changelog_packages"] = sorted({e["package"] for e in entries})


__all__ = ["define_env"]
