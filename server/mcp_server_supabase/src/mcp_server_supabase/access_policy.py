import json
from dataclasses import dataclass
from typing import Any


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


@dataclass(frozen=True)
class ToolPolicy:
    feature: str
    scoped: bool


TOOL_POLICIES = {
    "list_workspaces": ToolPolicy("account", False),
    "get_workspace": ToolPolicy("account", True),
    "create_workspace": ToolPolicy("account", False),
    "pause_workspace": ToolPolicy("account", True),
    "restore_workspace": ToolPolicy("account", True),
    "execute_sql": ToolPolicy("database", True),
    "list_tables": ToolPolicy("database", True),
    "list_migrations": ToolPolicy("database", True),
    "list_extensions": ToolPolicy("database", True),
    "apply_migration": ToolPolicy("database", True),
    "get_workspace_url": ToolPolicy("development", True),
    "get_publishable_keys": ToolPolicy("development", True),
    "generate_typescript_types": ToolPolicy("development", True),
    "list_edge_functions": ToolPolicy("functions", True),
    "get_edge_function": ToolPolicy("functions", True),
    "deploy_edge_function": ToolPolicy("functions", True),
    "delete_edge_function": ToolPolicy("functions", True),
    "list_storage_buckets": ToolPolicy("storage", True),
    "create_storage_bucket": ToolPolicy("storage", True),
    "delete_storage_bucket": ToolPolicy("storage", True),
    "get_storage_config": ToolPolicy("storage", True),
    "list_branches": ToolPolicy("branching", True),
    "create_branch": ToolPolicy("branching", True),
    "delete_branch": ToolPolicy("branching", True),
    "reset_branch": ToolPolicy("branching", True),
}

ALL_TOOL_NAMES = frozenset(TOOL_POLICIES.keys())
FEATURE_TOOLS = {
    feature: frozenset(name for name, policy in TOOL_POLICIES.items() if policy.feature == feature)
    for feature in OFFICIAL_FEATURE_GROUPS
}
SCOPED_TOOL_NAMES = frozenset(name for name, policy in TOOL_POLICIES.items() if policy.scoped)


@dataclass(frozen=True)
class PartialAccessPolicy:
    workspace_ref: str | None = None
    features: frozenset[str] | None = None
    enabled_tools: frozenset[str] | None = None
    disabled_tools: frozenset[str] | None = None


@dataclass(frozen=True)
class ResolvedAccessPolicy:
    workspace_ref: str | None
    features: frozenset[str]
    enabled_tools: frozenset[str] | None
    disabled_tools: frozenset[str]


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


def _parse_query_name_set(params: Any, name: str) -> frozenset[str] | None:
    if params is None:
        return None
    values: list[str] = []
    if hasattr(params, "getlist"):
        values = [value for value in params.getlist(name) if value is not None]
    elif hasattr(params, "get"):
        value = params.get(name)
        if value is not None:
            values = [value]
    if not values:
        return None
    names: list[str] = []
    for value in values:
        names.extend(_expand_names(value))
    if not names:
        return frozenset()
    return frozenset(names)


def _parse_workspace_ref(value: Any) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError("workspace_ref must be a string")
    normalized = value.strip()
    if not normalized:
        return None
    return normalized


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


def build_partial_access_policy(
    workspace_ref: Any = None,
    features: Any = None,
    enabled_tools: Any = None,
    disabled_tools: Any = None,
) -> PartialAccessPolicy:
    return PartialAccessPolicy(
        workspace_ref=_parse_workspace_ref(workspace_ref),
        features=_validate_features(_parse_name_set(features)),
        enabled_tools=_validate_tools(_parse_name_set(enabled_tools), "enabled_tools"),
        disabled_tools=_validate_tools(_parse_name_set(disabled_tools), "disabled_tools"),
    )


def build_query_access_policy(params: Any) -> PartialAccessPolicy | None:
    if params is None:
        return None
    workspace_ref = _parse_workspace_ref(params.get("workspace_ref")) if hasattr(params, "get") else None
    features = _validate_features(_parse_query_name_set(params, "features"))
    enabled_tools = _validate_tools(_parse_query_name_set(params, "enabled_tools"), "enabled_tools")
    disabled_tools = _validate_tools(_parse_query_name_set(params, "disabled_tools"), "disabled_tools")
    if workspace_ref is None and features is None and enabled_tools is None and disabled_tools is None:
        return None
    return PartialAccessPolicy(
        workspace_ref=workspace_ref,
        features=features,
        enabled_tools=enabled_tools,
        disabled_tools=disabled_tools,
    )


def resolve_access_policy(
    server_policy: PartialAccessPolicy | None,
    request_policy: PartialAccessPolicy | None,
) -> ResolvedAccessPolicy:
    server_policy = server_policy or PartialAccessPolicy()
    request_policy = request_policy or PartialAccessPolicy()

    if server_policy.workspace_ref and request_policy.workspace_ref and server_policy.workspace_ref != request_policy.workspace_ref:
        raise ValueError("workspace_ref does not match the server scope")
    workspace_ref = server_policy.workspace_ref or request_policy.workspace_ref

    features = DEFAULT_FEATURE_GROUPS
    if server_policy.features is not None:
        features = server_policy.features
    if request_policy.features is not None:
        features = request_policy.features if server_policy.features is None else features & request_policy.features

    enabled_tools = server_policy.enabled_tools
    if request_policy.enabled_tools is not None:
        enabled_tools = request_policy.enabled_tools if enabled_tools is None else enabled_tools & request_policy.enabled_tools

    disabled_tools = frozenset()
    if server_policy.disabled_tools:
        disabled_tools |= server_policy.disabled_tools
    if request_policy.disabled_tools:
        disabled_tools |= request_policy.disabled_tools

    return ResolvedAccessPolicy(
        workspace_ref=workspace_ref,
        features=features,
        enabled_tools=enabled_tools,
        disabled_tools=disabled_tools,
    )


def resolve_allowed_tools(policy: ResolvedAccessPolicy) -> frozenset[str]:
    allowed = frozenset().union(*(FEATURE_TOOLS[feature] for feature in policy.features))
    if policy.workspace_ref:
        allowed -= FEATURE_TOOLS["account"]
    if policy.enabled_tools is not None:
        allowed &= policy.enabled_tools
    allowed -= policy.disabled_tools
    return allowed


def workspace_scope_schema(tool_name: str, input_schema: dict[str, Any], workspace_ref: str | None) -> dict[str, Any]:
    if not workspace_ref or tool_name not in SCOPED_TOOL_NAMES:
        return input_schema
    properties = dict(input_schema.get("properties", {}))
    properties.pop("workspace_id", None)
    result = dict(input_schema)
    result["properties"] = properties
    if "required" in result:
        result["required"] = [name for name in result.get("required", []) if name != "workspace_id"]
    return result
