import logging
import os

from typing import Any
from mcp.server.fastmcp import Context, FastMCP
from mcp_server_vortexip.base.vortexip import VortexIPSDK

logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("VortexIP MCP Server", port=int(os.getenv("PORT", "8000")))

vortexip_resource = VortexIPSDK()


@mcp.tool()
def describe_vortex_ip_attributes(vortex_id: str = None) -> dict[str, Any]:
    """Describe VortexIP information"""

    req = {"vortex_id": vortex_id}
    resp = vortexip_resource.describe_vortex_ip_attributes(req)
    logger.info(f"Success to describe vortexip attributes {vortex_id}, {resp}")
    return resp.to_dict()


@mcp.tool()
def describe_web_scraper_attributes(web_scraper_id: str = None) -> dict[str, Any]:
    """Describe WebScraper information"""

    req = {"web_scraper_id": web_scraper_id}
    resp = vortexip_resource.describe_web_scraper_attributes(req)
    logger.info(f"Success to describe webscraper attributes {web_scraper_id}, {resp}")
    return resp.to_dict()
