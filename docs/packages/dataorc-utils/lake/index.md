---
title: dataorc-utils - Lake
---

# dataorc-utils — Lake

Filesystem utilities for reading and writing to the Data Lake.

## Overview

The `lake` module provides a unified interface for file operations on Azure Data Lake Storage.
Two implementations are available:

| Class | Backend | Use case |
|-------|---------|----------|
| `LakeFileSystem` | Local / FUSE mount (via `fsspec`) | Databricks with mounted storage |
| `AdlsLakeFileSystem` | ADLS Gen2 SDK (direct) | Any environment — no mounts or dbutils needed |

Both classes inherit from `LakeFileSystemProtocol` and expose the **same core API**
(`read_text`, `write_text`, `read_json`, `write_json`, `exists`, `delete`),
so switching between them requires only changing the constructor.

The `LakeFileSystemProtocol` serves double duty:

- **Type hint** — use it when your code should accept *any* filesystem backend
  without coupling to a concrete class.
- **Shared logic** — subclasses that inherit from it get `read_json`, `write_json`,
  and `_resolve` for free. Only the four backend-specific primitives need implementing.

**Key design principle:** The module is **path-agnostic**. It performs pure I/O operations
without assuming any specific mounting conventions.

### Architecture

```text
LakeFileSystemProtocol (Protocol)
├── read_text()      ← primitive  (each backend implements)
├── write_text()     ← primitive
├── exists()         ← primitive
├── delete()         ← primitive
├── _resolve()       ← shared (prepends base_path)
├── read_json()      ← shared (calls read_text)
└── write_json()     ← shared (calls write_text)

LakeFileSystem(LakeFileSystemProtocol)       # fsspec / local / FUSE mount
AdlsLakeFileSystem(LakeFileSystemProtocol)   # Azure SDK (direct ADLS Gen2)
```

## Quick start

### LakeFileSystem (mount-based)

```python
from dataorc_utils.lake import LakeFileSystem

# Initialize with a base path
fs = LakeFileSystem(base_path="/dbfs/mnt/datalakestore/bronze/sales/orders")

# Write and read text files
fs.write_text("metadata.txt", "Pipeline run: 2026-02-02")
content = fs.read_text("metadata.txt")

# Write and read JSON files
fs.write_json("config.json", {"version": 1, "status": "complete"})
config = fs.read_json("config.json")

# Check existence and delete
if fs.exists("old_file.txt"):
    fs.delete("old_file.txt")
```

### AdlsLakeFileSystem (direct ADLS Gen2)

!!! note "Requires the `azure` extra"
    Install with: `pip install dataorc-utils[azure]`

```python
from dataorc_utils.lake import AdlsLakeFileSystem

# Connect directly to ADLS Gen2 — no mounts or dbutils required
fs = AdlsLakeFileSystem(
    account_url="https://testdatadevsc.dfs.core.windows.net",
    container="bronze",
    base_path="sales/orders",          # optional prefix inside the container
)

# Same API from here on
fs.write_text("metadata.txt", "Pipeline run: 2026-02-02")
content = fs.read_text("metadata.txt")

fs.write_json("config.json", {"version": 1, "status": "complete"})
config = fs.read_json("config.json")

if fs.exists("old_file.txt"):
    fs.delete("old_file.txt")
```

Authentication uses `DefaultAzureCredential` by default, which supports
Managed Identity, Azure CLI (`az login`), and environment variables.
You can also pass a custom credential via the `credential` parameter
(e.g. `ManagedIdentityCredential()`).

## API Reference

### LakeFileSystemProtocol

The shared `Protocol` that defines the filesystem contract.
Both implementations inherit from it, gaining `read_json`,
`write_json`, and `_resolve` automatically.

Each backend provides its own `read_text`, `write_text`, `exists`,
and `delete`.

### LakeFileSystem

The fsspec-backed implementation for local / FUSE-mount environments.

```python
from dataorc_utils.lake import LakeFileSystem

fs = LakeFileSystem(base_path="/dbfs/mnt/datalakestore/bronze")
```

#### Constructor

| Parameter | Type | Description |
|-----------|------|-------------|
| `base_path` | `str \| None` | Optional base path prepended to all operations. Should be an absolute path valid for the runtime environment. |

#### Methods

##### Text Operations

| Method | Returns | Description |
|--------|---------|-------------|
| `read_text(path)` | `str \| None` | Read a text file. Returns `None` if file doesn't exist. |
| `write_text(path, content)` | `None` | Write a text file. Creates parent directories if needed. |

##### JSON Operations

| Method | Returns | Description |
|--------|---------|-------------|
| `read_json(path)` | `dict \| None` | Read and parse a JSON file. Returns `None` if file doesn't exist or parse fails. |
| `write_json(path, data, indent=2)` | `None` | Write a dictionary as JSON. Creates parent directories if needed. |

##### Directory Operations

| Method | Returns | Description |
|--------|---------|-------------|
| `exists(path)` | `bool` | Check if a file or directory exists. |
| `delete(path)` | `bool` | Delete a file. Returns `True` if deleted, `False` if didn't exist. |

---

### AdlsLakeFileSystem

Direct connection to ADLS Gen2 — no mounts or Databricks utilities required.

#### Constructor

| Parameter | Type | Description |
|-----------|------|-------------|
| `account_url` | `str` | Full DFS endpoint, e.g. `"https://<account>.dfs.core.windows.net"` |
| `container` | `str` | File-system / container name, e.g. `"bronze"` |
| `base_path` | `str` | Optional prefix inside the container prepended to every path. Defaults to `""`. |
| `credential` | `Any \| None` | Any Azure credential accepted by the SDK. Defaults to `DefaultAzureCredential()`. |

#### Methods

`AdlsLakeFileSystem` exposes the same text, JSON, and directory methods as `LakeFileSystem`:

##### Text Operations

| Method | Returns | Description |
|--------|---------|-------------|
| `read_text(path)` | `str \| None` | Read a UTF-8 text file. Returns `None` if the file doesn't exist. |
| `write_text(path, content)` | `None` | Write (or overwrite) a UTF-8 text file. |

##### JSON Operations

| Method | Returns | Description |
|--------|---------|-------------|
| `read_json(path)` | `dict \| None` | Read and parse a JSON file. Returns `None` if the file doesn't exist or parse fails. |
| `write_json(path, data, indent=2)` | `None` | Write a dictionary as JSON. |

##### Directory Operations

| Method | Returns | Description |
|--------|---------|-------------|
| `exists(path)` | `bool` | Check if a file exists. |
| `delete(path)` | `bool` | Delete a file. Returns `True` if deleted, `False` otherwise. |

## Usage in Pipelines

### With CorePipelineConfig

The `lake` module integrates naturally with `CorePipelineConfig`:

```python
from dataorc_utils.config import PipelineParameterManager
from dataorc_utils.lake import LakeFileSystem

# Build config as usual
mgr = PipelineParameterManager()
infra = mgr.prepare_infrastructure(["datalake_name"])
cfg = mgr.build_core_config(infra, domain="sales", product="orders", table_name="lines")

# Use lake paths from config
fs = LakeFileSystem(base_path=cfg.get_lake_path("bronze"))

# Now all operations are relative to the bronze path
fs.write_json("_metadata/run_info.json", {
    "pipeline": "orders_ingestion",
    "timestamp": "2026-02-02T10:00:00Z",
    "records_processed": 1500
})
```

### Path Handling

#### LakeFileSystem

The module does **not** perform path normalization. Your pipeline code is responsible for
providing correct absolute paths for the runtime environment.

On Databricks with FUSE mount, paths should include the `/dbfs/` prefix:

```python
# Correct - includes /dbfs/ prefix
fs = LakeFileSystem(base_path="/dbfs/mnt/datalakestore/bronze")

# Or use absolute paths directly
fs = LakeFileSystem()
fs.write_text("/dbfs/mnt/datalakestore/bronze/file.txt", "content")
```

#### AdlsLakeFileSystem

Paths are always **relative to the container and `base_path`** — no mount prefixes needed.
For example, with `container="bronze"` and `base_path="sales/orders"`,
calling `fs.write_text("file.txt", ...)` resolves to `bronze/sales/orders/file.txt`.

### Error Handling

The module returns `None` for missing files rather than raising exceptions:

```python
fs = LakeFileSystem(base_path="/dbfs/mnt/datalake")

# Safe - returns None if file doesn't exist
config = fs.read_json("config.json")
if config is None:
    config = {"default": "values"}

# Safe - returns False if file doesn't exist
deleted = fs.delete("maybe_exists.txt")
```
