import os
import sys

import pytest

# Ensure the package src directory is on path before importing package
CURRENT_DIR = os.path.dirname(__file__)
SRC_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if SRC_ROOT not in sys.path:
    sys.path.insert(0, SRC_ROOT)

from dataorc_utils.config import (  # noqa: E402
    CoreParam,
    CorePipelineConfig,
    PipelineParameterManager,
)


def make_config(**overrides):
    base = dict(
        env="dev",
        path_segments=("finance", "forecast", "positions"),
        bronze_version="v1",
        silver_version="v2",
        gold_version="v3",
        bronze_processing_method="incremental",
        silver_processing_method="full",
        gold_processing_method="delta",
        env_vars={
            "datalake_name": "dlakeacct",
            "datalake_container_name": "raw",
        },
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


def test_validate_rules_fail_uppercase_segment():
    cfg = make_config(path_segments=("Finance", "forecast", "positions"))
    with pytest.raises(ValueError) as exc:
        cfg.validate_rules()
    assert "uppercase" in str(exc.value).lower()


def test_validate_rules_fail_bad_version_pattern():
    cfg = make_config(bronze_version="version1")  # missing leading 'v'
    with pytest.raises(ValueError) as exc:
        cfg.validate_rules()
    assert "pattern" in str(exc.value).lower() or "v<integer>" in str(exc.value)


def test_validate_rules_pass_custom_version_override():
    # Overrides should not break rule when format is correct
    cfg = make_config()
    path = cfg.get_lake_path("bronze", version_override="v99")
    assert path.endswith("/v99/output/incremental")


def test_case_fallback_env_uppercase_resolution(monkeypatch):
    """Primary fallback behavior: uppercase variant is resolved when case_fallback=True."""
    key_upper = "DATALAKE_NAME"
    key_lower = CoreParam.DATALAKE_NAME.value
    for k in (key_upper, key_lower):
        monkeypatch.delenv(k, raising=False)

    # On Windows env vars are case-insensitive, but logic path still runs.
    monkeypatch.setenv(key_upper, "LakeAcctFallback")
    monkeypatch.setenv("DATALAKE_CONTAINER_NAME", "container-fb")
    monkeypatch.setenv("env", "dev")

    mgr = PipelineParameterManager(case_fallback=True)
    infra = mgr.prepare_infrastructure(["datalake_name", "datalake_container_name"])
    assert infra.variables.get("datalake_name") == "LakeAcctFallback"
    assert infra.variables.get("datalake_container_name") == "container-fb"
