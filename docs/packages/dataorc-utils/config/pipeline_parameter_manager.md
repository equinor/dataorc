---
title: PipelineParameterManager
---

Environment-driven config assembly. Reads from environment variables.

## Basic workflow

```python
from dataorc_utils.config import PipelineParameterManager
import os

os.environ["env"] = "dev"  # optional; `env` is a plain string (not an enum); defaults to 'dev' when not set
os.environ["datalake_name"] = "mydatalake"
os.environ["datalake_container_name"] = "data"

mgr = PipelineParameterManager()

# Capture infrastructure variables
infra = mgr.prepare_infrastructure([
    "datalake_name",
    "datalake_container_name",
])

# Build core config
cfg = mgr.build_core_config(
    infra,
    domain="sales",
    product="orders",
    table_name="order_lines",
)

print(cfg.get_lake_path("bronze"))
# -> data/bronze/sales/orders/order_lines/v1/output/incremental

# Access infrastructure variables
datalake = cfg.env_vars["datalake_name"]
container = cfg.env_vars["datalake_container_name"]
# Or from infra context: infra.variables["datalake_name"]
```

## Constructor

```python
PipelineParameterManager(
    environments_config: dict = None,
    domain_configs: dict = None,
    product_configs: dict = None,
    case_fallback: bool = False,
)
```

**Parameters:**
- `environments_config`, `domain_configs`, `product_configs` — optional advanced configs
- `case_fallback` — if True, tries uppercase fallback for env vars (default: False)

For most use cases: `PipelineParameterManager()`

## Methods

### prepare_infrastructure(env_vars)

Reads `env` (optional) and caller-specified variables. `env` is returned as a plain
string on the resulting `InfraContext`. If `env` is not set in the environment,
the manager defaults it to "dev".

Missing variables returned by `get_env_variables()` appear in the `variables` dict
as empty strings unless a default is applied. The lookup strategy is exact-name
first, and when `case_fallback=True` the manager will attempt uppercase then
lowercase variants.

Migration note: The previous `Environment` enum was removed — callers must treat
`env` as a plain `str` (no enum conversion is performed).

**Parameters:**
- `env_vars` (list[str]) — env var names to capture

**Returns:** `InfraContext` with `env` and `variables` dict

**Raises:** None. `env` defaults to "dev" when not provided.

```python
infra = mgr.prepare_infrastructure([
    "datalake_name",
    "datalake_container_name",
    "az_tenant_id",
])
```

### build_core_config(infra, domain, product, table_name, ...)

Assembles immutable `CorePipelineConfig`. Validates before returning.

**Parameters:**
- `infra` (InfraContext) — from `prepare_infrastructure()`
- `domain`, `product`, `table_name` — path structure
- `bronze_version`, `silver_version`, `gold_version` — defaults to `v1`
- `bronze_processing_method`, `silver_processing_method`, `gold_processing_method` — defaults to `incremental`, `incremental`, `delta`

**Returns:** `CorePipelineConfig`

```python
cfg = mgr.build_core_config(
    infra,
    domain="sales",
    product="orders",
    table_name="order_lines",
    bronze_version="v2",
)
```

### get_env_variables(var_names, required=False)

Reads env vars with optional case-insensitive fallback.

**Parameters:**
- `var_names` (list[str]) — variable names
- `required` (bool) — if True, raises on missing vars

**Returns:** `dict[str, str]`

```python
vars = mgr.get_env_variables(["datalake_name", "custom_var"])
```

## Key environment variables

**Optional:**
- `env` — execution environment (defaults to "dev"). Can be any string; not limited to a predefined set.

**Infrastructure variables** (specify in `prepare_infrastructure()`):
- `datalake_name`, `datalake_container_name` — storage info
- `az_tenant_id`, `az_client_id`, `az_subscription_id`, `az_keyvault_scope` — Azure auth
