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

cfg = mgr.build_core_config(
    infra,
    domain="sales",
    product="orders",
    table_name="order_lines",
)

print(cfg.get_lake_path("bronze"))
print(cfg.get_work_path("bronze"))

# Access infrastructure variables
datalake = cfg.env_vars["datalake_name"]
# Or: infra.variables["datalake_name"]
```