from __future__ import annotations

import logging
from collections.abc import Sequence
from os import environ
from typing import Any

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.server import Context
from mcp.server.session import ServerSession
from mcp.types import ContentBlock
from starlette.requests import Request

from .constant import (
    MCP_DOMAINS_HEADER,
    MCP_TOOLS_HEADER,
    MCP_DOMAINS_ENV,
    MCP_TOOLS_ENV,
)

logger = logging.getLogger(__name__)


class BaseMCP(FastMCP):
    """MediaKit MCP Server 基类

    继承 FastMCP，提供：
    1. 工具分组过滤（list_tools 时按 domain/tool 过滤）
    2. 请求上下文获取（get_request_ctx）
    3. 在 call_tool 时将 client 实例注入 _base_mcp_store，供其动态获取当前请求凭证
    """

    def __init__(
        self,
        *,
        name: str | None = None,
        instructions: str | None = None,
        host: str = "0.0.0.0",
        port: int = 8000,
        streamable_http_path: str = "/mcp",
        stateless_http: bool = True,
    ):
        super().__init__(
            name=name,
            instructions=instructions,
            host=host,
            port=port,
            streamable_http_path=streamable_http_path,
            stateless_http=stateless_http,
        )
        self._base_mcp_store: dict[str, Any] = {}
        # domain -> set(tool_name) 的映射，由 register_categories 注册时填充
        self._domain_tools_map: dict[str, set[str]] = {}

    # ─── base_mcp_store 操作 ───────────────────────────

    def set_base_mcp_store(self, store: dict[str, Any]) -> dict[str, Any]:
        """合并设置 base_mcp_store"""
        self._base_mcp_store = {**self._base_mcp_store, **store}
        return self._base_mcp_store

    def get_base_mcp_store(self, key: str) -> Any:
        """获取 base_mcp_store 中的值"""
        if key is None:
            return None
        return self._base_mcp_store.get(key)

    # ─── domain_tools_map 操作 ─────────────────────────

    def register_domain_tools(self, domain: str, tool_names: list[str]) -> None:
        """注册 domain 及其对应的 tool 列表"""
        if domain not in self._domain_tools_map:
            self._domain_tools_map[domain] = set()
        self._domain_tools_map[domain].update(tool_names)
        logger.debug(f"Registered domain '{domain}' with tools: {tool_names}")

    def get_tool_domain(self, tool_name: str) -> str:
        """根据 tool_name 查找所属 domain"""
        for domain, tools in self._domain_tools_map.items():
            if tool_name in tools:
                return domain
        return ""

    # ─── 请求上下文 ────────────────────────────────────

    def get_request_ctx(self) -> Request | None:
        """获取当前 HTTP 请求的 Request 对象（Streamable HTTP 模式下）

        stdio 模式下返回 None。
        """
        try:
            ctx: Context[ServerSession, object] | None = self.get_context()
            if ctx and hasattr(ctx, "request_context") and ctx.request_context:
                raw_request: Request | None = ctx.request_context.request
                return raw_request
        except Exception as e:
            logger.debug(f"Failed to get request context: {e}")
        return None

    # ─── 工具过滤配置解析 ──────────────────────────────

    def _resolve_filter_config(self) -> tuple[set[str], set[str]]:
        """解析 domain / tool 过滤配置

        优先级：HTTP Header > 环境变量 > 无限制

        Returns:
            (allowed_domains, allowed_tools) — 空集合表示无限制
        """
        domains: set[str] = set()
        tools: set[str] = set()

        # 优先级1: HTTP Header（Streamable HTTP 模式）
        try:
            raw_request = self.get_request_ctx()
            if raw_request:
                headers = raw_request.headers
                domains_h = headers.get(MCP_DOMAINS_HEADER, "")
                tools_h = headers.get(MCP_TOOLS_HEADER, "")
                if domains_h:
                    domains = {item.strip() for item in domains_h.split(",") if item.strip()}
                if tools_h:
                    tools = {item.strip() for item in tools_h.split(",") if item.strip()}
                if domains or tools:
                    logger.debug(f"Filter from header: domains={domains}, tools={tools}")
                    return (domains, tools)
        except Exception as e:
            logger.debug(f"Failed to get filter from header: {e}")

        # 优先级2: 环境变量（Studio stdio 模式）
        domains_e = environ.get(MCP_DOMAINS_ENV, "")
        tools_e = environ.get(MCP_TOOLS_ENV, "")
        if domains_e:
            domains = {item.strip() for item in domains_e.split(",") if item.strip()}
        if tools_e:
            tools = {item.strip() for item in tools_e.split(",") if item.strip()}
        if domains or tools:
            logger.debug(f"Filter from env: domains={domains}, tools={tools}")
            return (domains, tools)

        # 无限制
        logger.debug("No filter configured, all tools allowed")
        return (domains, tools)

    # ─── list_tools 过滤 ───────────────────────────────

    async def list_tools(self):
        """获取可用工具列表，应用 domain / tool 过滤"""
        try:
            res = await super().list_tools()
            allowed_domains, allowed_tools = self._resolve_filter_config()

            # 无限制
            if not allowed_domains and not allowed_tools:
                return res

            filtered = []
            for tool in res:
                # 通过 _domain_tools_map 查找 tool 所属 domain
                tool_domain = self.get_tool_domain(tool.name)
                # shared 分组工具始终加载，不受过滤规则影响
                if tool_domain == "shared":
                    filtered.append(tool)
                    continue
                if allowed_domains and tool_domain not in allowed_domains:
                    continue
                if allowed_tools and tool.name not in allowed_tools:
                    continue
                filtered.append(tool)

            logger.info(
                f"BaseMCP.list_tools: filtered to {len(filtered)}/{len(res)} tools"
            )
            return filtered
        except Exception as e:
            logger.error(f"BaseMCP.list_tools failed: {e}")
            import traceback

            logger.error(traceback.format_exc())
            return []

    # ─── call_tool ─────────────────────────────────────

    async def call_tool(
        self,
        name: str,
        arguments: dict[str, Any],
    ) -> Sequence[ContentBlock] | dict[str, Any]:
        """Call a tool by name with arguments."""
        try:
            # 将当前 MCP 上下文注入 arguments，供 tool handler 使用
            ctx: Context[ServerSession, object] | None = self.get_context()
            arguments["ctx"] = ctx

            # 如果 store 中有 apiRequestInstance（client 实例），设置当前 tool name 到 header
            api_request_instance = self._base_mcp_store.get("apiRequestInstance")
            if api_request_instance and hasattr(api_request_instance, "set_headers") and name:
                api_request_instance.set_headers("x-tt-tools-name", name)

            return await super().call_tool(name, arguments)
        except Exception as e:
            logger.error(f"BaseMCP.call_tool failed with error: {e}")
            import traceback

            logger.error(traceback.format_exc())
            raise e
