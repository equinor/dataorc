import types

import pytest


class DummyFS:
    def __init__(self, mounted_points=None):
        self._mounted = set(mounted_points or [])
        self.mount_calls = []
        self.update_calls = []

    def mounts(self):
        # return objects with .mountPoint attribute
        return [types.SimpleNamespace(mountPoint=m) for m in self._mounted]

    def mount(self, source, mount_point, extra_configs=None):
        self.mount_calls.append((source, mount_point, extra_configs))
        if mount_point in self._mounted:
            raise RuntimeError("Already mounted")
        self._mounted.add(mount_point)

    def updateMount(self, source, mount_point, extra_configs=None):
        self.update_calls.append((source, mount_point, extra_configs))
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


@pytest.mark.parametrize(
    "mount_point,update_if_exists,should_mount,should_update",
    [
        ("/mnt/newmount", True, True, False),
        ("/mnt/datalakestore", False, False, False),
        ("/mnt/datalakestore", True, False, True),
    ],
)
def test_ensure_mount_behaviors(
    mount_point, update_if_exists, should_mount, should_update
):
    from dataorc_utils.databricks import mounts

    result = mounts.ensure_mount(
        container_name="raw",
        datalake_name="mydatalake",
        tenant_id="t",
        secret_scope="s",
        client_id_key="id",
        client_secret_key="secret",
        mount_point=mount_point,
        update_if_exists=update_if_exists,
    )

    assert result is True
    # inspect the patched dbutils state in the module
    fs = mounts.dbutils.fs

    if should_mount:
        assert any(call[1] == mount_point for call in fs.mount_calls)
        assert mount_point in fs._mounted
    else:
        assert not any(call[1] == mount_point for call in fs.mount_calls)

    if should_update:
        assert any(call[1] == mount_point for call in fs.update_calls)
    else:
        assert not any(call[1] == mount_point for call in fs.update_calls)
