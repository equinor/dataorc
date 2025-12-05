"""Dataorc Utils

A collection of utility functions for ETL operations.
"""

__author__ = "Equinor"
__email__ = "toarst@equinor.com"

# Import main functions/classes here to make them available at package level
# Example:
# from .core import some_function
# from .utils import another_function

# Re-export subpackages / common symbols for convenience.
# This allows: `from dataorc_utils import config` or
# `from dataorc_utils.config import CorePipelineConfig`.
from . import azure, config, databricks  # convenient access to subpackages

# __all__ defines what gets imported with "from dataorc_utils import *"
__all__ = [
    "azure",
    "config",
    "databricks",
]
