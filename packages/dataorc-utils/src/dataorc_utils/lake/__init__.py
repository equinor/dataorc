"""Data lake filesystem utilities for Databricks pipelines."""

from .filesystem import LakeFileSystem

__all__ = ["AdlsLakeFileSystem", "LakeFileSystem"]


def __getattr__(name: str):  # noqa: N807
    """Lazy import for AdlsLakeFileSystem to avoid hard azure dependency."""
    if name == "AdlsLakeFileSystem":
        from .adls_filesystem import AdlsLakeFileSystem

        return AdlsLakeFileSystem
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
