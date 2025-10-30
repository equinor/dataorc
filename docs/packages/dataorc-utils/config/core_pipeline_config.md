---
title: CorePipelineConfig
---

Immutable configuration snapshot built via `PipelineParameterManager`.

## Path pattern

```text
{container}/{layer}/{domain}/{product}/{table_name}/{version}/output/{processing_method}
```

## Fields

| Group | Fields | Defaults |
|-------|--------|----------|
| Required | `env` | must be set |
| Structure | `domain`, `product`, `table_name` | empty strings |
| Versions | `bronze_version`, `silver_version`, `gold_version` | `v1` |
| Processing | `bronze_processing_method`, `silver_processing_method`, `gold_processing_method` | `incremental`, `incremental`, `delta` |
| Infrastructure | `env_vars` (dict) | empty dict |

**Infrastructure variables** (specified in `prepare_infrastructure()`): `datalake_name`, `datalake_container_name`, Azure IDs, etc.

**Accessing infrastructure variables:**
```python
tenant_id = cfg.env_vars["az_tenant_id"]
datalake = cfg.env_vars["datalake_name"]
```

## Methods

### get_lake_path(layer, processing_method_override=None, version_override=None)

Returns folder path. Overrides are optional.

```python
cfg.get_lake_path("bronze")
# -> "data/bronze/sales/orders/order_lines/v1/output/incremental"

cfg.get_lake_path("gold", processing_method_override="full", version_override="v9")
# -> "data/gold/sales/orders/order_lines/v9/output/full"
```

### get_work_path(layer, version_override=None)

Returns working path (ends with `/work`, no processing method).

```python
cfg.get_work_path("bronze")
# -> "data/bronze/sales/orders/order_lines/v1/work"
```

### validate_rules(layers=None)

Raises `ValueError` on rule failures. Called automatically by `build_core_config()`.
