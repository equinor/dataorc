"""MkDocs macros package for DataOrc aggregated changelogs.

This package exposes a single public macro entrypoint ``define_env`` and
splits supporting logic into submodules (``constants``, ``renderer``,
``parser``, ``discover``). We inline the entrypoint here so that MkDocs can
reference the package directly (``macros``) instead of an intermediate
``macros.main`` module.
"""

from .discover import discover_changelogs


def define_env(env):  # MkDocs Macros entrypoint
    entries = discover_changelogs()
    env.variables["changelog_entries"] = entries
    env.variables["changelog_packages"] = sorted({e["package"] for e in entries})


__all__ = ["define_env"]
