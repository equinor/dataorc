"""Helpers for Azure Key Vault operations."""

from __future__ import annotations

import logging
import time
from typing import Any

logger = logging.getLogger(__name__)

# Module-level cache for credential and clients
_credential: Any = None
_clients: dict[str, Any] = {}


def _clear_cache() -> None:
    """Clear cached credentials and clients."""
    global _credential, _clients
    _credential = None
    _clients = {}


def get_keyvault_secret(
    vault_url: str,
    secret_name: str,
    max_retries: int = 2,
    retry_delay: float = 1.0,
) -> str:
    """Retrieve a secret from Azure Key Vault with retry logic.

    Args:
        vault_url: The vault URL (e.g. ``https://myvault.vault.azure.net/``).
        secret_name: The secret name to retrieve.
        max_retries: Maximum retry attempts (default: 3).
        retry_delay: Initial delay in seconds, doubles each retry (default: 1.0).

    Returns:
        The secret value as a string.

    Raises:
        ImportError: If the Azure SDK is not installed.
    """
    global _credential, _clients

    try:
        from azure.core.exceptions import (  # type: ignore
            ClientAuthenticationError,
            HttpResponseError,
            ServiceRequestError,
        )
        from azure.identity import DefaultAzureCredential  # type: ignore
        from azure.keyvault.secrets import SecretClient  # type: ignore
    except ImportError as exc:
        raise ImportError(
            "Azure SDK not installed. Install with 'pip install dataorc-utils[azure]'"
        ) from exc

    retryable = (ClientAuthenticationError, HttpResponseError, ServiceRequestError)
    last_exc: Exception | None = None

    for attempt in range(max_retries):
        try:
            # Lazy init credential and client
            if _credential is None:
                _credential = DefaultAzureCredential(
                    exclude_interactive_browser_credential=True,
                    exclude_visual_studio_code_credential=True,
                )
            if vault_url not in _clients:
                _clients[vault_url] = SecretClient(
                    vault_url=vault_url, credential=_credential
                )

            return _clients[vault_url].get_secret(secret_name).value

        except retryable as exc:
            last_exc = exc
            if attempt < max_retries - 1:
                delay = retry_delay * (2**attempt)
                logger.warning(
                    "Key Vault request failed (attempt %d/%d): %s. Retrying in %.1fs...",
                    attempt + 1,
                    max_retries,
                    exc,
                    delay,
                )
                time.sleep(delay)
                if isinstance(exc, ClientAuthenticationError):
                    _clear_cache()
            else:
                logger.error(
                    "Key Vault request failed after %d attempts: %s",
                    max_retries,
                    exc,
                )

    raise last_exc  # type: ignore[misc]
