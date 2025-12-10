"""Helpers for Azure Key Vault operations.

The helpers use the Azure SDK when available and fall back to environment
variables when running in environments without Key Vault access.
"""

from __future__ import annotations

from typing import Any


def get_keyvault_secret(vault_url: str, secret_name: str) -> str:
    """Retrieve a secret from Azure Key Vault using DefaultAzureCredential.

    The Azure SDK imports are performed inside the function so the module can be
    imported in environments where the optional `azure` extras are not installed.

    Args:
        vault_url: The full vault URL (e.g. ``https://myvault.vault.azure.net/``).
        secret_name: The secret name to retrieve.

    Returns:
        The secret value as a string.

    Raises:
        ImportError: If the Azure SDK is not installed.
        Any exception from the Azure SDK that arises when retrieving the secret.
    """

    try:
        from azure.identity import DefaultAzureCredential  # type: ignore
        from azure.keyvault.secrets import SecretClient  # type: ignore
    except Exception as exc:  # pragma: no cover - environment dependent
        raise ImportError(
            "Azure SDK not installed. Install with 'pip install dataorc-utils[azure]'"
        ) from exc

    cred: Any = DefaultAzureCredential()
    client: Any = SecretClient(vault_url=vault_url, credential=cred)
    secret = client.get_secret(secret_name)
    return secret.value
