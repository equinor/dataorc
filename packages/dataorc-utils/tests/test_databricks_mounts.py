import types

import pytest


class DummyFS:
    def __init__(self, mounted_points=None):
        self._mounted = set(mounted_points or [])

    def mounts(self):
        # return objects with .mountPoint attribute
        return [types.SimpleNamespace(mountPoint=m) for m in self._mounted]

    def mount(self, source, mount_point, extra_configs=None):
        if mount_point in self._mounted:
            raise RuntimeError("Already mounted")
        self._mounted.add(mount_point)

    def updateMount(self, source, mount_point, extra_configs=None):
        if mount_point not in self._mounted:
            raise RuntimeError("Not mounted")
        # simulate update by replacing configs (no-op here)

    def ls(self, mount_point):
        if mount_point not in self._mounted:
            raise RuntimeError("Not mounted")
        return [types.SimpleNamespace(path=mount_point + "/file1")]


class DummyDbutils:
    def __init__(self, mounted=None):
        self.fs = DummyFS(mounted)
        self.secrets = types.SimpleNamespace(get=lambda scope, key: "secret-value")


@pytest.fixture(autouse=True)
def patch_dbutils(monkeypatch):
    # Create a dummy dbutils and patch it into the module
    dummy = DummyDbutils(mounted=["/mnt/datalakestore"])  # default has one mount
    monkeypatch.setattr("dataorc_utils.databricks.mounts.dbutils", dummy)
    return dummy


def test_mount_when_not_present(monkeypatch, patch_dbutils):
    # Ensure mount at a new point succeeds
    from dataorc_utils.databricks.mounts import ensure_mount

    # choose a mount point that is not present
    success = ensure_mount(
        container_name="raw",
        datalake_name="mydatalake",
        tenant_id="t",
        secret_scope="s",
        client_id_key="id",
        client_secret_key="secret",
        mount_point="/mnt/newmount",
        update_if_exists=True,
    )
    assert success is True


def test_skip_update_when_exists(monkeypatch, patch_dbutils):
    from dataorc_utils.databricks.mounts import ensure_mount

    # existing mount '/mnt/datalakestore' exists in dummy
    success = ensure_mount(
        container_name="raw",
        datalake_name="mydatalake",
        tenant_id="t",
        secret_scope="s",
        client_id_key="id",
        client_secret_key="secret",
        mount_point="/mnt/datalakestore",
        update_if_exists=False,
    )
    assert success is True


def test_update_when_exists(monkeypatch, patch_dbutils):
    from dataorc_utils.databricks.mounts import ensure_mount

    success = ensure_mount(
        container_name="raw",
        datalake_name="mydatalake",
        tenant_id="t",
        secret_scope="s",
        client_id_key="id",
        client_secret_key="secret",
        mount_point="/mnt/datalakestore",
        update_if_exists=True,
    )
    assert success is True
