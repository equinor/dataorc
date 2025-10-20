"""Rule framework for configuration validation.

Extensible mechanism for validating `CorePipelineConfig` objects. Each rule is a
callable taking (config, layer) and returning True or raising ValueError.

Built‑in rules:
- `lowercase_lake_path_rule`: lake paths must not contain uppercase letters.

Add new rules by appending to `RULES` or passing a custom list to
`run_rules_checks`.
"""
from __future__ import annotations

import re
from typing import TYPE_CHECKING, Callable, Iterable, List

if TYPE_CHECKING:  # pragma: no cover
    from .models import CorePipelineConfig

RuleFunc = Callable[["CorePipelineConfig", str], bool]


def lowercase_lake_path_rule(config: "CorePipelineConfig", layer: str) -> bool:
    path = config.get_lake_path(layer)
    if any(ch.isalpha() and ch.isupper() for ch in path):
        raise ValueError(f"Lake path contains uppercase letters: '{path}'")
    return True


_VERSION_PATTERN = re.compile(r"^v[0-9]+$")


def version_format_rule(config: "CorePipelineConfig", layer: str) -> bool:
    """Ensure the version segment for the layer matches pattern v<integer>.

    It derives the layer-specific version attribute (e.g. bronze_version) and validates
    it matches the required pattern. Also verifies that the lake path actually embeds
    that exact version token (defensive consistency check).
    """
    attr = f"{layer}_version"
    if not hasattr(config, attr):  # defensive: unknown layer
        return True
    value = getattr(config, attr)
    if not isinstance(value, str) or not _VERSION_PATTERN.match(value):
        raise ValueError(
            f"Version for layer '{layer}' must match pattern 'v<integer>' (e.g. v1); got: {value!r}"
        )
    path = config.get_lake_path(layer)
    # Ensure token boundary match in path
    if f"/{value}/" not in path:
        raise ValueError(
            f"Lake path for layer '{layer}' does not include expected version token '{value}': {path}"
        )
    return True


RULES: List[RuleFunc] = [lowercase_lake_path_rule, version_format_rule]


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
    "version_format_rule",
    "run_rules_checks",
]
