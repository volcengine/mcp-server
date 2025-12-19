from src.alb.api.api import AlbAPI
from mcp.server.fastmcp import FastMCP
from .note import note
import json


def create_mcp_server():
    service = AlbAPI()
    mcp = FastMCP(
        "ALB MCP",
        instructions="火山引擎 应用型负载均衡 官方推出的 MCP Server，支持自然语言查询信息和分析数据。",
    )

    @mcp.tool()
    def guide():
        """
        ## MCP Invocation Method Guide
        - For task decomposition, it is necessary to use the mcp tool.
        - The first step requires invoking the `get_note` function to obtain the parameter instructions.
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
    def describe_acl_attributes(params: dict) -> str:
        """
        调用 DescribeAclAttributes 接口，查询指定访问控制策略组的详细信息。每秒最多提交 200 个 API 请求。
        Call steps:
        1. Pass "describe_acl_attributes" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
        2. After obtaining the parameter instructions, invoke  describe_acl_attributes
        """
        reqs = service.mcp_get("McpDescribeAclAttributes", params, json.dumps({}))

        return reqs

    @mcp.tool()
    def describe_ca_certificates(params: dict) -> str:
        """
        调用 DescribeCACertificates 接口，查询 CA 证书列表，单个账号每次最多查询 100 个 CA 证书。每秒最多提交 40 个 API 请求。
        Call steps:
        1. Pass "describe_ca_certificates" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
        2. After obtaining the parameter instructions, invoke  describe_ca_certificates
        """
        reqs = service.mcp_get("McpDescribeCACertificates", params, json.dumps({}))

        return reqs

    @mcp.tool()
    def describe_acls(params: dict) -> str:
        """
        调用 DescribeAcls 接口，查询访问控制策略组列表。调用一次接口最多可查询 100 个访问控制策略组。每秒最多提交 200 个 API 请求。
        Call steps:
        1. Pass "describe_acls" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
        2. After obtaining the parameter instructions, invoke  describe_acls
        """
        reqs = service.mcp_get("McpDescribeAcls", params, json.dumps({}))

        return reqs

    @mcp.tool()
    def describe_certificates(params: dict) -> str:
        """
        调用 DescribeCertificates 接口，查询服务器证书列表，单个账号每次最多查询100个证书。每秒最多提交 40 个 API 请求。
        Call steps:
        1. Pass "describe_certificates" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
        2. After obtaining the parameter instructions, invoke  describe_certificates
        """
        reqs = service.mcp_get("McpDescribeCertificates", params, json.dumps({}))

        return reqs

    @mcp.tool()
    def describe_customized_cfgs(params: dict) -> str:
        """
        调用 DescribeCustomizedCfgs 接口，查询个性化配置列表。每秒最多提交 40 个 API 请求。
        Call steps:
        1. Pass "describe_customized_cfgs" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
        2. After obtaining the parameter instructions, invoke  describe_customized_cfgs
        """
        reqs = service.mcp_get("McpDescribeCustomizedCfgs", params, json.dumps({}))

        return reqs

    @mcp.tool()
    def describe_all_certificates(params: dict) -> str:
        """
        调用 DescribeAllCertificates 接口，查询所有证书列表，单个账号每次最多查询100个证书。每秒最多提交 40 个 API 请求。
        Call steps:
        1. Pass "describe_all_certificates" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
        2. After obtaining the parameter instructions, invoke  describe_all_certificates
        """
        reqs = service.mcp_get("McpDescribeAllCertificates", params, json.dumps({}))

        return reqs

    @mcp.tool()
    def describe_listener_attributes(params: dict) -> str:
        """
        调用 DescribeListenerAttributes 接口，查询指定监听器的详细信息。每秒最多提交 200 个 API 请求。
        Call steps:
        1. Pass "describe_listener_attributes" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
        2. After obtaining the parameter instructions, invoke  describe_listener_attributes
        """
        reqs = service.mcp_get("McpDescribeListenerAttributes", params, json.dumps({}))

        return reqs

    @mcp.tool()
    def describe_listeners(params: dict) -> str:
        """
        调用 DescribeListeners 接口，查询监听器列表。每秒最多提交 200 个 API 请求。
        Call steps:
        1. Pass "describe_listeners" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
        2. After obtaining the parameter instructions, invoke  describe_listeners
        """
        reqs = service.mcp_get("McpDescribeListeners", params, json.dumps({}))

        return reqs

    @mcp.tool()
    def describe_load_balancer_attributes(params: dict) -> str:
        """
        调用 DescribeLoadBalancerAttributes 接口，查询 ALB 实例的详细信息。每秒最多提交 200 个 API 请求。
        Call steps:
        1. Pass "describe_load_balancer_attributes" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
        2. After obtaining the parameter instructions, invoke  describe_load_balancer_attributes
        """
        reqs = service.mcp_get(
            "McpDescribeLoadBalancerAttributes", params, json.dumps({})
        )

        return reqs

    @mcp.tool()
    def describe_customized_cfg_attributes(params: dict) -> str:
        """
        调用 DescribeCustomizedCfgAttributes 接口，查询指定个性化配置详细信息。每秒最多提交 40 个 API 请求。
        Call steps:
        1. Pass "describe_customized_cfg_attributes" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
        2. After obtaining the parameter instructions, invoke  describe_customized_cfg_attributes
        """
        reqs = service.mcp_get(
            "McpDescribeCustomizedCfgAttributes", params, json.dumps({})
        )

        return reqs

    @mcp.tool()
    def describe_health_check_templates(params: dict) -> str:
        """
        调用 DescribeHealthCheckTemplates 接口，获取健康检查模板列表。单次根据 ID 可查询的模板上限为 20 个。每秒最多提交 40 个 API 请求。
        Call steps:
        1. Pass "describe_health_check_templates" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
        2. After obtaining the parameter instructions, invoke  describe_health_check_templates
        """
        reqs = service.mcp_get(
            "McpDescribeHealthCheckTemplates", params, json.dumps({})
        )

        return reqs

    @mcp.tool()
    def describe_listener_health(params: dict) -> str:
        """
        调用 DescribeListenerHealth 接口，查询指定监听器关联后端服务器的健康检查信息。
        Call steps:
        1. Pass "describe_listener_health" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
        2. After obtaining the parameter instructions, invoke  describe_listener_health
        """
        reqs = service.mcp_get("McpDescribeListenerHealth", params, json.dumps({}))

        return reqs

    @mcp.tool()
    def describe_load_balancers(params: dict) -> str:
        """
        调用 DescribeLoadBalancers 接口，查询 ALB 实例列表。每秒最多提交 200 个 API 请求。
        Call steps:
        1. Pass "describe_load_balancers" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
        2. After obtaining the parameter instructions, invoke  describe_load_balancers
        """
        reqs = service.mcp_get("McpDescribeLoadBalancers", params, json.dumps({}))

        return reqs

    @mcp.tool()
    def describe_server_group_attributes(params: dict) -> str:
        """
        调用 DescribeServerGroupAttributes 接口，查询服务器组的详细信息。每秒最多提交 200 个 API 请求。
        Call steps:
        1. Pass "describe_server_group_attributes" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
        2. After obtaining the parameter instructions, invoke  describe_server_group_attributes
        """
        reqs = service.mcp_get(
            "McpDescribeServerGroupAttributes", params, json.dumps({})
        )

        return reqs

    @mcp.tool()
    def describe_rules(params: dict) -> str:
        """
        调用 DescribeRules 接口，获取指定监听器转发规则列表。每秒最多提交 40 个 API 请求。
        Call steps:
        1. Pass "describe_rules" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
        2. After obtaining the parameter instructions, invoke  describe_rules
        """
        reqs = service.mcp_get("McpDescribeRules", params, json.dumps({}))

        return reqs

    @mcp.tool()
    def describe_zones(params: dict) -> str:
        """
        调用 DescribeZones 接口，查询 ALB 支持部署的可用区列表。每秒最多提交 40 个 API 请求。
        Call steps:
        1. Pass "describe_zones" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
        2. After obtaining the parameter instructions, invoke  describe_zones
        """
        reqs = service.mcp_get("McpDescribeZones", params, json.dumps({}))

        return reqs

    @mcp.tool()
    def describe_server_groups(params: dict) -> str:
        """
        调用 DescribeServerGroups 接口，查询服务器组列表。每秒最多提交 200 个 API 请求。
        Call steps:
        1. Pass "describe_server_groups" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
        2. After obtaining the parameter instructions, invoke  describe_server_groups
        """
        reqs = service.mcp_get("McpDescribeServerGroups", params, json.dumps({}))

        return reqs

    @mcp.tool()
    def describe_server_group_backend_servers(params: dict) -> str:
        """
        调用 DescribeServerGroupBackendServers 接口，查询服务器组的后端服务器信息。每秒最多提交 200 个 API 请求。
        Call steps:
        1. Pass "describe_server_group_backend_servers" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
        2. After obtaining the parameter instructions, invoke  describe_server_group_backend_servers
        """
        reqs = service.mcp_get(
            "McpDescribeServerGroupBackendServers", params, json.dumps({})
        )

        return reqs

    return mcp
