import logging
import os

from typing import Any
from mcp.server.fastmcp import FastMCP
from mcp_server_na.common.client import NAClient
from mcp_server_na.common.config import NA_CONFIG

logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("NetworkAdvisor MCP Server", port=int(os.getenv("PORT", "8000")))

na_client = NAClient(NA_CONFIG.region, NA_CONFIG.host, NA_CONFIG.access_key, NA_CONFIG.secret_key)


@mcp.tool()
def create_diagnosis_instance(region: str, resource_type: str, resource_id: str) -> dict[str, Any]:
    """Create diagnosis instance"""
    return na_client.create_diagnosis_instance(region, resource_type, resource_id)


@mcp.tool()
def describe_diagnosis_instance_detail(diagnosis_instance_id: str) -> dict[str, Any]:
    """Describe diagnosis instance detail"""
    return na_client.describe_diagnosis_instance_detail(diagnosis_instance_id)
