"""
Core library default values - truly generic defaults that apply to any data pipeline.

These are the only hardcoded defaults in the core library. Everything else should be
configured at the repository or product level.
"""

from .enums import CoreParam, LoadType

# Core library defaults - truly generic values that rarely change
# NOTE: These are the SINGLE SOURCE OF TRUTH for all default values.
# The CorePipelineConfig dataclass references these values to avoid duplication.
CORE_LIBRARY_DEFAULTS = {
    # Data pipeline layer versions (standard across most projects)
    CoreParam.BRONZE_VERSION: "v1",
    CoreParam.SILVER_VERSION: "v1",
    CoreParam.GOLD_VERSION: "v1",
    # Standard processing methods (can be overridden per product)
    CoreParam.BRONZE_PROCESSING_METHOD: "incremental",
    CoreParam.SILVER_PROCESSING_METHOD: "incremental",
    CoreParam.GOLD_PROCESSING_METHOD: "delta",
    # Standard load type
    CoreParam.LOAD_TYPE: LoadType.INCREMENTAL.value,
    # Table name default (generic placeholder)
    CoreParam.TABLE_NAME: "table",
}


def _merge_repository_defaults(base: dict, repository_defaults: dict | None) -> dict:
    """Merge repository defaults into the provided base config and return a new dict.

    This helper avoids mutating the original base mapping.
    """
    merged = base.copy()
    if repository_defaults:
        merged.update(repository_defaults)
    return merged


def _generate_infra_names(config: dict, env_name: str, env_config: dict) -> None:
    """Populate infrastructure-related names into `config` in-place.

    Expects `env_config` to contain `env_suffix` and `location` when infra names
    should be generated.
    """
    if "env_suffix" not in env_config or "location" not in env_config:
        return

    env_suffix = env_config["env_suffix"]
    location = env_config["location"]

    if "storage_prefix" in env_config:
        config[CoreParam.AZ_BLOB_STORAGE_ACCOUNT] = (
            f"{env_config['storage_prefix']}{env_suffix}{location}"
        )

    if "datalake_prefix" in env_config:
        config[CoreParam.AZ_DATALAKE_STORAGE_ACCOUNT] = (
            f"{env_config['datalake_prefix']}{env_suffix}{location}"
        )
        config[CoreParam.DATALAKE_NAME] = (
            f"{env_config['datalake_prefix']}{env_suffix}{location}"
        )

    if "keyvault_prefix" in env_config:
        config[CoreParam.AZ_KEYVAULT_SCOPE] = (
            f"{env_config['keyvault_prefix']}-{env_name}-{location}"
        )


def _add_api_management_url(config: dict, env_config: dict) -> None:
    """Add API Management base URL to `config` if both subdomain and domain are present."""
    if "apim_subdomain" in env_config and "apim_domain" in env_config:
        config[CoreParam.APIM_BASE_URL] = (
            f"https://{env_config['apim_subdomain']}.{env_config['apim_domain']}"
        )


def _apply_env_overrides(config: dict, env_config: dict) -> None:
    """Apply any remaining environment-specific overrides into `config` in-place."""
    reserved = {
        "env_suffix",
        "location",
        "apim_subdomain",
        "apim_domain",
        "keyvault_prefix",
        "storage_prefix",
        "datalake_prefix",
    }
    env_overrides = {k: v for k, v in env_config.items() if k not in reserved}
    config.update(env_overrides)


def build_environment_config(
    env_name: str, env_config: dict, repository_defaults: dict | None = None
) -> dict:
    """Build a complete environment configuration dictionary.

    The implementation delegates small, well-documented responsibilities to
    private helper functions to make maintenance easier.
    """
    # Start with core library defaults and merge repository defaults
    config = _merge_repository_defaults(CORE_LIBRARY_DEFAULTS, repository_defaults)

    # Add environment name
    config[CoreParam.ENV] = env_name

    # Populate infra names (storage, datalake, keyvault) when possible
    _generate_infra_names(config, env_name, env_config)

    # Add API Management URL if present
    _add_api_management_url(config, env_config)

    # Apply other environment-specific overrides
    _apply_env_overrides(config, env_config)

    return config


def resolve_environment_config(
    env: str,
    environments_config: dict | None = None,
    repository_defaults: dict | None = None,
    custom_overrides: dict | None = None,
) -> dict:
    """Resolve and return the complete configuration for `env`.

    This function validates that `env` exists in `environments_config`, builds
    the environment configuration using `build_environment_config`, and then
    applies any `custom_overrides`.
    """
    if not environments_config or env not in environments_config:
        available = list(environments_config.keys()) if environments_config else []
        raise ValueError(
            f"Environment '{env}' not found in repository configuration. "
            f"Available: {available}"
        )

    config = build_environment_config(
        env_name=env,
        env_config=environments_config[env],
        repository_defaults=repository_defaults,
    )

    if custom_overrides:
        config.update(custom_overrides)

    return config
