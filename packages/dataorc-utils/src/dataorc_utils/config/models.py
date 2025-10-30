"""Core configuration data classes."""

from dataclasses import dataclass, field

from .enums import Defaults, Environment


@dataclass
class InfraContext:
    """Infrastructure-level context captured prior to pipeline specifics.

    Stable across multiple pipeline jobs; excludes dataset identifiers and
    per-layer version/processing configuration.

    The `variables` dict holds all infrastructure environment variables
    (e.g., datalake_name, datalake_container_name, Azure tenant/client IDs, etc.)
    that were requested when calling prepare_infrastructure().
    """

    env: Environment
    variables: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class CorePipelineConfig:
    """Immutable pipeline configuration snapshot.

    Path pattern: container/{layer}/{domain}/{product}/{table_name}/{version}/output/{processing_method}
    Construct via PipelineParameterManager.build_core_config() in production code.

    The `env_vars` dict holds infrastructure environment variables
    (e.g., datalake_name, datalake_container_name, Azure IDs, etc.) captured during
    prepare_infrastructure().
    """

    # Required
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

    # Flexible infrastructure variables (datalake_name, container, Azure IDs, etc.)
    env_vars: dict[str, str] = field(default_factory=dict)
    # Convenience properties that return the canonical lake path for each layer.

    def get_lake_path(
        self,
        layer: str,
        processing_method_override: str = None,
        version_override: str = None,
        domain_override: str = None,
        product_override: str = None,
        table_name_override: str = None,
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
        # Allow callers to override identifiers; fall back to the instance values.
        domain = domain_override or self.domain
        product = product_override or self.product
        table_name = table_name_override or self.table_name
        container = self.env_vars.get("datalake_container_name", "")

        if not all([container, domain, product, table_name]):
            raise ValueError(
                "datalake_container_name, domain, product and table_name must be set to generate lake path"
            )

        # Resolve attribute names directly (e.g. bronze_version, bronze_processing_method)
        v_attr = f"{layer}_version"
        p_attr = f"{layer}_processing_method"

        version = version_override or getattr(self, v_attr, Defaults.VERSION)
        processing_method = processing_method_override or getattr(
            self, p_attr, Defaults.BRONZE_PROCESSING_METHOD
        )

        return f"{container}/{layer}/{domain}/{product}/{table_name}/{version}/output/{processing_method}"

    def get_work_path(
        self,
        layer: str,
        version_override: str = None,
        domain_override: str = None,
        product_override: str = None,
        table_name_override: str = None,
    ) -> str:
        """Return the working path for a layer.

        This reuses `get_lake_path(...)` and replaces the trailing
        `/output/{processing_method}` segment with `/work`. If the
        expected `/output/` segment isn't found, `/work` is appended.
        """
        # Reuse get_lake_path to compose the canonical path and then
        # convert it to a work path by replacing the output segment.
        lake_path = self.get_lake_path(
            layer,
            processing_method_override=None,
            version_override=version_override,
            domain_override=domain_override,
            product_override=product_override,
            table_name_override=table_name_override,
        )

        marker = "/output/"
        idx = lake_path.find(marker)
        if idx >= 0:
            return lake_path[:idx] + "/work"
        # Fallback: append /work if format differs
        return lake_path.rstrip("/") + "/work"

    def validate_rules(self, layers: list | None = None) -> bool:
        """Run repository-config rules against this CorePipelineConfig.

        Delegates to `run_rules_checks` and returns True if checks pass or
        raises ValueError if any rule fails.
        """
        # Import locally to avoid circular imports at module import time
        from .rules import run_rules_checks

        return run_rules_checks(self, layers)

    @property
    def bronze_lake_path(self) -> str:
        return self.get_lake_path("bronze")

    @property
    def silver_lake_path(self) -> str:
        return self.get_lake_path("silver")

    @property
    def gold_lake_path(self) -> str:
        return self.get_lake_path("gold")
