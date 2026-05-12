"""Argument parsing utilities for Databricks wheel tasks.

Provides a simple helper to parse CLI arguments passed to wheel tasks
in Databricks jobs.
"""

from __future__ import annotations

from argparse import ArgumentParser, Namespace
from typing import Dict, Iterable, Union


def parse_args(
    description: str,
    arguments: Union[Iterable[str], Dict[str, bool]],
) -> Namespace:
    """Parse command-line arguments for a Databricks wheel task.

    Accepts either an iterable of argument names (all required), or a dict
    mapping argument names to a boolean `required` flag. Each argument is
    exposed as a `--name` CLI option and parsed as `str`.

    Args:
        description: Description shown in help output for the argument parser.
        arguments: Either a list/iterable of argument names (e.g., ["db"]),
            which will be treated as required, or a dict mapping names to a
            boolean indicating whether the argument is required
            (e.g., {"db": True, "schema": False}).

    Returns:
        Namespace with parsed arguments accessible as attributes.

    Examples:
        # All required args
        args = parse_args("ETL Job", ["database", "schema"])  # both required

        # Per-arg required flags
        args = parse_args("ETL Job", {"database": True, "schema": False})
    """
    parser = ArgumentParser(description=description)

    # Normalize arguments into a mapping of name -> required flag
    if isinstance(arguments, dict):
        arg_map = arguments
    else:
        arg_map = {name: True for name in arguments}

    for name, required in arg_map.items():
        parser.add_argument(f"--{name}", type=str, required=bool(required))

    return parser.parse_args()
