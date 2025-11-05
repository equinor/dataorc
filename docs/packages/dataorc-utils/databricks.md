# Databricks utilities

This page documents Databricks-specific helpers in `dataorc_utils.databricks`.

## Mounting an Azure Data Lake (ADLS Gen2)

Use `ensure_mount` to idempotently mount or update an ABFS container into Databricks.

### Function

`ensure_mount(container_name, datalake_name, tenant_id, secret_scope, client_id_key, client_secret_key, mount_point='/mnt/datalakestore', update_if_exists=True)`

Parameters:

- `container_name` (str): The ADLS Gen2 container name (e.g. `raw`).
- `datalake_name` (str): The storage account / datalake name (e.g. `mydatalake`).
- `tenant_id` (str): Azure tenant ID used to build the OAuth token endpoint.
- `secret_scope` (str): Databricks secret scope where client id & secret are stored.
- `client_id_key` (str): Secret key name for the service principal client id.
- `client_secret_key` (str): Secret key name for the service principal client secret.
- `mount_point` (str, optional): Where to mount in DBFS. Defaults to `/mnt/datalakestore`.
- `update_if_exists` (bool, optional): If `True`, existing mount is updated with new creds; if `False`, existing mount is left alone.

### Example (Databricks notebook)

```python
from dataorc_utils.databricks import ensure_mount

ensure_mount(
    container_name="raw",
    datalake_name="mydatalake",
    tenant_id="your-tenant-id",
    secret_scope="kv-sdf-dh",
    client_id_key="db-sp-id",
    client_secret_key="db-sp-secret",
    mount_point="/mnt/datalakestore",
)
```

Notes:
- `ensure_mount` reads the client id and secret from the given Databricks secret scope.
- `ensure_mount` is safe to call on every job start; it will update if necessary and otherwise ensure the mount exists.

***

If you want a smaller wrapper that only mounts without updating, call with `update_if_exists=False`.
