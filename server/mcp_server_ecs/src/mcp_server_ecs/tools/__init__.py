"""
Tool module initialization
"""

import os

from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "ECS MCP Server",
    host=os.getenv("MCP_SERVER_HOST", "127.0.0.1"),
    port=int(os.getenv("PORT", "8000")),
)
