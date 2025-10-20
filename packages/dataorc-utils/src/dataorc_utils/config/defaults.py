"""
Environment configuration builders.

Functions for building complete environment configurations from templates.
No longer contains global defaults - those moved to enums.Defaults class.
"""

from .enums import CoreParam


def _generate_infra_names(config: dict, env_name: str, env_config: dict) -> None:
    """Populate infrastructure-related names into `config` in-place.

    Expects `env_config` to contain `env_suffix` and `location` when infra names
    should be generated.
    """
    if "env_suffix" not in env_config or "location" not in env_config:
        return

    env_suffix = env_config["env_suffix"]
    location = env_config["location"]

    if "datalake_prefix" in env_config:
        config[CoreParam.DATALAKE_NAME] = (
            f"{env_config['datalake_prefix']}{env_suffix}{location}"
        )

    if "keyvault_prefix" in env_config:
        config[CoreParam.AZ_KEYVAULT_SCOPE] = (
            f"{env_config['keyvault_prefix']}-{env_name}-{location}"
        )


def _apply_env_overrides(config: dict, env_config: dict) -> None:
    """Apply any remaining environment-specific overrides into `config` in-place."""
    reserved = {
        "env_suffix",
        "location",
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
    # Start with repository defaults (or empty dict)
    config = (repository_defaults or {}).copy()

    # Add environment name
    config[CoreParam.ENV] = env_name

    # Populate infra names (storage, datalake, keyvault) when possible
    _generate_infra_names(config, env_name, env_config)

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
