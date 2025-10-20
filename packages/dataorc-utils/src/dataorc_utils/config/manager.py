"""
Parameter management for pipeline configuration.

This manager reads configuration from environment variables.
Cluster environment variables / wheel packaging.
"""

import os
from enum import Enum
from typing import Dict, Optional

from .enums import CoreParam, Defaults, Environment
from .models import CorePipelineConfig, InfraContext


class PipelineParameterManager:
    """
    General parameter manager for data pipelines.

    This manager is designed to work with repository-specific configurations.
    Most repositories should create their own wrapper that provides the
    repository-specific configuration dictionaries.
    """

    def __init__(
        self,
        environments_config: dict = None,
        repository_defaults: dict = None,
        domain_configs: dict = None,
        product_configs: dict = None,
        custom_params: Dict[Enum, str] = None,
        case_fallback: bool = False,
    ):
        """
        Initialize parameter manager.

        Args:
            environments_config: Dictionary of environment configurations
            repository_defaults: Dictionary of repository-specific defaults
            domain_configs: Dictionary of domain configurations
            product_configs: Dictionary of product configurations
            custom_params: Additional custom parameters specific to pipeline type
        """
        # Wheel-based packaging for configuration delivery.
        self.environments_config = environments_config or {}
        self.repository_defaults = repository_defaults or {}
        self.domain_configs = domain_configs or {}
        self.product_configs = product_configs or {}
        self.custom_params = custom_params or {}
        self._config_cache: Optional[Dict[str, str]] = None
        self.case_fallback = case_fallback
        self._local_environment = Environment.DEV  # Default for local development

    def _get_default_value(self, param: CoreParam) -> str:
        """Get default value for a core parameter."""
        defaults_map = {
            CoreParam.BRONZE_VERSION: Defaults.VERSION,
            CoreParam.SILVER_VERSION: Defaults.VERSION,
            CoreParam.GOLD_VERSION: Defaults.VERSION,
            CoreParam.BRONZE_PROCESSING_METHOD: Defaults.BRONZE_PROCESSING_METHOD,
            CoreParam.SILVER_PROCESSING_METHOD: Defaults.SILVER_PROCESSING_METHOD,
            CoreParam.GOLD_PROCESSING_METHOD: Defaults.GOLD_PROCESSING_METHOD,
        }
        return defaults_map.get(param, "")

    def get_parameter_values(self, param_list: list = None) -> Dict[str, str]:
        """
        Get parameter values from environment variables.

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

        config_dict: Dict[str, str] = {}
        for param in param_list:
            param_name = param.value if hasattr(param, "value") else str(param)

            # Lookup strategy: exact first. If case_fallback enabled, try UPPER then lower.
            env_value = os.getenv(param_name)
            if env_value is None and self.case_fallback:
                if param_name.upper() != param_name:
                    env_value = os.getenv(param_name.upper())
                if env_value is None and param_name.lower() != param_name:
                    env_value = os.getenv(param_name.lower())

            if env_value is not None:
                config_dict[param_name] = env_value
            else:
                config_dict[param_name] = self._get_default_value(param)

        self._config_cache = config_dict
        return config_dict

    def prepare_infrastructure(self) -> InfraContext:
        """Read and return infrastructure context (no dataset identifiers)."""
        values = self.get_parameter_values()
        return InfraContext(
            datalake_name=values.get(CoreParam.DATALAKE_NAME, ""),
            datalake_container_name=values.get(CoreParam.DATALAKE_CONTAINER_NAME, ""),
            env=Environment(values.get(CoreParam.ENV, Environment.DEV.value)),
            az_tenant_id=values.get(CoreParam.AZ_TENANT_ID, ""),
            az_client_id=values.get(CoreParam.AZ_CLIENT_ID, ""),
            az_subscription_id=values.get(CoreParam.AZ_SUBSCRIPTION_ID, ""),
            az_keyvault_scope=values.get(CoreParam.AZ_KEYVAULT_SCOPE, ""),
            az_blob_storage_account=values.get(CoreParam.AZ_BLOB_STORAGE_ACCOUNT, ""),
            az_datalake_storage_account=values.get(
                CoreParam.AZ_DATALAKE_STORAGE_ACCOUNT, ""
            ),
        )

    def build_core_config(
        self,
        infra: InfraContext,
        domain: str = "",
        product: str = "",
        table_name: str = "",
        bronze_version: str | None = None,
        silver_version: str | None = None,
        gold_version: str | None = None,
        bronze_processing_method: str | None = None,
        silver_processing_method: str | None = None,
        gold_processing_method: str | None = None,
    ) -> CorePipelineConfig:
        """Compose a CorePipelineConfig from infra plus pipeline-specific overrides."""
        # Resolve defaults if None supplied
        bv = bronze_version or self._get_default_value(CoreParam.BRONZE_VERSION)
        sv = silver_version or self._get_default_value(CoreParam.SILVER_VERSION)
        gv = gold_version or self._get_default_value(CoreParam.GOLD_VERSION)

        bpm = bronze_processing_method or self._get_default_value(
            CoreParam.BRONZE_PROCESSING_METHOD
        )
        spm = silver_processing_method or self._get_default_value(
            CoreParam.SILVER_PROCESSING_METHOD
        )
        gpm = gold_processing_method or self._get_default_value(
            CoreParam.GOLD_PROCESSING_METHOD
        )

        config = CorePipelineConfig(
            datalake_name=infra.datalake_name,
            datalake_container_name=infra.datalake_container_name,
            env=infra.env,
            domain=domain,
            product=product,
            table_name=table_name,
            bronze_version=bv,
            silver_version=sv,
            gold_version=gv,
            bronze_processing_method=bpm,
            silver_processing_method=spm,
            gold_processing_method=gpm,
            az_tenant_id=infra.az_tenant_id,
            az_client_id=infra.az_client_id,
            az_subscription_id=infra.az_subscription_id,
            az_keyvault_scope=infra.az_keyvault_scope,
            az_blob_storage_account=infra.az_blob_storage_account,
            az_datalake_storage_account=infra.az_datalake_storage_account,
        )
        config.validate_rules()
        return config
