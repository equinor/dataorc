---
title: Defaults and validation
---

Helper constants and validation utilities.

## Defaults

Location: `dataorc_utils.config.enums.Defaults`

```python
from dataorc_utils.config.enums import Defaults

Defaults.VERSION  # "v1"
Defaults.BRONZE_PROCESSING_METHOD  # "incremental"
Defaults.SILVER_PROCESSING_METHOD  # "incremental"
Defaults.GOLD_PROCESSING_METHOD    # "delta"
```

## print_config(config, title="Pipeline Configuration")

Prints formatted summary.

```python
from dataorc_utils.config.validation import print_config

print_config(cfg, title="Sales Orders Pipeline")
```

**Sample output:**

```text
📦 Pipeline Configuration
   Environment: dev
   🏗️ Data Lake Structure:
     Domain: sales
     Product: orders
     Table: order_lines
     Bronze Version: v1
     Silver Version: v1
     Gold Version: v1
    # The version format now optionally supports a revision suffix, e.g. v1r2
   ⚙️ Processing Methods:
     Bronze: incremental
     Silver: incremental
     Gold: delta
   📁 Generated Paths:
    Bronze Lake Path: data/bronze/sales/orders/order_lines/v1/output/incremental
    Silver Lake Path: data/silver/sales/orders/order_lines/v1r2/output/incremental
    Gold Lake Path: data/gold/sales/orders/order_lines/v1/output/delta
   📁 Work paths:
     Bronze: data/bronze/sales/orders/order_lines/v1/work
     Silver: data/silver/sales/orders/order_lines/v1/work
     Gold: data/gold/sales/orders/order_lines/v1/work
   🔧 Infrastructure Variables:
     datalake_container_name: data
     datalake_name: mydatalake
```

## validate_rules()

`CorePipelineConfig.validate_rules()` raises `ValueError` if rule fails. Called automatically by `build_core_config()`.

## Example

```python
import os
from dataorc_utils.config import PipelineParameterManager
from dataorc_utils.config.validation import print_config

os.environ["env"] = "dev"  # exact name match; set PipelineParameterManager(case_fallback=True) to allow UPPER/lower fallbacks
os.environ["datalake_container_name"] = "data"

mgr = PipelineParameterManager()
infra = mgr.prepare_infrastructure(["datalake_container_name"])
cfg = mgr.build_core_config(infra, domain="sales", product="orders", table_name="order_lines")

print_config(cfg)
print(cfg.get_lake_path("bronze"))
```

