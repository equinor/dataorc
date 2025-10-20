---
title: CorePipelineConfig
---

Minimal immutable configuration snapshot built via the manager API.

## Purpose

`CorePipelineConfig` is a frozen (immutable) dataclass produced by:

1. `PipelineParameterManager.prepare_infrastructure()` -> `InfraContext`
2. `PipelineParameterManager.build_core_config(infra, domain=..., product=..., table_name=..., ...)`

Treat it as read-only. Rebuild instead of mutating.

## Path pattern

```text
{container}/{layer}/{domain}/{product}/{table_name}/{version}/output/{processing_method}
```

`domain`, `product`, and `table_name` must be set before generating a path.

## Field summary

| Group | Fields | Defaults |
|-------|--------|----------|
| Required | `datalake_name`, `datalake_container_name`, `env` | (none) |
| Structure | `domain`, `product`, `table_name` | empty strings |
| Versions | `bronze_version`, `silver_version`, `gold_version` | `v1` |
| Processing | `bronze_processing_method`, `silver_processing_method`, `gold_processing_method` | `incremental`, `incremental`, `delta` |
| Azure infra | `az_tenant_id`, `az_subscription_id`, `az_keyvault_scope` | empty strings |

## Methods

- `get_lake_path(layer, processing_method_override=None, version_override=None)` – returns folder path; you can override method or version ad hoc.
- `validate_rules(layers=None)` – raises `ValueError` on rule failures (invoked automatically during build).

## Advanced usage

Direct instantiation of `CorePipelineConfig` is discouraged outside unit tests. Use the manager to ensure defaults and validation remain consistent.
