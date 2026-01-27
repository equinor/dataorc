# Azure helpers

This page documents small Azure helpers included in `dataorc_utils.azure`.

## Key Vault: `get_keyvault_secret`

Retrieve a secret from Azure Key Vault using `DefaultAzureCredential`.

Usage:

```python
from dataorc_utils.azure import get_keyvault_secret

val = get_keyvault_secret(
    vault_url="https://myvault.vault.azure.net/",
    secret_name="my-secret",
)
print(val)
```

### Retry and caching behavior

The function includes built-in resilience for parallel execution scenarios:

- **Credential caching**: Credentials and clients are cached at module level to reduce token acquisition overhead
- **Retry with exponential backoff**: Transient failures are retried up to 3 times by default
- **Automatic credential refresh**: On authentication errors, the credential cache is cleared and fresh credentials are acquired

You can customize retry behavior:

```python
val = get_keyvault_secret(
    vault_url="https://myvault.vault.azure.net/",
    secret_name="my-secret",
    max_retries=5,      # Default: 3
    retry_delay=2.0,    # Default: 1.0 seconds (doubles each retry)
)
```


Prerequisites:

- Install the optional extras which include the Azure SDK:

```bash
pip install "dataorc-utils[azure]"
```

- When running in Azure, ensure the host's managed identity or service principal has `GET` permissions on the Key Vault secret (Key Vault Access Policies or RBAC).

Notes:

- This helper uses `DefaultAzureCredential` with optimized settings for non-interactive environments
- For local development authenticate with `az login` or set up environment-based authentication supported by `DefaultAzureCredential`
