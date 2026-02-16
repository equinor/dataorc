"""Tests for LakeFileSystem and AdlsLakeFileSystem."""

from __future__ import annotations

import tempfile
from unittest.mock import MagicMock, patch

import pytest

from dataorc_utils.lake import LakeFileSystem
from dataorc_utils.lake.adls_filesystem import AdlsLakeFileSystem

# ---------------------------------------------------------------------------
# In-memory ADLS mock — behaves like a tiny object store
# ---------------------------------------------------------------------------


class _InMemoryFileClient:
    """Simulates a DataLake file client backed by a shared dict."""

    def __init__(self, store: dict[str, bytes], path: str):
        self._store = store
        self._path = path

    def upload_data(self, data: bytes, *, overwrite: bool = False) -> None:
        self._store[self._path] = data

    def download_file(self):
        if self._path not in self._store:
            raise FileNotFoundError(self._path)
        blob = self._store[self._path]

        dl = MagicMock()
        dl.readall.return_value = blob
        return dl

    def get_file_properties(self):
        if self._path not in self._store:
            raise FileNotFoundError(self._path)
        return {}

    def delete_file(self):
        if self._path not in self._store:
            raise FileNotFoundError(self._path)
        del self._store[self._path]


class _InMemoryFsClient:
    """Simulates a DataLake file-system client backed by a shared dict."""

    def __init__(self):
        self._store: dict[str, bytes] = {}

    def get_file_client(self, path: str) -> _InMemoryFileClient:
        return _InMemoryFileClient(self._store, path)


# ---------------------------------------------------------------------------
# Fixtures — each yields a ready-to-use filesystem instance
# ---------------------------------------------------------------------------


@pytest.fixture
def lake_fs():
    """LakeFileSystem backed by a real temp directory."""
    with tempfile.TemporaryDirectory() as d:
        yield LakeFileSystem(base_path=d)


@pytest.fixture
def adls_fs():
    """AdlsLakeFileSystem backed by an in-memory mock store."""
    with (
        patch(
            "dataorc_utils.lake.adls_filesystem.DataLakeServiceClient"
        ) as mock_service_cls,
        patch("dataorc_utils.lake.adls_filesystem.DefaultAzureCredential"),
    ):
        mock_service = mock_service_cls.return_value
        mock_service.get_file_system_client.return_value = _InMemoryFsClient()

        yield AdlsLakeFileSystem(
            account_url="https://fake.dfs.core.windows.net",
            container="test",
        )


@pytest.fixture(params=["lake", "adls"])
def fs(request, lake_fs, adls_fs):
    """Parametrized fixture that yields both filesystem implementations."""
    if request.param == "lake":
        return lake_fs
    return adls_fs


# ---------------------------------------------------------------------------
# Shared tests — run once per implementation
# ---------------------------------------------------------------------------


class TestFileSystem:
    def test_write_and_read_text(self, fs):
        assert not fs.exists("test.txt")
        fs.write_text("test.txt", "hello world")
        assert fs.exists("test.txt")
        assert fs.read_text("test.txt") == "hello world"

    def test_read_nonexistent_returns_none(self, fs):
        result = fs.read_text("does_not_exist.txt")

        assert result is None

    def test_write_and_read_json(self, fs):
        data = {"key": "value", "number": 42}

        fs.write_json("data.json", data)

        assert fs.read_json("data.json") == data

    def test_delete(self, fs):
        fs.write_text("to_delete.txt", "content")

        assert fs.exists("to_delete.txt")
        assert fs.delete("to_delete.txt")
        assert not fs.exists("to_delete.txt")
        assert not fs.delete("to_delete.txt")  # Already deleted


# ---------------------------------------------------------------------------
# LakeFileSystem-specific tests
# ---------------------------------------------------------------------------


class TestLakeFileSystemSpecific:
    def test_write_creates_parent_directories(self, lake_fs):
        lake_fs.write_text("nested/subdir/file.txt", "content")

        assert lake_fs.exists("nested/subdir/file.txt")
        assert lake_fs.read_text("nested/subdir/file.txt") == "content"
