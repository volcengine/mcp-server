from src.dcdn.api.api import DcdnAPI
from mcp.server.fastmcp import FastMCP
from .note import note
from src.utils.response import HandlerVolcResponse
import json


def create_mcp_server():
    service = DcdnAPI()
    mcp = FastMCP(
        "IGA MCP",
        instructions="Volcengine(火山引擎) IGA(智能全球加速) MCP，提供智能全球加速相关服务",
    )

    @mcp.tool()
    def guide():
        """
        ## MCP Invocation Method Guide
        - For task decomposition, it is necessary to use the mcp tool.
        - The first step requires invoking the `get_note` function to obtain the parameter description.
        - Subsequently, the corresponding method should be called to retrieve the data.
        """
        return """use  `guide` instructions to get how to use Mcp Server"""

    @mcp.tool()
    def get_note(func_name: str) -> str:
        """
        获取参数描述

        Args:
            func_name: 函数名

        """
        return note.get(func_name)

    @mcp.tool()
    def list_domain_config(body: dict) -> str:
        """
        批量查询全站加速的域名配置信息。
        Call steps:
        1. Pass "list_domain_config" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  list_domain_config
        """
        reqs = service.mcp_post("McpListDomainConfig", {}, json.dumps(body))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def describe_dcdn_region_and_isp(body: dict) -> str:
        """
        查询地域和运营商信息
        Call steps:
        1. Pass "describe_dcdn_region_and_isp" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_dcdn_region_and_isp
        """
        reqs = service.mcp_post("McpDescribeDcdnRegionAndIsp", {}, json.dumps(body))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def describe_domain_isp_data(body: dict) -> str:
        """
        查询运营商分布统计数据
        Call steps:
        1. Pass "describe_domain_isp_data" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_domain_isp_data
        """
        reqs = service.mcp_post("McpDescribeDomainIspData", {}, json.dumps(body))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def describe_domain_pv_data(body: dict) -> str:
        """
        查询PV统计数据
        Call steps:
        1. Pass "describe_domain_pv_data" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_domain_pv_data
        """
        reqs = service.mcp_post("McpDescribeDomainPVData", {}, json.dumps(body))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def describe_domain_uv_data(body: dict) -> str:
        """
        查询UV统计数据
        Call steps:
        1. Pass "describe_domain_uv_data" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_domain_uv_data
        """
        reqs = service.mcp_post("McpDescribeDomainUVData", {}, json.dumps(body))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def describe_origin_statistics_detail(body: dict) -> str:
        """
        查询访问回源资源用量细节
        Call steps:
        1. Pass "describe_origin_statistics_detail" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_origin_statistics_detail
        """
        reqs = service.mcp_post(
            "McpDescribeOriginStatisticsDetail", {}, json.dumps(body)
        )

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def describe_origin_statistics(body: dict) -> str:
        """
        查询回源资源用量
        Call steps:
        1. Pass "describe_origin_statistics" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_origin_statistics
        """
        reqs = service.mcp_post("McpDescribeOriginStatistics", {}, json.dumps(body))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def describe_top_domains(body: dict) -> str:
        """
        查询域名排行统计数据
        Call steps:
        1. Pass "describe_top_domains" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_top_domains
        """
        reqs = service.mcp_post("McpDescribeTopDomains", {}, json.dumps(body))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def describe_top_i_ps(body: dict) -> str:
        """
        查询IP排行统计数据
        Call steps:
        1. Pass "describe_top_i_ps" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_top_i_ps
        """
        reqs = service.mcp_post("McpDescribeTopIPs", {}, json.dumps(body))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def describe_top_referers(body: dict) -> str:
        """
        查询Referer排行统计数据
        Call steps:
        1. Pass "describe_top_referers" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_top_referers
        """
        reqs = service.mcp_post("McpDescribeTopReferers", {}, json.dumps(body))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def describe_top_urls(body: dict) -> str:
        """
        查询URL排行统计数据
        Call steps:
        1. Pass "describe_top_urls" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_top_urls
        """
        reqs = service.mcp_post("McpDescribeTopUrls", {}, json.dumps(body))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def list_cert(body: dict) -> str:
        """
        API描述
        API名称：ListCert。
        API域名：open.volcengineapi.com。
        API描述：查询用户在火山平台拥有的证书。
        Call steps:
        1. Pass "list_cert" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  list_cert
        """
        reqs = service.mcp_post("McpListCert", {}, json.dumps(body))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def list_cert_bind(body: dict) -> str:
        """
        API描述
        API名称：ListCertBind。
        API域名：open.volcengineapi.com。
        API描述：查询证书绑定关系。
        Call steps:
        1. Pass "list_cert_bind" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  list_cert_bind
        """
        reqs = service.mcp_post("McpListCertBind", {}, json.dumps(body))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def describe_domain_region_data(body: dict) -> str:
        """
        查询域名的区域分布统计数据。
        Call steps:
        1. Pass "describe_domain_region_data" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_domain_region_data
        """
        reqs = service.mcp_post("McpDescribeDomainRegionData", {}, json.dumps(body))

        return HandlerVolcResponse(reqs)

    return mcp
