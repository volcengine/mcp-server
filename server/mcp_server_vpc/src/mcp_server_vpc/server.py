from mcp.server.fastmcp import FastMCP

from mcp_server_vpc.common import config

mcp = FastMCP(
    "vpc",
    host=config.VPCConfig().mcp_server_host,
    port=config.VPCConfig().mcp_server_port,
)
