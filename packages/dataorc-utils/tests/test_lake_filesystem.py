"""Tests for LakeFileSystem."""

import tempfile

import pytest

from dataorc_utils.lake import LakeFileSystem


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as d:
        yield d


class TestLakeFileSystem:
    def test_write_and_read_text(self, temp_dir: str):
        fs = LakeFileSystem(base_path=temp_dir)

        assert not fs.exists("test.txt")
        fs.write_text("test.txt", "hello world")
        assert fs.exists("test.txt")
        assert fs.read_text("test.txt") == "hello world"

    def test_read_nonexistent_returns_none(self, temp_dir: str):
        fs = LakeFileSystem(base_path=temp_dir)

        result = fs.read_text("does_not_exist.txt")

        assert result is None

    def test_write_creates_parent_directories(self, temp_dir: str):
        fs = LakeFileSystem(base_path=temp_dir)

        fs.write_text("nested/subdir/file.txt", "content")

        assert fs.exists("nested/subdir/file.txt")
        assert fs.read_text("nested/subdir/file.txt") == "content"

    def test_write_and_read_json(self, temp_dir: str):
        fs = LakeFileSystem(base_path=temp_dir)
        data = {"key": "value", "number": 42}

        fs.write_json("data.json", data)

        assert fs.read_json("data.json") == data

    def test_delete(self, temp_dir: str):
        fs = LakeFileSystem(base_path=temp_dir)
        fs.write_text("to_delete.txt", "content")

        assert fs.exists("to_delete.txt")
        assert fs.delete("to_delete.txt")
        assert not fs.exists("to_delete.txt")
        assert not fs.delete("to_delete.txt")  # Already deleted
