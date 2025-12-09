"""Parameter management for pipeline configuration.

This manager reads configuration from environment variables.
Cluster environment variables / wheel packaging.
"""

from __future__ import annotations

import os
from typing import Any, Mapping, Optional

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
        environments_config: Optional[Mapping[str, Any]] = None,
        domain_configs: Optional[Mapping[str, Any]] = None,
        product_configs: Optional[Mapping[str, Any]] = None,
        case_fallback: bool = False,
    ) -> None:
        """
        Initialize parameter manager.

        Args:
            environments_config: Dictionary of environment configurations
            domain_configs: Dictionary of domain configurations
            product_configs: Dictionary of product configurations
        """
        # Wheel-based packaging for configuration delivery.
        self.environments_config: Mapping[str, Any] = environments_config or {}
        self.domain_configs: Mapping[str, Any] = domain_configs or {}
        self.product_configs: Mapping[str, Any] = product_configs or {}
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

    def get_env_variables(
        self, var_names: list[str], required: bool = False
    ) -> dict[str, str]:
        """
        Retrieve environment variables by name.

        Args:
            var_names: List of environment variable names to retrieve
            required: If True, raises ValueError when a variable is missing

        Returns:
            Dictionary mapping variable names to their values (empty string for missing vars)

        Raises:
            ValueError: If required=True and any variable is not set
        """
        result = {}
        missing = []

        for var_name in var_names:
            # Lookup strategy: exact first. If case_fallback enabled, try UPPER then lower.
            env_value = os.getenv(var_name)
            if env_value is None and self.case_fallback:
                if var_name.upper() != var_name:
                    env_value = os.getenv(var_name.upper())
                if env_value is None and var_name.lower() != var_name:
                    env_value = os.getenv(var_name.lower())

            if env_value is not None:
                result[var_name] = env_value
            else:
                if required:
                    missing.append(var_name)
                else:
                    result[var_name] = ""

        if missing:
            raise ValueError(
                f"Required environment variables not set: {', '.join(missing)}"
            )

        return result

    def prepare_infrastructure(self, env_vars: list[str]) -> InfraContext:
        """Read and return infrastructure context (no dataset identifiers).

        Args:
            env_vars: List of infrastructure environment variable names to capture
                (e.g., ["datalake_name", "datalake_container_name", "az_tenant_id"]).
                These will be stored in InfraContext.variables.

        Returns:
            InfraContext with env and requested infrastructure variables

        Raises:
            ValueError: If the ENV environment variable is not set in environment
        """
        # Get the environment (always required)
        env_value = os.getenv(CoreParam.ENV.value)
        if not env_value:
            raise ValueError(
                f"Required environment variable '{CoreParam.ENV.value}' is not set"
            )

        env = Environment(env_value)

        # Capture infrastructure variables
        infra_vars = self.get_env_variables(env_vars, required=False)

        return InfraContext(
            env=env,
            variables=infra_vars,
        )

    def build_core_config(
        self,
        infra: InfraContext,
        domain: str = "",
        product: str = "",
        table_name: str = "",
        bronze_version: Optional[str] = None,
        silver_version: Optional[str] = None,
        gold_version: Optional[str] = None,
        bronze_processing_method: Optional[str] = None,
        silver_processing_method: Optional[str] = None,
        gold_processing_method: Optional[str] = None,
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
            env_vars=infra.variables,
        )
        config.validate_rules()
        return config
