from src.ga.api.api import GaAPI
from mcp.server.fastmcp import FastMCP
from .note import note
import json


def create_mcp_server():
    service = GaAPI()
    mcp = FastMCP(
        "GA MCP",
        description="Volcengine(火山引擎)全球加速 GA MCP，提供全球加速相关服务",
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
    def describe_accelerator(params: dict, body: dict) -> str:
        """
        查询标准型加速器详情
        Call steps:
        1. Pass "describe_accelerator" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_accelerator
        """
        reqs = service.mcp_post("McpDescribeAccelerator", params, json.dumps(body))

        return reqs

    @mcp.tool()
    def describe_basic_accelerator(params: dict, body: dict) -> str:
        """
        查询基础型加速器详情
        Call steps:
        1. Pass "describe_basic_accelerator" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_basic_accelerator
        """
        reqs = service.mcp_post("McpDescribeBasicAccelerator", params, json.dumps(body))

        return reqs

    @mcp.tool()
    def describe_basic_endpoint_group(params: dict, body: dict) -> str:
        """
        查询终端节点组详情
        Call steps:
        1. Pass "describe_basic_endpoint_group" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_basic_endpoint_group
        """
        reqs = service.mcp_post(
            "McpDescribeBasicEndpointGroup", params, json.dumps(body)
        )

        return reqs

    @mcp.tool()
    def describe_basic_ip_set(params: dict, body: dict) -> str:
        """
        查询基础型加速器加速区域详情
        Call steps:
        1. Pass "describe_basic_ip_set" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_basic_ip_set
        """
        reqs = service.mcp_post("McpDescribeBasicIPSet", params, json.dumps(body))

        return reqs

    @mcp.tool()
    def describe_endpoint_group(params: dict, body: dict) -> str:
        """
        查询终端节点组
        Call steps:
        1. Pass "describe_endpoint_group" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_endpoint_group
        """
        reqs = service.mcp_post("McpDescribeEndpointGroup", params, json.dumps(body))

        return reqs

    @mcp.tool()
    def describe_ip_set(params: dict, body: dict) -> str:
        """
        查询加速区域
        Call steps:
        1. Pass "describe_ip_set" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_ip_set
        """
        reqs = service.mcp_post("McpDescribeIPSet", params, json.dumps(body))

        return reqs

    @mcp.tool()
    def describe_listener(params: dict, body: dict) -> str:
        """
        查询监听器配置详情。
        Call steps:
        1. Pass "describe_listener" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_listener
        """
        reqs = service.mcp_post("McpDescribeListener", params, json.dumps(body))

        return reqs

    @mcp.tool()
    def describe_statistics(params: dict, body: dict) -> str:
        """
        查询全球加速监控数据
        Call steps:
        1. Pass "describe_statistics" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_statistics
        """
        reqs = service.mcp_post("McpDescribeStatistics", params, json.dumps(body))

        return reqs

    @mcp.tool()
    def get_accelerator_dimension(params: dict, body: dict) -> str:
        """
        获取加速器维度信息
        Call steps:
        1. Pass "get_accelerator_dimension" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  get_accelerator_dimension
        """
        reqs = service.mcp_post("McpGetAcceleratorDimension", params, json.dumps(body))

        return reqs

    @mcp.tool()
    def get_bandwidth_package(params: dict, body: dict) -> str:
        """
        带宽包详情
        Call steps:
        1. Pass "get_bandwidth_package" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  get_bandwidth_package
        """
        reqs = service.mcp_post("McpGetBandwidthPackage", params, json.dumps(body))

        return reqs

    @mcp.tool()
    def list_accelerators(params: dict, body: dict) -> str:
        """
        列举加速实例
        Call steps:
        1. Pass "list_accelerators" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  list_accelerators
        """
        reqs = service.mcp_post("McpListAccelerators", params, json.dumps(body))

        return reqs

    @mcp.tool()
    def list_bandwidth_packages(params: dict, body: dict) -> str:
        """
        带宽包列表
        Call steps:
        1. Pass "list_bandwidth_packages" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  list_bandwidth_packages
        """
        reqs = service.mcp_post("McpListBandwidthPackages", params, json.dumps(body))

        return reqs

    @mcp.tool()
    def list_basic_accelerate_i_ps(params: dict, body: dict) -> str:
        """
        拉取基础型加速器加速IP列表
        Call steps:
        1. Pass "list_basic_accelerate_i_ps" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  list_basic_accelerate_i_ps
        """
        reqs = service.mcp_post("McpListBasicAccelerateIPs", params, json.dumps(body))

        return reqs

    @mcp.tool()
    def list_basic_accelerators(params: dict, body: dict) -> str:
        """
        查询基础型加速器列表
        Call steps:
        1. Pass "list_basic_accelerators" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  list_basic_accelerators
        """
        reqs = service.mcp_post("McpListBasicAccelerators", params, json.dumps(body))

        return reqs

    @mcp.tool()
    def list_basic_endpoint_groups(params: dict, body: dict) -> str:
        """
        获取基础型加速器终端节点组列表
        Call steps:
        1. Pass "list_basic_endpoint_groups" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  list_basic_endpoint_groups
        """
        reqs = service.mcp_post("McpListBasicEndpointGroups", params, json.dumps(body))

        return reqs

    @mcp.tool()
    def list_basic_endpoints(params: dict, body: dict) -> str:
        """
        拉取基础型加速器终端节点
        Call steps:
        1. Pass "list_basic_endpoints" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  list_basic_endpoints
        """
        reqs = service.mcp_post("McpListBasicEndpoints", params, json.dumps(body))

        return reqs

    @mcp.tool()
    def list_basic_ip_sets(params: dict, body: dict) -> str:
        """
        获取基础型加速区域列表
        Call steps:
        1. Pass "list_basic_ip_sets" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  list_basic_ip_sets
        """
        reqs = service.mcp_post("McpListBasicIPSets", params, json.dumps(body))

        return reqs

    @mcp.tool()
    def list_endpoint_groups(params: dict, body: dict) -> str:
        """
        列举终端节点组
        Call steps:
        1. Pass "list_endpoint_groups" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  list_endpoint_groups
        """
        reqs = service.mcp_post("McpListEndpointGroups", params, json.dumps(body))

        return reqs

    @mcp.tool()
    def list_listeners(params: dict, body: dict) -> str:
        """
        查询标准型加速器上的所有监听器的配置详情。
        Call steps:
        1. Pass "list_listeners" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  list_listeners
        """
        reqs = service.mcp_post("McpListListeners", params, json.dumps(body))

        return reqs

    return mcp
