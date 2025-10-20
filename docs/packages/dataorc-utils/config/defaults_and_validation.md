---
title: Defaults and validation
---

Helper constants and validation utilities for the configuration system.

## Defaults class

Location: `dataorc_utils.config.enums.Defaults`

```python
from dataorc_utils.config.enums import Defaults

Defaults.VERSION  # "v1"
Defaults.BRONZE_PROCESSING_METHOD  # "incremental"
Defaults.SILVER_PROCESSING_METHOD  # "incremental"
Defaults.GOLD_PROCESSING_METHOD    # "delta"
```

## Printing configuration

`print_config(config: CorePipelineConfig, title: str = "Pipeline Configuration")` prints a formatted summary.

```python
from dataorc_utils.config.manager import PipelineParameterManager
from dataorc_utils.config.validation import print_config

mgr = PipelineParameterManager()
infra = mgr.prepare_infrastructure()
cfg = mgr.build_core_config(infra, domain="sales", product="orders", table_name="order_lines")

print_config(cfg, title="Sales Orders Pipeline")
```

## Rule validation

`CorePipelineConfig.validate_rules()` raises `ValueError` if a rule fails. Called automatically by `PipelineParameterManager.build_core_config()`.

Advanced (rare) usage: You can instantiate `CorePipelineConfig` directly for unit tests, but production code should prefer the `PipelineParameterManager` two-step (`prepare_infrastructure` + `build_core_config`) to ensure consistent defaults and validation.

## Complete validation example

```python
import os
from dataorc_utils.config.manager import PipelineParameterManager
from dataorc_utils.config.validation import print_config

os.environ["DATALAKE_NAME"] = "mydatalake"
os.environ["DATALAKE_CONTAINER_NAME"] = "data"
os.environ["ENV"] = "dev"
os.environ["DOMAIN"] = "sales"
os.environ["PRODUCT"] = "orders"
os.environ["TABLE_NAME"] = "order_lines"

mgr = PipelineParameterManager()
infra = mgr.prepare_infrastructure()
cfg = mgr.build_core_config(infra, domain="sales", product="orders", table_name="order_lines")

print_config(cfg, title="Validated Pipeline Config")
print(f"Path: {cfg.get_lake_path('bronze')}")
print(f"Work path: {cfg.get_work_path('bronze')}")
```

## Sample print_config output

Example output (values will vary):

```text
📦 Pipeline Configuration
     Environment: test
     Data Lake: coral-lake-7
     Container: ingest
     🏗️ Data Lake Structure:
         Domain: maritime
         Product: bathymetry
         Table: tidegrid
         Bronze Version: v1
         Silver Version: v2
         Gold Version: v3
     ⚙️ Processing Methods:
         Bronze: incremental
         Silver: snapshot
         Gold: delta
     📁 Generated Paths:
         Bronze Lake Path: ingest/bronze/maritime/bathymetry/tidegrid/v1/output/incremental
         Silver Lake Path: ingest/silver/maritime/bathymetry/tidegrid/v2/output/snapshot
         Gold Lake Path: ingest/gold/maritime/bathymetry/tidegrid/v3/output/delta
     📁 Work paths:
         Bronze: ingest/bronze/maritime/bathymetry/tidegrid/v1/work
         Silver: ingest/silver/maritime/bathymetry/tidegrid/v2/work
         Gold: ingest/gold/maritime/bathymetry/tidegrid/v3/work
     KeyVault Scope: kv-maritime-test
```

