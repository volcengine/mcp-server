from vcloud.veenedge.api.api import VeenedgeAPI
from mcp.server.fastmcp import FastMCP
from .note import note
from vcloud.utils.response import HandlerVolcResponse
import json


def create_mcp_server():
    service = VeenedgeAPI()
    mcp = FastMCP(
        "TrafficRoute MCP",
        description="The DNS routing service that allows users to configure DNS rules to ensure that requests from clients reach the desired service nodes.",
    )

    @mcp.tool()
    def guide():
        """
        ## MCP Invocation Method Guide
        - For task decomposition, it is necessary to use the mcp tool.
        - The first step requires invoking the `get_note` function to obtain the parameter description.
        - Subsequently, the corresponding method should be called to retrieve the data.
        """
        return """use  `guide` description to get how to use Mcp Server"""

    @mcp.tool()
    def get_note(func_name: str) -> str:
        """
        获取参数描述

        Args:
            func_name: The function name to get the description for.

        """
        return note.get(func_name)
