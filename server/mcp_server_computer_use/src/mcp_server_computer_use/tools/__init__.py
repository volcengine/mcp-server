import os
from mcp.server.fastmcp import FastMCP

MCP = FastMCP(name="computer_use", port=int(
    os.getenv("MCP_SERVER_PORT", "8000")))
