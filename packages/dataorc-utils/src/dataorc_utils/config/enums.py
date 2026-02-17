"""
Core parameter definitions and enums.
"""

from enum import Enum


class CoreParam(str, Enum):
    """Core parameters used across all pipelines."""

    # Environment and data lake
    DATALAKE_NAME = "datalake_name"
    DATALAKE_CONTAINER_NAME = "datalake_container_name"
    ENV = "env"

    # Data Lake Structure Parameters
    # Following pattern: [containername/]{layer}/{domain}/{product}/{version}/output/{processing_method}
    # When datalake_container_name is omitted, the layer itself acts as the container
    DOMAIN = "domain"  # Business domain  -> Catalog name
    PRODUCT = "product"  # Product/project  -> Database name
    TABLE_NAME = "table_name"  # Table name within the product/database

    # layers
    BRONZE_VERSION = "bronze_version"  # Version for bronze layer
    SILVER_VERSION = "silver_version"  # Version for silver layer
    GOLD_VERSION = "gold_version"  # Version for gold layer

    # Processing Methods (layer-specific, user-configurable)
    BRONZE_PROCESSING_METHOD = "bronze_processing_method"  # incremental, full, delta
    SILVER_PROCESSING_METHOD = "silver_processing_method"  # incremental, full, delta
    GOLD_PROCESSING_METHOD = "gold_processing_method"  # incremental, full, delta


# Default values - co-located with their semantic meaning
class Defaults:
    """Default values for pipeline configuration."""

    # Version defaults
    VERSION = "v1"

    # Processing method defaults
    BRONZE_PROCESSING_METHOD = "incremental"
    SILVER_PROCESSING_METHOD = "incremental"
    GOLD_PROCESSING_METHOD = "delta"
