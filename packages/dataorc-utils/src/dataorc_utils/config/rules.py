"""Rule framework for configuration validation.

Extensible mechanism for validating `CorePipelineConfig` objects. Each rule is a
callable taking (config, layer) and returning True or raising ValueError.

Built‑in rules:
- `lowercase_lake_path_rule`: lake paths must not contain uppercase letters.

Add new rules by appending to `RULES` or passing a custom list to
`run_rules_checks`.
"""
from __future__ import annotations

from typing import Callable, Iterable, List, TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from .models import CorePipelineConfig

RuleFunc = Callable[["CorePipelineConfig", str], bool]


def lowercase_lake_path_rule(config: "CorePipelineConfig", layer: str) -> bool:
    path = config.get_lake_path(layer)
    if any(ch.isalpha() and ch.isupper() for ch in path):
        raise ValueError(f"Lake path contains uppercase letters: '{path}'")
    return True


RULES: List[RuleFunc] = [lowercase_lake_path_rule]


def run_rules_checks(
    config: "CorePipelineConfig",
    layers: Iterable[str] | None = None,
    rules: Iterable[RuleFunc] | None = None,
) -> bool:
    if layers is None:
        layers = ("bronze", "silver", "gold")
    if rules is None:
        rules = RULES

    errors: list[str] = []
    for layer in layers:
        for rule in rules:
            try:
                rule(config, layer)
            except Exception as exc:  # noqa: BLE001
                errors.append(f"[{layer}] {exc}")

    if errors:
        raise ValueError("Rule checks failed:\n" + "\n".join(errors))
    return True


__all__ = [
    "RuleFunc",
    "RULES",
    "lowercase_lake_path_rule",
    "run_rules_checks",
]
