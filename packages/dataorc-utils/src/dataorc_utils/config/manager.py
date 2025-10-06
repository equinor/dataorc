"""
Parameter management and dbutils integration.
"""

import os
from enum import Enum
from typing import Dict, Optional

from .defaults import CORE_LIBRARY_DEFAULTS
from .enums import CoreParam, Environment, LoadType
from .models import CorePipelineConfig


class PipelineParameterManager:
    """
    General parameter manager for data pipelines.

    This manager is designed to work with repository-specific configurations.
    Most repositories should create their own wrapper that provides the
    repository-specific configuration dictionaries.
    """

    def __init__(
        self,
        dbutils=None,
        environments_config: dict = None,
        repository_defaults: dict = None,
        domain_configs: dict = None,
        product_configs: dict = None,
        custom_params: Dict[Enum, str] = None,
    ):
        """
        Initialize parameter manager.

        Args:
            dbutils: Databricks utilities object (optional for local development)
            environments_config: Dictionary of environment configurations
            repository_defaults: Dictionary of repository-specific defaults
            domain_configs: Dictionary of domain configurations
            product_configs: Dictionary of product configurations
            custom_params: Additional custom parameters specific to pipeline type
        """
        self.dbutils = dbutils
        self.environments_config = environments_config or {}
        self.repository_defaults = repository_defaults or {}
        self.domain_configs = domain_configs or {}
        self.product_configs = product_configs or {}
        self.custom_params = custom_params or {}
        self._config_cache: Optional[Dict[str, str]] = None
        self._local_environment = Environment.DEV  # Default for local development

    def get_parameter_values(self, param_list: list = None) -> Dict[str, str]:
        """
        Get parameter values from dbutils widgets or environment variables.

        Args:
            param_list: List of parameter enums to retrieve. If None, gets all core params.

        Returns:
            Dictionary of parameter names to values
        """
        if self._config_cache:
            return self._config_cache

        # Default to core parameters if none specified
        if param_list is None:
            param_list = list(CoreParam)

        if self.dbutils:
            # Get values from dbutils widgets
            config_dict = {}
            for param in param_list:
                param_name = param.value if hasattr(param, "value") else str(param)
                config_dict[param_name] = self.dbutils.widgets.get(param_name)
        else:
            # Fallback to environment variables for local development
            config_dict = {}
            for param in param_list:
                param_name = param.value if hasattr(param, "value") else str(param)
                env_var_name = param_name.upper()
                # Use environment variable if available, otherwise use defaults
                env_value = os.getenv(env_var_name)
                if env_value is not None:
                    config_dict[param_name] = env_value
                else:
                    # Use defaults for local development
                    config_dict[param_name] = CORE_LIBRARY_DEFAULTS.get(param, "")

        self._config_cache = config_dict
        return config_dict

    def get_core_config(self) -> CorePipelineConfig:
        """Get core pipeline configuration with validation."""
        values = self.get_parameter_values()
        # Build CorePipelineConfig once, validate rules, and return
        config = CorePipelineConfig(
            datalake_name=values[CoreParam.DATALAKE_NAME],
            datalake_container_name=values[CoreParam.DATALAKE_CONTAINER_NAME],
            env=Environment(values[CoreParam.ENV]),
            load_type=LoadType(values[CoreParam.LOAD_TYPE]),
            # Data Lake Structure Parameters
            domain=values.get(CoreParam.DOMAIN, ""),
            table_name=values.get(
                CoreParam.TABLE_NAME, CORE_LIBRARY_DEFAULTS[CoreParam.TABLE_NAME]
            ),
            product=values.get(CoreParam.PRODUCT, ""),
            bronze_version=values.get(
                CoreParam.BRONZE_VERSION,
                CORE_LIBRARY_DEFAULTS[CoreParam.BRONZE_VERSION],
            ),
            silver_version=values.get(
                CoreParam.SILVER_VERSION,
                CORE_LIBRARY_DEFAULTS[CoreParam.SILVER_VERSION],
            ),
            gold_version=values.get(
                CoreParam.GOLD_VERSION, CORE_LIBRARY_DEFAULTS[CoreParam.GOLD_VERSION]
            ),
            # Processing Methods Parameters
            bronze_processing_method=values.get(
                CoreParam.BRONZE_PROCESSING_METHOD,
                CORE_LIBRARY_DEFAULTS[CoreParam.BRONZE_PROCESSING_METHOD],
            ),
            silver_processing_method=values.get(
                CoreParam.SILVER_PROCESSING_METHOD,
                CORE_LIBRARY_DEFAULTS[CoreParam.SILVER_PROCESSING_METHOD],
            ),
            gold_processing_method=values.get(
                CoreParam.GOLD_PROCESSING_METHOD,
                CORE_LIBRARY_DEFAULTS[CoreParam.GOLD_PROCESSING_METHOD],
            ),
            # Azure infrastructure
            az_tenant_id=values.get(CoreParam.AZ_TENANT_ID, ""),
            az_subscription_id=values.get(CoreParam.AZ_SUBSCRIPTION_ID, ""),
            az_keyvault_scope=values.get(CoreParam.AZ_KEYVAULT_SCOPE, ""),
            az_blob_storage_account=values.get(CoreParam.AZ_BLOB_STORAGE_ACCOUNT, ""),
            az_datalake_storage_account=values.get(
                CoreParam.AZ_DATALAKE_STORAGE_ACCOUNT, ""
            ),
            # API Management
            apim_base_url=values.get(CoreParam.APIM_BASE_URL, ""),
        )

        # Validate rules (raises ValueError on failure)
        config.validate_rules()

        return config
