"""通用 MCP Schema 兼容：内联本地引用，不依赖特定客户端。"""

import json

import jsonref
from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from mcp.types import CallToolResult, TextContent
from pydantic import ValidationError

from .observability import observe_call


def _reject_external_reference(uri):
    raise ValueError("工具 Schema 不允许读取外部引用")


def inline_schema(schema: dict) -> dict:
    """展开生成模型的本地引用，保留实际 JSON Schema 约束。"""
    resolved = jsonref.replace_refs(
        schema, proxies=False, lazy_load=False, merge_props=True, loader=_reject_external_reference
    )
    # JSON 编码同时拒绝递归结构；这些结构无法用有限内联 Schema 表达。
    resolved = json.loads(json.dumps(resolved))

    def clean(value):
        if isinstance(value, dict):
            return {
                key: clean(item)
                for key, item in value.items()
                if key not in {"$defs", "definitions", "discriminator"}
            }
        if isinstance(value, list):
            return [clean(item) for item in value]
        return value

    return clean(resolved)


class SmsAPIError(ToolError):
    """SmsAPIError 保留原始结构化失败，供协议和观测边界共同消费。"""

    def __init__(self, result: dict):
        self.result = result
        super().__init__(json.dumps(result, ensure_ascii=False))


class SmsMCPServer(MCPServer):
    """SmsMCPServer 在协议出口提供可直接消费的内联工具定义。"""

    async def list_tools(self):
        tools = await super().list_tools()
        return [
            tool.model_copy(
                update={
                    "input_schema": inline_schema(tool.input_schema),
                    "output_schema": (
                        inline_schema(tool.output_schema)
                        if tool.output_schema is not None
                        else None
                    ),
                }
            )
            for tool in tools
        ]

    async def call_tool(self, name, arguments, context=None):
        with observe_call("tool", name) as observation:
            try:
                result = await super().call_tool(name, arguments, context)
            except ToolError as exc:
                if isinstance(exc.__cause__, SmsAPIError):
                    failure = exc.__cause__.result
                    observation.record(failure)
                    return CallToolResult(
                        content=[TextContent(type="text", text=json.dumps(failure, ensure_ascii=False))],
                        structured_content=failure,
                        is_error=True,
                    )
                if isinstance(exc.__cause__, ValidationError):
                    observation.result_class = "failed"
                    observation.error_code = "invalid_arguments"
                    # 未知字段的最后一段是调用方提供的键，也可能是误填的私密数据。
                    errors = [
                        {
                            "field": list(
                                error["loc"][:-1]
                                if error["type"] == "extra_forbidden" else error["loc"]
                            ),
                            "type": error["type"],
                        }
                        for error in exc.__cause__.errors(
                            include_input=False, include_context=False
                        )
                    ]
                    failure = {
                        "success": False, "action": name, "request_id": None, "result": None,
                        "error": {"code": "invalid_arguments", "message": "参数校验未通过，请检查表单", "outcome_unknown": False, "fields": errors},
                    }
                    return CallToolResult(
                        content=[TextContent(type="text", text=json.dumps(failure, ensure_ascii=False))],
                        structured_content=failure,
                        is_error=True,
                    )
                raise
            observation.record(result.structured_content)
            return result
