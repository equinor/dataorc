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


Prerequisites:

- Install the optional extras which include the Azure SDK:

```bash
pip install "dataorc-utils[azure]"
```

- When running in Azure, ensure the host's managed identity or service principal has `GET` permissions on the Key Vault secret (Key Vault Access Policies or RBAC).

Notes:

- This helper is intentionally minimal: it uses `DefaultAzureCredential` and will raise any Azure SDK exception that occurs when retrieving the secret.
- For local development authenticate with `az login` or set up environment-based authentication supported by `DefaultAzureCredential`.
