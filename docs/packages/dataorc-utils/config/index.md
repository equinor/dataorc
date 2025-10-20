---
title: dataorc-utils - Config
---

# dataorc-utils — Config

Lightweight configuration primitives for Data Lake pipelines deployed via Databricks Asset Bundles.

This overview explains where to find specific information:

| Topic | Go to | Summary |
|-------|------|---------|
| Immutable snapshot & path pattern | [CorePipelineConfig](core_pipeline_config.md) | Minimal immutable config + lake path pattern |
| Environment integration | [PipelineParameterManager](pipeline_parameter_manager.md) | Reads bundle variables / task env, builds validated config |
| Defaults & validation helpers | [Defaults and validation](defaults_and_validation.md) | Default constants, printing & rule validation |

Minimal usage (conceptual two-step):
```python
from dataorc_utils.config.manager import PipelineParameterManager

mgr = PipelineParameterManager()
infra = mgr.prepare_infrastructure()
cfg = mgr.build_core_config(infra, domain="sales", product="orders", table_name="order_lines")
print(cfg.get_lake_path("bronze"))
```

Refer to the linked pages for full variable lists, wheel job patterns, and validation examples.