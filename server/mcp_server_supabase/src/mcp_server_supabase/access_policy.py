import json
from dataclasses import dataclass
from typing import Any

from .tool_registry import TOOL_DEFINITIONS

OFFICIAL_FEATURE_GROUPS = (
    "account",
    "docs",
    "database",
    "debugging",
    "development",
    "functions",
    "storage",
    "branching",
)
DEFAULT_FEATURE_GROUPS = frozenset({
    "account",
    "database",
    "debugging",
    "development",
    "docs",
    "functions",
    "branching",
})

ALL_TOOL_NAMES = frozenset(tool.name for tool in TOOL_DEFINITIONS)
FEATURE_TOOLS = {
    feature: frozenset(tool.name for tool in TOOL_DEFINITIONS if tool.feature == feature)
    for feature in OFFICIAL_FEATURE_GROUPS
}
SCOPED_TOOL_NAMES = frozenset(tool.name for tool in TOOL_DEFINITIONS if tool.scoped)
MUTATING_TOOL_NAMES = frozenset(tool.name for tool in TOOL_DEFINITIONS if tool.mutating)


@dataclass(frozen=True)
class AccessPolicy:
    workspace_ref: str | None = None
    features: frozenset[str] = DEFAULT_FEATURE_GROUPS
    read_only: bool = False
    disabled_tools: frozenset[str] = frozenset()


def _normalize_name(value: Any) -> str:
    if not isinstance(value, str):
        raise ValueError("Expected string value")
    normalized = value.strip()
    if not normalized:
        raise ValueError("Value cannot be empty")
    return normalized


def _expand_names(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return []
        if text.startswith("["):
            parsed = json.loads(text)
            if not isinstance(parsed, list):
                raise ValueError("Expected a JSON array")
            return [_normalize_name(item) for item in parsed]
        return [_normalize_name(item) for item in text.split(",") if item.strip()]
    if isinstance(value, (list, tuple, set, frozenset)):
        return [_normalize_name(item) for item in value]
    raise ValueError("Unsupported value type")


def _parse_name_set(value: Any) -> frozenset[str] | None:
    names = _expand_names(value)
    if not names:
        return None
    return frozenset(names)


def _parse_workspace_ref(value: Any) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError("workspace_ref must be a string")
    normalized = value.strip()
    if not normalized:
        return None
    if normalized.startswith("br-"):
        raise ValueError("workspace_ref must be a workspace ID; branch IDs are not supported")
    return normalized


def _parse_read_only(value: Any) -> bool | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if not isinstance(value, str):
        raise ValueError("read_only must be a boolean")
    normalized = value.strip().lower()
    if not normalized:
        return None
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise ValueError("read_only must be true or false")


def _validate_features(features: frozenset[str] | None) -> frozenset[str] | None:
    if features is None:
        return None
    invalid = sorted(features - set(OFFICIAL_FEATURE_GROUPS))
    if invalid:
        raise ValueError(f"Unsupported features: {', '.join(invalid)}")
    return features


def _validate_tools(tools: frozenset[str] | None, field_name: str) -> frozenset[str] | None:
    if tools is None:
        return None
    invalid = sorted(tools - ALL_TOOL_NAMES)
    if invalid:
        raise ValueError(f"Unsupported {field_name}: {', '.join(invalid)}")
    return tools


def build_access_policy(
    workspace_ref: Any = None,
    features: Any = None,
    read_only: Any = None,
    disabled_tools: Any = None,
) -> AccessPolicy:
    return AccessPolicy(
        workspace_ref=_parse_workspace_ref(workspace_ref),
        features=_validate_features(_parse_name_set(features)) or DEFAULT_FEATURE_GROUPS,
        read_only=bool(_parse_read_only(read_only)),
        disabled_tools=_validate_tools(_parse_name_set(disabled_tools), "disabled_tools") or frozenset(),
    )


def resolve_allowed_tools(policy: AccessPolicy) -> frozenset[str]:
    allowed = frozenset().union(*(FEATURE_TOOLS[feature] for feature in policy.features))
    if policy.workspace_ref:
        allowed -= FEATURE_TOOLS["account"]
    if policy.read_only:
        allowed -= MUTATING_TOOL_NAMES
    allowed -= policy.disabled_tools
    return allowed


def workspace_scope_schema(tool_name: str, input_schema: dict[str, Any], workspace_ref: str | None) -> dict[str, Any]:
    if tool_name not in SCOPED_TOOL_NAMES:
        return input_schema
    result = dict(input_schema)
    properties = dict(input_schema.get("properties", {}))
    result["properties"] = properties
    required = [name for name in result.get("required", []) if name != "workspace_id"]
    if workspace_ref:
        properties.pop("workspace_id", None)
        if required:
            result["required"] = required
        elif "required" in result:
            result.pop("required", None)
        return result
    if "workspace_id" in properties and "workspace_id" not in required:
        required.append("workspace_id")
    if required:
        result["required"] = required
    return result
