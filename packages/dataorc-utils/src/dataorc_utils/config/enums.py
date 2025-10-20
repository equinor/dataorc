"""
Core parameter definitions and enums.
"""

from enum import Enum


class Environment(str, Enum):
    """Pipeline execution environments."""

    DEV = "dev"
    TEST = "test"
    PROD = "prod"


class CoreParam(str, Enum):
    """Core parameters used across all pipelines."""

    # Environment and data lake
    DATALAKE_NAME = "datalake_name"
    DATALAKE_CONTAINER_NAME = "datalake_container_name"
    ENV = "env"

    # Data Lake Structure Parameters
    # Following pattern: containername/{layer}/{domain}/{product}/{version}/output/{processing_method}
    DOMAIN = "domain"  # Business domain  -> Catalog name
    PRODUCT = "product"  # Product/project  -> Database name
    TABLE_NAME = "table_name"  # Table name within the product/database
    BRONZE_VERSION = "bronze_version"  # Version for bronze layer
    SILVER_VERSION = "silver_version"  # Version for silver layer
    GOLD_VERSION = "gold_version"  # Version for gold layer

    # Processing Methods (layer-specific, user-configurable)
    BRONZE_PROCESSING_METHOD = "bronze_processing_method"  # incremental, full, delta
    SILVER_PROCESSING_METHOD = "silver_processing_method"  # incremental, full, delta
    GOLD_PROCESSING_METHOD = "gold_processing_method"  # incremental, full, delta

    # Azure infrastructure (generalizable across pipelines)
    AZ_TENANT_ID = "az_tenant_id"
    AZ_CLIENT_ID = "az_client_id"
    AZ_SUBSCRIPTION_ID = "az_subscription_id"
    AZ_KEYVAULT_SCOPE = "az_keyvault_scope"
    AZ_BLOB_STORAGE_ACCOUNT = "az_blob_storage_account"
    AZ_DATALAKE_STORAGE_ACCOUNT = "az_datalake_storage_account"


# Default values - co-located with their semantic meaning
class Defaults:
    """Default values for pipeline configuration."""

    # Version defaults
    VERSION = "v1"

    # Processing method defaults
    BRONZE_PROCESSING_METHOD = "incremental"
    SILVER_PROCESSING_METHOD = "incremental"
    GOLD_PROCESSING_METHOD = "delta"
