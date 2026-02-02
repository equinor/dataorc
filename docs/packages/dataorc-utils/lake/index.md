---
title: dataorc-utils - Lake
---

# dataorc-utils — Lake

Filesystem utilities for reading and writing to the Data Lake in Databricks pipelines.

## Overview

The `lake` module provides a unified interface for file operations on Azure Data Lake Storage,
abstracting away the differences between local development and Databricks runtime environments.

**Key design principle:** The module is **path-agnostic**. It performs pure I/O operations
without assuming any specific mounting conventions. Path normalization (e.g., `dls://` → `/mnt/...`)
is the responsibility of your pipeline code.

## Quick start

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

## API Reference

### LakeFileSystem

The main class for all file operations.

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
| `makedirs(path, exist_ok=True)` | `None` | Create directory and all parent directories. |

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

## Runtime Detection

The module automatically detects whether it's running on Databricks (by checking for `/dbfs`)
and uses the appropriate fsspec backend. This is transparent to your code.
