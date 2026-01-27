---
title: CorePipelineConfig
---

Immutable configuration snapshot built via `PipelineParameterManager`.

## Path pattern

```text
{container}/{layer}/{...path_segments}/{version}/output/{processing_method}
```

The `path_segments` tuple allows flexible naming hierarchy. Users can provide
1-N segments depending on their organizational needs.

**Examples:**
- Single segment: `raw/bronze/orders/v1/output/incremental`
- Three segments: `raw/bronze/finance/forecast/positions/v1/output/incremental`
- Five segments: `raw/bronze/org/dept/area/product/table/v1/output/incremental`

## Fields

| Group | Fields | Defaults |
|-------|--------|----------|
| Required | `env`, `path_segments` | `env` defaults to "dev"; `path_segments` is required (at least one) |
| Versions | `bronze_version`, `silver_version`, `gold_version` | `v1` |
| Processing | `bronze_processing_method`, `silver_processing_method`, `gold_processing_method` | `incremental`, `incremental`, `delta` |
| Infrastructure | `env_vars` (dict) | empty dict |

**Infrastructure variables** (specified in `prepare_infrastructure()`): `datalake_name`, `datalake_container_name`, Azure IDs, etc.

**Note:** the environment key used by the manager is `env` by default. Lookup follows the `PipelineParameterManager` `case_fallback` setting (exact name first, then uppercase/lowercase fallbacks if enabled). When `env` is not set in the environment, it defaults to `"dev"`.

**Accessing infrastructure variables:**
```python
tenant_id = cfg.env_vars["az_tenant_id"]
datalake = cfg.env_vars["datalake_name"]
```

## Methods

### get_lake_path(layer, processing_method_override=None, version_override=None, path_segments_override=None)

Returns folder path. Overrides are optional.

```python
# With path_segments=("sales", "orders", "order_lines")
cfg.get_lake_path("bronze")
# -> "data/bronze/sales/orders/order_lines/v1/output/incremental"

cfg.get_lake_path("gold", processing_method_override="full", version_override="v9")
# -> "data/gold/sales/orders/order_lines/v9/output/full"

# Override segments for this call only
cfg.get_lake_path("bronze", path_segments_override=("other", "path"))
# -> "data/bronze/other/path/v1/output/incremental"
```

### get_work_path(layer, version_override=None, path_segments_override=None)

Returns working path (ends with `/work`, no processing method).

```python
cfg.get_work_path("bronze")
# -> "data/bronze/sales/orders/order_lines/v1/work"
```

### validate_rules(layers=None)

Raises `ValueError` on rule failures. Called automatically by `build_core_config()`.
