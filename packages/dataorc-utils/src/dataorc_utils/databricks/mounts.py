"""Databricks Data Lake Mount Utilities.

Provides idempotent functions for mounting, updating, listing and unmounting
Azure Data Lake Storage Gen2 (ABFS) containers in Databricks using `dbutils`.

Design goals:
- Safe: only mounts if not present, updates if already mounted.
- Explicit: caller supplies `container_name`, `datalake_name`, and auth settings
  are retrieved from Databricks secrets.
- Reusable: small focused functions to assist pipelines.

Example:
    from dataorc_utils.databricks.mounts import ensure_mount
    ensure_mount(
        container_name="raw",
        datalake_name="mydatalake",
        tenant_id="my-tenant-id",
        secret_scope="kv-sdf-dh",
        client_id_key="db-sp-id",
        client_secret_key="db-sp-secret",
        mount_point="/mnt/datalakestore"
    )

"""
from __future__ import annotations

from dataclasses import dataclass

try:  # Import guarded for non-Databricks local environments.
    from databricks.sdk.runtime import dbutils  # type: ignore
except Exception:  # pragma: no cover
    dbutils = None  # type: ignore


@dataclass(slots=True)
class OAuthConfig:
    """Holds client credential settings for ADLS OAuth."""
    tenant_id: str
    client_id: str
    client_secret: str

    def to_dict(self) -> dict[str, str]:
        return {
            "fs.azure.account.auth.type": "OAuth",
            "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
            "fs.azure.account.oauth2.client.id": self.client_id,
            "fs.azure.account.oauth2.client.secret": self.client_secret,
            "fs.azure.account.oauth2.client.endpoint": f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/token",
        }


def _get_oauth_config(tenant_id: str, secret_scope: str, client_id_key: str, client_secret_key: str) -> OAuthConfig:
    if dbutils is None:  # pragma: no cover
        raise RuntimeError("dbutils is not available. This module must run inside a Databricks notebook/cluster.")
    client_id = dbutils.secrets.get(scope=secret_scope, key=client_id_key)
    client_secret = dbutils.secrets.get(scope=secret_scope, key=client_secret_key)
    return OAuthConfig(tenant_id=tenant_id, client_id=client_id, client_secret=client_secret)


def _build_abfss_uri(container_name: str, datalake_name: str) -> str:
    """Internal: return ABFSS URI for a container.

    Example: abfss://raw@mydatalake.dfs.core.windows.net/
    """
    return f"abfss://{container_name}@{datalake_name}.dfs.core.windows.net/"


def _is_mounted(mount_point: str) -> bool:
    """Internal: return True if mount_point exists.

    Guarded for non-databricks environments.
    """
    if dbutils is None:  # pragma: no cover
        return False
    try:
        # dbutils.fs.mounts() returns list of objects with .mountPoint property
        return any(m.mountPoint == mount_point for m in dbutils.fs.mounts())
    except Exception:  # pragma: no cover
        return False


def ensure_mount(
    container_name: str,
    datalake_name: str,
    tenant_id: str,
    secret_scope: str,
    client_id_key: str,
    client_secret_key: str,
    mount_point: str = "/mnt/datalakestore",
    update_if_exists: bool = True,
) -> None:
    """Mount or update a Databricks mount point for an ADLS Gen2 container.

    If the mount exists and `update_if_exists` is True, `dbutils.fs.updateMount` is used.
    Otherwise it attempts a fresh mount.
    """
    if dbutils is None:  # pragma: no cover
        raise RuntimeError("dbutils is not available. Run inside Databricks.")
    oauth_cfg = _get_oauth_config(tenant_id, secret_scope, client_id_key, client_secret_key)
    configs = oauth_cfg.to_dict()
    source = _build_abfss_uri(container_name, datalake_name)

    if _is_mounted(mount_point):
        if update_if_exists:
            print(f"Updating mount at {mount_point} -> {source}")
            dbutils.fs.updateMount(source=source, mount_point=mount_point, extra_configs=configs)
        else:
            print(f"Mount point {mount_point} already exists; skipping update.")
    else:
        print(f"Mounting {source} at {mount_point}")
        dbutils.fs.mount(source=source, mount_point=mount_point, extra_configs=configs)

    # Simple verification listing the mount root
    dbutils.fs.ls(mount_point)








