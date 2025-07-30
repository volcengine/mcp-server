import inspect
from pydantic.networks import AnyUrl
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.resources import FunctionResource
from mcp_server_tls.config import TLS_CONFIG
from mcp_server_tls.tools import SUPPORT_TOOLS
from mcp_server_tls.resources import SUPPORT_RESOURCES

# Initialize FastMCP server
mcp = FastMCP(
    "TLS MCP Server",
    dependencies=["env", "volcengine"],
    port=int(TLS_CONFIG.mcp_port),
    host=TLS_CONFIG.mcp_host,
)

def add_resources_to_mcp(mcp):
    """加载mcp resource"""
    for resource_name, resource_info in SUPPORT_RESOURCES.items():

        fn = resource_info.get("fn")
        uri = "https://tls-{Region}.ivolces.com" + resource_info.get("uri")
        description = resource_info.get("description", None)
        mime_type = resource_info.get("mime_type", None)

        # Check if this should be a template
        has_uri_params = "{" in uri and "}" in uri
        has_func_params = bool(inspect.signature(fn).parameters)

        if has_uri_params or has_func_params:
            # Validate that URI params match function params
            # uri_params = set(re.findall(r"{(\w+)}", uri))
            # func_params = set(inspect.signature(fn).parameters.keys())

            # if uri_params != func_params:
            #     raise ValueError(
            #         f"Mismatch between URI parameters {uri_params} "
            #         f"and function parameters {func_params}"
            #     )

            # Register as template
            mcp._resource_manager.add_template(
                fn=fn,
                uri_template=uri,
                name=resource_name,
                description=description,
                mime_type=mime_type or "text/plain",
            )
        else:
            # Register as regular resource
            resource = FunctionResource(
                uri=AnyUrl(uri),
                name=resource_name,
                description=description,
                mime_type=mime_type or "text/plain",
                fn=fn,
            )
            mcp.add_resource(resource)


def add_tools_to_mcp(mcp):
    # 加载mcp tools
    enabled_tools = TLS_CONFIG.enabled_tools
    if not enabled_tools or (len(enabled_tools) == 1 and enabled_tools[0] == "all"):
        for tool_name, tool_func in SUPPORT_TOOLS.items():
            mcp.add_tool(tool_func, tool_name)
    else:
        for tool_name in enabled_tools:
            if tool_name in SUPPORT_TOOLS:
                mcp.add_tool(SUPPORT_TOOLS.get(tool_name), tool_name)


add_resources_to_mcp(mcp)
add_tools_to_mcp(mcp)
