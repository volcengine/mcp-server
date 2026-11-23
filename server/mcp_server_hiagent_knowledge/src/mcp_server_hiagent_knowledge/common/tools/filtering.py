"""Tool-scope filtering for the HiAgent Knowledge MCP server.

A deployment may only want a subset of the tools exposed (e.g. restrict a host
to the Wiki tools so the agent reliably searches the Wiki). This module resolves
which tool names stay enabled from an optional allowlist and denylist; the server
registers every tool and then removes the ones this resolver excludes.

Both filters take exact tool names (comma-separated on the CLI / environment):
- allowlist selects the base set (``None`` / empty means "all tools");
- denylist is then subtracted from that base set.

Unknown names are rejected so a typo fails fast instead of silently doing
nothing.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence


def parse_tool_list(raw: str | None) -> list[str] | None:
    """Parse a comma-separated tool list from a CLI value / environment variable.

    Returns ``None`` when the value carries no tool names — argument omitted, or a
    string that is empty / whitespace / only separators (e.g. ``HIAGENT_TOOLS=``).
    This maps "no meaningful value" to "no restriction" (all tools), matching the
    documented "unset = all tools" behaviour and avoiding an empty environment
    variable silently narrowing the tool set. Surrounding whitespace is trimmed
    and blank entries are dropped.
    """

    if raw is None:
        return None
    names = [name.strip() for name in raw.split(",")]
    names = [name for name in names if name]
    return names or None


def resolve_enabled_tools(
    all_tools: Sequence[str],
    *,
    enabled: Iterable[str] | None = None,
    disabled: Iterable[str] | None = None,
    always_on: Iterable[str] = (),
) -> list[str]:
    """Resolve the enabled tool names from an allowlist and denylist.

    - ``enabled`` (allowlist) picks the base set; ``None`` means all tools.
    - ``disabled`` (denylist) is subtracted from the base set.
    - ``always_on`` names are tools the server keeps regardless of the filter
      (e.g. ``health_check``). They are accepted as valid names in either filter
      so a user can list one without error, but they are not part of ``all_tools``
      and never appear in the returned base set (the server adds them back).

    The returned list preserves ``all_tools`` order. Raises ``ValueError`` listing
    every unknown name found in either filter (so a typo fails fast).
    """

    known = set(all_tools)
    always_on_set = set(always_on)

    enabled_set = set(enabled) if enabled is not None else None
    disabled_set = set(disabled or ())

    # ``always_on`` names are valid input even though they are filtered out of the
    # base set: the server keeps them unconditionally, so listing one must not error.
    unknown = sorted(((enabled_set or set()) | disabled_set) - known - always_on_set)
    if unknown:
        message = (
            "unknown tool name(s): "
            + ", ".join(unknown)
            + "; known tools: "
            + ", ".join(all_tools)
        )
        if always_on_set:
            message += (
                "; always kept (no need to list): "
                + ", ".join(sorted(always_on_set))
            )
        raise ValueError(message)

    base = list(all_tools) if enabled_set is None else [
        name for name in all_tools if name in enabled_set
    ]
    return [name for name in base if name not in disabled_set]
