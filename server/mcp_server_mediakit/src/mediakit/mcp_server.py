from __future__ import annotations

import importlib
import logging
import pkgutil

from base.client import MediKitClient

logger = logging.getLogger(__name__)


def register_categories(mcp, client: MediKitClient) -> None:
    """自动发现并注册 mcp_tools 下所有 domain 模块的 tool。

    遍历 mediakit.mcp_tools 包下所有模块，
    对每个含 register_tools 函数的模块调用注册，传入 mcp 和 client。
    模块需定义 TOOL_NAMES 列表，注册后通过 mcp.register_domain_tools 维护映射。
    """
    from . import mcp_tools as tools_pkg

    modules = sorted(pkgutil.iter_modules(tools_pkg.__path__), key=lambda item: item[1])
    for _, mod_name, is_pkg in modules:
        if is_pkg:
            continue
        try:
            module = importlib.import_module(f".{mod_name}", package=tools_pkg.__package__)
            if hasattr(module, "register_tools"):
                module.register_tools(mcp, client)

                # 注册 domain -> tools 映射
                if hasattr(mcp, "register_domain_tools") and hasattr(module, "TOOL_NAMES"):
                    mcp.register_domain_tools(mod_name, module.TOOL_NAMES)
        except Exception as exc:
            logger.exception("Failed to register MCP tools from module %s: %s", mod_name, exc)
