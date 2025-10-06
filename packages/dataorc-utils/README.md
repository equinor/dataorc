# dataorc-utils

Lightweight utilities for configuring data lake ETL pipelines (early iteration).

## Status
Alpha – API surface is intentionally minimal and may change.

## Install
pip install -e packages/dataorc-utils

## Quickstart
from dataorc_utils.config.enums import Environment, LoadType
from dataorc_utils.config.models import CorePipelineConfig
from dataorc_utils.config.validation import print_config

cfg = CorePipelineConfig(
    datalake_name=\"<lake>\",
    datalake_container_name=\"raw\",
    env=Environment.DEV,
    load_type=LoadType.INCREMENTAL,
    domain=\"finance\",
    product=\"forecast\",
    table_name=\"positions\",
)

print_config(cfg)