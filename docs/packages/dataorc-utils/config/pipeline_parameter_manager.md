---
title: PipelineParameterManager
---

`PipelineParameterManager` reads environment variables exactly as named (no implicit case changes) and enables a two-step assembly of configuration:

1. Infrastructure phase (`prepare_infrastructure`) – capture stable environment / lake / subscription context as an `InfraContext`.
2. Pipeline phase (`build_core_config`) – supply dataset‑specific identifiers and optional layer overrides to produce a validated `CorePipelineConfig`.

## Overview

Designed for Databricks Asset Bundle + wheel deployments:

1. Reads environment variables as defined in bundle `variables:` / task `environment:` blocks
2. Applies defaults only for layer version / processing overrides when not provided at build time
3. Separates infra state from dataset state (improves testability & reuse)
4. Validates resulting `CorePipelineConfig`

## Constructor

```python
PipelineParameterManager(
    environments_config: dict = None,
    repository_defaults: dict = None,
    domain_configs: dict = None,
    product_configs: dict = None,
    custom_params: Dict[Enum, str] = None,
    case_fallback: bool = False,
)
```

**Parameters:**

- `environments_config` (dict, optional): Environment-specific configurations (for advanced use)
- `repository_defaults` (dict, optional): Repository-level defaults (for advanced use)
- `domain_configs` (dict, optional): Domain-specific configurations (for advanced use)
- `product_configs` (dict, optional): Product-specific configurations (for advanced use)
- `custom_params` (Dict[Enum, str], optional): Additional custom parameters
- `case_fallback` (bool, optional): If True, falls back to `UPPER` then `lower` forms of each variable name when exact match is missing (bridges naming inconsistencies). Default False; enable only if migrating mixed-case environments.

For most use cases, initialize with no arguments: `PipelineParameterManager()`

## Usage pattern (conceptual)

1. Instantiate: `mgr = PipelineParameterManager()`.
2. Prepare infra context: `infra = mgr.prepare_infrastructure()` (captures lake/container/env + Azure IDs).
3. Build pipeline config: `cfg = mgr.build_core_config(infra, domain=..., product=..., table_name=..., bronze_version=..., bronze_processing_method=...)`.
4. Use `cfg.get_lake_path("bronze")` etc. in jobs.

`get_parameter_values()` remains available for raw inspection / troubleshooting.

## Methods (concise)

### prepare_infrastructure() -> InfraContext

Reads only infrastructure-related variables (lake name, container, env, Azure IDs). Returns an `InfraContext` object.

### build_core_config(infra: InfraContext, **overrides) -> CorePipelineConfig

Compose a validated configuration by adding dataset identifiers (`domain`, `product`, `table_name`) and optional per-layer overrides (versions, processing methods). Missing overrides fall back to defaults.

### get_parameter_values(param_list: list | None = None) -> dict

Low-level helper to retrieve raw environment mappings (used internally by other methods; exposed for diagnostics).

## Key environment variables

Infrastructure: `DATALAKE_NAME`, `DATALAKE_CONTAINER_NAME`, `ENV`, Azure IDs & scopes.

Pipeline identifiers: `DOMAIN`, `PRODUCT`, `TABLE_NAME` (passed when calling `build_core_config`).

Optional layer overrides: versions & processing methods (`BRONZE_VERSION`, etc.)—may be provided as environment variables or passed explicitly when building the config.

## Advanced usage & rationale

You normally just call `prepare_infrastructure()` then `build_core_config(...)`. The optional constructor dictionaries let you inject repository or domain knowledge without scattering conditionals through jobs.

| Argument | Purpose | When to use |
|----------|---------|-------------|
| `environments_config` | Override values per environment (e.g., different storage accounts) | Centralize environment differences instead of branching in code |
| `repository_defaults` | Provide default versions / processing methods shared across many jobs | Reduce repetition of identical overrides |
| `domain_configs` | Domain-specific defaults (e.g., all finance tables use `incremental` silver) | Enforce domain conventions |
| `product_configs` | Product/project specific tweaks | Consistency within a product scope |
| `custom_params` | Extra enum-keyed parameters not part of core set | Extend without modifying library code |

### Example: environment-specific override

```python
envs = {
    "dev": {"DATALAKE_CONTAINER_NAME": "data-dev"},
    "prod": {"DATALAKE_CONTAINER_NAME": "data"},
}
mgr = PipelineParameterManager(environments_config=envs)
infra = mgr.prepare_infrastructure()  # picks container based on ENV env var
cfg = mgr.build_core_config(infra, domain="sales", product="orders", table_name="order_lines")
```

### Example: domain + product defaults

```python
domain_defaults = {"sales": {"BRONZE_PROCESSING_METHOD": "incremental"}}
product_defaults = {"orders": {"GOLD_PROCESSING_METHOD": "delta"}}
mgr = PipelineParameterManager(domain_configs=domain_defaults, product_configs=product_defaults)
infra = mgr.prepare_infrastructure()
cfg = mgr.build_core_config(infra, domain="sales", product="orders", table_name="order_lines")
```

### Example: custom parameter extension

Define your own enum for extra parameters (e.g., `RUN_MODE`) and pass values via environment variables or `custom_params`.

```python
from enum import Enum

class ExtraParam(Enum):
    RUN_MODE = "RUN_MODE"

os.environ["RUN_MODE"] = "dry_run"
mgr = PipelineParameterManager(custom_params={ExtraParam.RUN_MODE: "dry_run"})
infra = mgr.prepare_infrastructure()
cfg = mgr.build_core_config(infra, domain="sales", product="orders", table_name="order_lines")
```

Rationale: Centralizing these patterns keeps jobs lean and makes adjustments (e.g., switching processing methods for a domain) a configuration change instead of code edits.
