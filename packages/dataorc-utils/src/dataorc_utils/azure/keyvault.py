"""Helpers for Azure Key Vault operations.

The helpers use the Azure SDK when available and fall back to environment
variables when running in environments without Key Vault access.
"""

# Use postponed evaluation of annotations to avoid import-time evaluation
# (prevents unnecessary runtime imports and helps with forward references).
from __future__ import annotations

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


def get_keyvault_secret(vault_url: str, secret_name: str) -> str:
    """Retrieve a secret from Azure Key Vault using DefaultAzureCredential.

    Args:
        vault_url: The full vault URL (e.g. ``https://myvault.vault.azure.net/``).
        secret_name: The secret name to retrieve.

    Returns:
        The secret value as a string.

    Raises:
        Any exception from the Azure SDK that arises when retrieving the secret.
    """

    cred = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=cred)
    secret = client.get_secret(secret_name)
    return secret.value
