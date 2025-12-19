from src.mcdn.api.api import McdnAPI
from mcp.server.fastmcp import FastMCP
from .note import note
import json


def create_mcp_server():
    service = McdnAPI()
    mcp = FastMCP(
        "MCDN MCP",
        instructions="Volcengine(火山引擎) MCDN(多云CDN) MCP",
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
            func_name: 函数名

        """
        return note.get(func_name)

    @mcp.tool()
    def list_cloud_accounts(body: dict) -> str:
        """
        调用本接口获取您在多云CDN中管理的云服务商账号列表。
        Call steps:
        1. Pass "list_cloud_accounts" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  list_cloud_accounts
        """
        reqs = service.mcp_post("McpListCloudAccounts", {}, json.dumps(body))

        return reqs

    @mcp.tool()
    def list_cdn_domains(body: dict) -> str:
        """
        调用本接口获取加速域名列表。加速域名包含您添加到内置CDN加速的域名，以及从第三方云服务商平台同步的加速域名。
        Call steps:
        1. Pass "list_cdn_domains" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  list_cdn_domains
        """
        reqs = service.mcp_post("McpListCdnDomains", {}, json.dumps(body))

        return reqs

    @mcp.tool()
    def describe_cdn_domain_config(params: dict) -> str:
        """
        调用本接口获取域名详情。
        Call steps:
        1. Pass "describe_cdn_domain_config" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_cdn_domain_config
        """
        reqs = service.mcp_get("McpDescribeCdnDomainConfig", params, json.dumps({}))

        return reqs

    @mcp.tool()
    def describe_cdn_access_log(body: dict) -> str:
        """
        调用本接口向云服务商平台发起请求，查询指定加速域名的访问日志。
        Call steps:
        1. Pass "describe_cdn_access_log" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_cdn_access_log
        """
        reqs = service.mcp_post("McpDescribeCdnAccessLog", {}, json.dumps(body))

        return reqs

    @mcp.tool()
    def describe_cdn_region_and_isp() -> str:
        """
        调用本接口获取地区名称列表和运营商名称列表。
        使用数据中心接口查询部分统计数据时，您可以按照地区和运营商对数据进行筛选。
        Call steps:
        1. Pass "describe_cdn_region_and_isp" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_cdn_region_and_isp
        """
        reqs = service.mcp_post("McpDescribeCdnRegionAndIsp", {}, json.dumps({}))

        return reqs

    @mcp.tool()
    def describe_cdn_data_offline(body: dict) -> str:
        """
        调用本接口查询加速域名的边缘统计数据。
        Call steps:
        1. Pass "describe_cdn_data_offline" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_cdn_data_offline
        """
        reqs = service.mcp_post("McpDescribeCdnDataOffline", {}, json.dumps(body))

        return reqs

    @mcp.tool()
    def describe_cdn_origin_data_offline(body: dict) -> str:
        """
        调用本接口查询加速域名的回源统计数据。
        Call steps:
        1. Pass "describe_cdn_origin_data_offline" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_cdn_origin_data_offline
        """
        reqs = service.mcp_post("McpDescribeCdnOriginDataOffline", {}, json.dumps(body))

        return reqs

    return mcp
