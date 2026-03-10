from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.exceptions import ToolError
from mcp.types import Tool as MCPTool

from .access_policy import (
    PartialAccessPolicy,
    SCOPED_TOOL_NAMES,
    resolve_access_policy,
    resolve_allowed_tools,
    workspace_scope_schema,
)


class ScopedFastMCP(FastMCP):
    def __init__(self, *args, access_policy: PartialAccessPolicy | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        self._access_policy = access_policy or PartialAccessPolicy()

    def _resolve_current_policy(self):
        return resolve_access_policy(self._access_policy)

    async def list_tools(self):
        policy = self._resolve_current_policy()
        allowed_tools = resolve_allowed_tools(policy)
        tools = await super().list_tools()
        visible_tools = []
        for tool in tools:
            if tool.name not in allowed_tools:
                continue
            scoped_schema = workspace_scope_schema(tool.name, tool.inputSchema, policy.workspace_ref)
            if scoped_schema is tool.inputSchema:
                visible_tools.append(tool)
                continue
            payload = tool.model_dump(exclude_none=False)
            payload["inputSchema"] = scoped_schema
            visible_tools.append(MCPTool(**payload))
        return visible_tools

    async def call_tool(self, name: str, arguments: dict[str, object]):
        policy = self._resolve_current_policy()
        allowed_tools = resolve_allowed_tools(policy)
        if name not in allowed_tools:
            raise ToolError(f"Tool '{name}' is not available for the current connection")

        effective_arguments = dict(arguments or {})
        if policy.workspace_ref and name in SCOPED_TOOL_NAMES:
            provided_workspace_id = effective_arguments.get("workspace_id")
            if provided_workspace_id not in {None, "", policy.workspace_ref}:
                raise ToolError("workspace_id is outside the current workspace_ref scope")
            effective_arguments["workspace_id"] = policy.workspace_ref

        return await super().call_tool(name, effective_arguments)
