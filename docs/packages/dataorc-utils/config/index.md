---
title: dataorc-utils - Config
---

# dataorc-utils — Config

Lightweight configuration for Data Lake pipelines.

| Topic | Link |
|-------|------|
| Immutable config & path pattern | [CorePipelineConfig](core_pipeline_config.md) |
| Environment integration | [PipelineParameterManager](pipeline_parameter_manager.md) |
| Validation helpers | [Defaults and validation](defaults_and_validation.md) |

## Quick start

```python
from dataorc_utils.config import PipelineParameterManager

mgr = PipelineParameterManager()

infra = mgr.prepare_infrastructure([
    "datalake_name",
    "datalake_container_name",
])

# path_segments is flexible - use 1 to N segments as needed
cfg = mgr.build_core_config(
    infra,
    path_segments=("sales", "orders", "order_lines"),
)

print(cfg.get_lake_path("bronze"))
# -> data/bronze/sales/orders/order_lines/v1/output/incremental

print(cfg.get_work_path("bronze"))
# -> data/bronze/sales/orders/order_lines/v1/work

# Single segment also works
cfg_simple = mgr.build_core_config(infra, path_segments=("orders",))
print(cfg_simple.get_lake_path("bronze"))
# -> data/bronze/orders/v1/output/incremental

# Access infrastructure variables
datalake = cfg.env_vars["datalake_name"]
# Or: infra.variables["datalake_name"]
```

Note: if `env` is not set in the environment, `prepare_infrastructure()` will default it to "dev".