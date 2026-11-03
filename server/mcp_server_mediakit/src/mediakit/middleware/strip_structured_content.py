from __future__ import annotations

from collections.abc import Sequence

from fastmcp.server.middleware import Middleware, MiddlewareContext
from fastmcp.tools.base import Tool, ToolResult
from mcp.types import CallToolRequestParams, ListToolsRequest


class StripStructuredContentMiddleware(Middleware):
    """Avoid duplicating tool payloads as structuredContent + content text.

    MCP clients (Cursor / mcp.client.session) enforce: if tools/list advertises
    outputSchema, tools/call MUST return structuredContent. So stripping only
    structured_content breaks invocation. This middleware clears both:

    - on_list_tools: drop output_schema so clients do not require structuredContent
    - on_call_tool: drop structured_content so the wire result is content-only

    Setting meta on the ToolResult makes to_mcp_result() return CallToolResult and
    bypass server-side SDK validation (same pattern as ResponseLimitingMiddleware).

    Note: mediakit-cli schema projection that reads live MCP tools/list will no
    longer see outputSchema; projection from approved assets is unaffected.
    """

    async def on_list_tools(
        self,
        context: MiddlewareContext[ListToolsRequest],
        call_next,
    ) -> Sequence[Tool]:
        tools = await call_next(context)
        return [
            tool.model_copy(update={"output_schema": None})
            if tool.output_schema is not None
            else tool
            for tool in tools
        ]

    async def on_call_tool(
        self,
        context: MiddlewareContext[CallToolRequestParams],
        call_next,
    ) -> ToolResult:
        result = await call_next(context)
        if result.structured_content is None:
            return result

        update = {
            "structured_content": None,
            "meta": result.meta if result.meta is not None else {},
        }
        if hasattr(result, "model_copy"):
            return result.model_copy(update=update)

        stripped = ToolResult(
            content=result.content,
            structured_content=None,
            meta=update["meta"],
        )
        if hasattr(result, "is_error") and hasattr(stripped, "is_error"):
            try:
                setattr(stripped, "is_error", getattr(result, "is_error"))
            except (TypeError, ValueError, AttributeError):
                pass
        return stripped
