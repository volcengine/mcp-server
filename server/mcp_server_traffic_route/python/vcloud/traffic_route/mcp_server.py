from vcloud.traffic_route.api.api import TrafficRouteAPI
from mcp.server.fastmcp import FastMCP
from .note import note
from vcloud.utils.response import HandlerVolcResponse
import json


def create_mcp_server():
    service = TrafficRouteAPI()
    mcp = FastMCP(
        "TrafficRoute MCP",
        instructions="The DNS routing service that allows users to configure DNS routing rules to ensure that requests from clients reach the desired service nodes.",
    )

    @mcp.tool()
    def guide():
        """
        ## MCP Invocation Method Guide
        - For task decomposition, it is necessary to use the mcp tool.
        - The first step requires invoking the `get_note` function to obtain the parameter instructions.
        - Subsequently, the corresponding method should be called to retrieve the data.
        """
        return """use `guide` description to get how to use Mcp Server"""

    @mcp.tool()
    def get_note(func_name: str) -> str:
        """
        获取参数描述

        Args:
            func_name: The function name to get the description for.

        """
        return note.get(func_name)

    @mcp.tool()
    def list_zones() -> str:
        """
        本接口用于获取在 TrafficRoute 上的解析域名列表。
        Call steps:
        1. Pass "list_zones" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
        2. After obtaining the parameter instructions, invoke  list_zones
        """
        reqs = service.mcp_post("McpStartCloudServer", {}, json.dumps({}))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def create_zone() -> str:
        """
        本接口用于添加域名。
        Call steps:
        1. Pass "create_zone" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
        2. After obtaining the parameter instructions, invoke  create_zone
        """
        reqs = service.mcp_post("McpStartCloudServer", {}, json.dumps({}))

        return HandlerVolcResponse(reqs)

    # @mcp.tool()
    # def create_record() -> str:
    #     """
    #     本接口用于给指定域名增加解析记录。
    #     Call steps:
    #     1. Pass "create_record" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
    #     2. After obtaining the parameter instructions, invoke  create_record
    #     """
    #     reqs = service.mcp_post("McpStartCloudServer", {}, json.dumps({}))

    #     return HandlerVolcResponse(reqs)

    @mcp.tool()
    def list_records() -> str:
        """
        本接口用于获取域名的全部解析记录列表。
        Call steps:
        1. Pass "list_records" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
        2. After obtaining the parameter instructions, invoke  list_records
        """
        reqs = service.mcp_post("McpStartCloudServer", {}, json.dumps({}))

        return HandlerVolcResponse(reqs)