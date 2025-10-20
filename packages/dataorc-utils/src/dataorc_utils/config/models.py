"""Core configuration data classes."""

from dataclasses import dataclass

from .enums import Defaults, Environment


@dataclass
class InfraContext:
    """Infrastructure-level context captured prior to pipeline specifics.

    Stable across multiple pipeline jobs; excludes dataset identifiers and
    per-layer version/processing configuration.
    """

    datalake_name: str
    datalake_container_name: str
    env: Environment
    az_tenant_id: str = ""
    az_client_id: str = ""
    az_subscription_id: str = ""
    az_keyvault_scope: str = ""
    az_blob_storage_account: str = ""
    az_datalake_storage_account: str = ""


@dataclass(frozen=True, slots=True)
class CorePipelineConfig:
    """Immutable pipeline configuration snapshot.

    Path pattern: container/{layer}/{domain}/{product}/{table_name}/{version}/output/{processing_method}
    Construct via PipelineParameterManager.build_core_config() in production code.
    """

    # Required
    datalake_name: str
    datalake_container_name: str
    env: Environment

    # Structure identifiers
    domain: str = ""
    product: str = ""
    table_name: str = ""

    # Layer versions
    bronze_version: str = Defaults.VERSION
    silver_version: str = Defaults.VERSION
    gold_version: str = Defaults.VERSION

    # Processing methods
    bronze_processing_method: str = Defaults.BRONZE_PROCESSING_METHOD
    silver_processing_method: str = Defaults.SILVER_PROCESSING_METHOD
    gold_processing_method: str = Defaults.GOLD_PROCESSING_METHOD

    # Azure infra
    az_tenant_id: str = ""
    az_client_id: str = ""
    az_subscription_id: str = ""
    az_keyvault_scope: str = ""
    az_blob_storage_account: str = ""
    az_datalake_storage_account: str = ""

    def get_lake_path(
        self,
        layer: str,
        processing_method_override: str = None,
        version_override: str = None,
    ) -> str:
        """
            Generate Data Lake path following the standard structure.

        Structure: containername/{layer}/{domain}/{product}/{table_name}/{version}/output/{processing_method}

            Args:
                layer: bronze, silver, or gold
                processing_method_override: override processing method for specific layer
                version_override: override version for specific layer

            Returns:
                Full data lake path
        """
        if not all([self.domain, self.product]):
            raise ValueError("domain and product must be set to generate lake path")

        # Resolve version inline
        if version_override:
            version = version_override
        else:
            if layer == "bronze":
                version = self.bronze_version
            elif layer == "silver":
                version = self.silver_version
            elif layer == "gold":
                version = self.gold_version
            else:
                version = Defaults.VERSION

        # Resolve processing method inline
        if processing_method_override:
            processing_method = processing_method_override
        else:
            if layer == "bronze":
                processing_method = self.bronze_processing_method
            elif layer == "silver":
                processing_method = self.silver_processing_method
            elif layer == "gold":
                processing_method = self.gold_processing_method
            else:
                processing_method = Defaults.BRONZE_PROCESSING_METHOD

        return f"{self.datalake_container_name}/{layer}/{self.domain}/{self.product}/{self.table_name}/{version}/output/{processing_method}"

    def validate_rules(self, layers: list | None = None) -> bool:
        """Run repository-config rules against this CorePipelineConfig.

        Delegates to `run_rules_checks` and returns True if checks pass or
        raises ValueError if any rule fails.
        """
        # Import locally to avoid circular imports at module import time
        from .rules import run_rules_checks

        return run_rules_checks(self, layers)
