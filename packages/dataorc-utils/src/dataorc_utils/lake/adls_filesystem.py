"""AdlsLakeFileSystem - ADLS Gen2-backed file operations.

Drop-in alternative for LakeFileSystem that connects directly to
Azure Data Lake Storage Gen2 via the Azure SDK, removing the
dependency on Databricks mounts / dbutils.

Requires the ``azure`` extra::

    pip install dataorc-utils[azure]
"""

from __future__ import annotations

import logging
from typing import Any

from azure.identity import DefaultAzureCredential
from azure.storage.filedatalake import DataLakeServiceClient

from .protocols import LakeFileSystemProtocol

logger = logging.getLogger(__name__)


class AdlsLakeFileSystem(LakeFileSystemProtocol):
    """ADLS Gen2-backed file operations — drop-in for LakeFileSystem.

    Args:
        account_url: Full DFS endpoint, e.g.
            ``"https://<storage_account>.dfs.core.windows.net"``
        container: File-system / container name, e.g. ``"bronze"``
        base_path: Optional prefix inside the container prepended to
            every path.
        credential: Any Azure credential accepted by the SDK.
            Defaults to ``DefaultAzureCredential()``.

    Example::

        fs = AdlsLakeFileSystem(
            account_url="https://testdatadevsc.dfs.core.windows.net",
            container="bronze",
            base_path="raw/my_pipeline",
        )
        fs.write_json("data.json", {"key": "value"})
        data = fs.read_json("data.json")
    """

    def __init__(
        self,
        account_url: str,
        container: str,
        base_path: str = "",
        credential: Any | None = None,
    ):
        self._credential = credential or DefaultAzureCredential()
        self._service = DataLakeServiceClient(
            account_url=account_url,
            credential=self._credential,
        )
        self._fs_client = self._service.get_file_system_client(
            file_system=container,
        )
        self._base_path = base_path.strip("/")

    # ------------------------------------------------------------------
    # Text operations
    # ------------------------------------------------------------------

    def read_text(self, path: str) -> str | None:
        """Read a UTF-8 text file. Returns ``None`` if the file does not exist."""
        resolved = self._resolve(path)
        try:
            file_client = self._fs_client.get_file_client(resolved)
            download = file_client.download_file()
            return download.readall().decode("utf-8")
        except Exception:
            logger.debug("Could not read %s", resolved, exc_info=True)
            return None

    def write_text(self, path: str, content: str) -> None:
        """Write (or overwrite) a UTF-8 text file.

        Parent "directories" are created implicitly by ADLS Gen2.
        """
        resolved = self._resolve(path)
        file_client = self._fs_client.get_file_client(resolved)
        file_client.upload_data(content.encode("utf-8"), overwrite=True)

    # ------------------------------------------------------------------
    # Directory / existence helpers
    # ------------------------------------------------------------------

    def exists(self, path: str) -> bool:
        """Check whether a file exists."""
        resolved = self._resolve(path)
        try:
            file_client = self._fs_client.get_file_client(resolved)
            file_client.get_file_properties()
            return True
        except Exception:
            return False

    def delete(self, path: str) -> bool:
        """Delete a file. Returns ``True`` if deleted, ``False`` otherwise."""
        resolved = self._resolve(path)
        try:
            file_client = self._fs_client.get_file_client(resolved)
            file_client.delete_file()
            return True
        except Exception:
            return False
