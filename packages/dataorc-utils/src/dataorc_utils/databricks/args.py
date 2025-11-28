"""Argument parsing utilities for Databricks wheel tasks.

Provides a simple helper to parse CLI arguments passed to wheel tasks
in Databricks jobs.
"""

from __future__ import annotations

import argparse


def parse_args(description: str, arguments: list[str]) -> argparse.Namespace:
    """Parse command-line arguments for a Databricks wheel task.

    When running Python wheel tasks in Databricks, job parameters are passed
    as command-line arguments. This helper creates an argument parser with
    the specified arguments and returns the parsed values.

    Args:
        description: Description shown in help output for the argument parser.
        arguments: List of argument names to parse (e.g., ["database", "schema"]).
            Each name becomes a required ``--name`` argument.

    Returns:
        Namespace with parsed arguments accessible as attributes.

    Example:
        >>> # Called with: --database mydb --schema public
        >>> args = parse_args("ETL Job", ["database", "schema"])
        >>> print(args.database, args.schema)
        mydb public
    """
    parser = argparse.ArgumentParser(description=description)

    for name in arguments:
        parser.add_argument(f"--{name}", type=str, required=True)

    return parser.parse_args()
