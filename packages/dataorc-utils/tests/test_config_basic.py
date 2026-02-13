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


def make_config(container_name="raw", **overrides):
    env_vars = {"datalake_name": "dlakeacct"}
    if container_name:
        env_vars["datalake_container_name"] = container_name
    base = dict(
        env="dev",
        domain="finance",
        product="forecast",
        table_name="positions",
        bronze_version="v1",
        silver_version="v2",
        gold_version="v3",
        bronze_processing_method="incremental",
        silver_processing_method="full",
        gold_processing_method="delta",
        env_vars=env_vars,
    )
    base.update(overrides)
    return CorePipelineConfig(**base)


# --- Lake path generation ---


@pytest.mark.parametrize(
    "layer, expected",
    [
        ("bronze", "raw/bronze/finance/forecast/positions/v1/output/incremental"),
        ("silver", "raw/silver/finance/forecast/positions/v2/output/full"),
        ("gold", "raw/gold/finance/forecast/positions/v3/output/delta"),
    ],
)
def test_lake_path_with_container(layer, expected):
    cfg = make_config()
    assert cfg.get_lake_path(layer) == expected


@pytest.mark.parametrize(
    "layer, expected",
    [
        ("bronze", "bronze/finance/forecast/positions/v1/output/incremental"),
        ("silver", "silver/finance/forecast/positions/v2/output/full"),
        ("gold", "gold/finance/forecast/positions/v3/output/delta"),
    ],
)
def test_lake_path_without_container(layer, expected):
    """When container_name is omitted, layer acts as the path root."""
    cfg = make_config(container_name=None)
    assert cfg.get_lake_path(layer) == expected


@pytest.mark.parametrize("container_name", ["raw", None])
def test_lake_path_overrides(container_name):
    cfg = make_config(container_name=container_name)
    path = cfg.get_lake_path(
        "gold", processing_method_override="full", version_override="v9"
    )
    assert path.endswith("gold/finance/forecast/positions/v9/output/full")


@pytest.mark.parametrize("container_name", ["raw", None])
def test_work_path(container_name):
    cfg = make_config(container_name=container_name)
    path = cfg.get_work_path("bronze")
    assert path.endswith("bronze/finance/forecast/positions/v1/work")


# --- Validation rules ---


@pytest.mark.parametrize("container_name", ["raw", None])
def test_validate_rules_pass(container_name):
    cfg = make_config(container_name=container_name)
    assert cfg.validate_rules() is True


def test_validate_rules_fail_uppercase_domain():
    cfg = make_config(domain="Finance")
    with pytest.raises(ValueError, match="(?i)uppercase"):
        cfg.validate_rules()


@pytest.mark.parametrize("bad_version", ["version1", "v1rX"])
def test_validate_rules_fail_bad_version(bad_version):
    cfg = make_config(bronze_version=bad_version)
    with pytest.raises(ValueError):
        cfg.validate_rules()


def test_validate_rules_pass_revision_format():
    cfg = make_config(bronze_version="v1r2", silver_version="v10r0", gold_version="v3")
    assert cfg.validate_rules() is True


# --- Case fallback ---


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
