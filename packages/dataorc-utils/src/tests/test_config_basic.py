import os
import sys
import pytest

# Ensure the package src directory is on path before importing package
CURRENT_DIR = os.path.dirname(__file__)
SRC_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if SRC_ROOT not in sys.path:
    sys.path.insert(0, SRC_ROOT)

from dataorc_utils.config import CorePipelineConfig, Environment, LoadType  # noqa: E402


def make_config(**overrides):
    base = dict(
        datalake_name="dlakeacct",
        datalake_container_name="raw",
        env=Environment.DEV,
        load_type=LoadType.INCREMENTAL,
        domain="finance",
        product="forecast",
        table_name="positions",
        bronze_version="v1",
        silver_version="v2",
        gold_version="v3",
        bronze_processing_method="incremental",
        silver_processing_method="full",
        gold_processing_method="delta",
    )
    base.update(overrides)
    return CorePipelineConfig(**base)


def test_lake_path_bronze():
    cfg = make_config()
    assert (
        cfg.get_lake_path("bronze")
        == "raw/bronze/finance/forecast/positions/v1/output/incremental"
    )


def test_lake_path_silver():
    cfg = make_config()
    assert (
        cfg.get_lake_path("silver")
        == "raw/silver/finance/forecast/positions/v2/output/full"
    )


def test_lake_path_gold():
    cfg = make_config()
    assert (
        cfg.get_lake_path("gold")
        == "raw/gold/finance/forecast/positions/v3/output/delta"
    )


def test_lake_path_overrides():
    cfg = make_config()
    custom = cfg.get_lake_path(
        "gold", processing_method_override="full", version_override="v9"
    )
    assert custom == "raw/gold/finance/forecast/positions/v9/output/full"


def test_validate_rules_pass():
    cfg = make_config()
    assert cfg.validate_rules() is True


def test_validate_rules_fail_uppercase_domain():
    cfg = make_config(domain="Finance")
    with pytest.raises(ValueError) as exc:
        cfg.validate_rules()
    assert "uppercase" in str(exc.value).lower()
