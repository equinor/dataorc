"""Tests for dataorc_utils.databricks.args module."""

from __future__ import annotations

import sys

import pytest

from dataorc_utils.databricks.args import parse_args


def test_parse_args_returns_namespace_with_values(monkeypatch: pytest.MonkeyPatch):
    """parse_args should return a Namespace with the expected attribute values."""
    monkeypatch.setattr(
        sys, "argv", ["script.py", "--database", "mydb", "--schema", "public"]
    )

    args = parse_args("Test", ["database", "schema"])

    assert args.database == "mydb"
    assert args.schema == "public"


def test_parse_args_empty_arguments_list(monkeypatch: pytest.MonkeyPatch):
    """parse_args with no arguments should return an empty Namespace."""
    monkeypatch.setattr(sys, "argv", ["script.py"])

    args = parse_args("No args job", [])

    # Namespace should have no extra attributes
    assert vars(args) == {}
