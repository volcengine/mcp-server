from __future__ import annotations

import importlib
import logging
import pkgutil

logger = logging.getLogger(__name__)

_registered_mcp_ids: set[int] = set()


def register_categories(mcp) -> None:
    """自动发现并注册 mcp_tools 下所有 domain 模块的 tool。"""
    mcp_id = id(mcp)
    if mcp_id in _registered_mcp_ids:
        return

    from . import mcp_tools as tools_pkg
    from base.registry import register_domain_tools

    modules = sorted(pkgutil.iter_modules(tools_pkg.__path__), key=lambda item: item[1])
    for _, mod_name, is_pkg in modules:
        if is_pkg:
            continue
        try:
            module = importlib.import_module(f".{mod_name}", package=tools_pkg.__package__)
            if hasattr(module, "register_tools"):
                module.register_tools(mcp)
                if hasattr(module, "TOOL_NAMES"):
                    domain = getattr(module, "DOMAIN", mod_name)
                    register_domain_tools(domain, module.TOOL_NAMES)
        except Exception as exc:
            logger.exception(
                "Failed to register MCP tools from module %s: %s", mod_name, exc
            )

    _registered_mcp_ids.add(mcp_id)
