from src.ESCloud.api.api import EscloudAPI
from mcp.server.fastmcp import FastMCP
from .note import note
import json
import os


def create_mcp_server():
    service = EscloudAPI()
    mcp = FastMCP(
        name="escloud-mcp-server",
        host=os.getenv("MCP_SERVER_HOST", "0.0.0.0"),
        port=int(os.getenv("MCP_SERVER_PORT", "8000")),
        stateless_http=os.getenv("STATLESS_HTTP", "true").lower() == "true",
        streamable_http_path=os.getenv("STREAMABLE_HTTP_PATH", "/mcp"),
        instructions="""
      ## MCP Invocation Method Guide
      - For task decomposition, it is necessary to use the mcp tool.
      - The first step requires invoking the `get_note` function to obtain the parameter description.
      - Subsequently, the corresponding method should be called to retrieve the data.
        Before calling the method, please first execute `get_note` to obtain the parameter description.
      """,
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
    def describe_zones(body: dict) -> str:
        """
        查询可用区列表
        Call steps:
        1. Pass "describe_zones" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_zones
        """
        reqs = service.mcp_post("Es_cloudMcpDescribeZones", {}, json.dumps(body))

        return reqs

    @mcp.tool()
    def describe_instances(body: dict) -> str:
        """
        查询云搜索实例列表，以及实例配置详情
        Call steps:
        1. Pass "describe_instances" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_instances
        """
        reqs = service.mcp_post("Es_cloudMcpDescribeInstances", {}, json.dumps(body))

        return reqs

    @mcp.tool()
    def create_instance_in_one_step(body: dict) -> str:
        """
        创建实例（立刻运行并开始计费）。支持创建 ElasticSearch (ES) 或 OpenSearch (OS) 实例。
        Call steps:
        1. Pass "create_instance_in_one_step" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  create_instance_in_one_step
        """
        reqs = service.mcp_post(
            "Es_cloudMcpCreateInstanceInOneStep", {}, json.dumps(body)
        )

        return reqs

    @mcp.tool()
    def describe_node_available_specs(body: dict) -> str:
        """
        查询可用的节点类型、节点规格和存储规格列表，并会返回计费配置码
        Call steps:
        1. Pass "describe_node_available_specs" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_node_available_specs
        """
        reqs = service.mcp_post(
            "Es_cloudMcpDescribeNodeAvailableSpecs", {}, json.dumps(body)
        )

        return reqs

    @mcp.tool()
    def describe_instance_plugins(body: dict) -> str:
        """
        查询实例中已经安装的插件列表
        Call steps:
        1. Pass "describe_instance_plugins" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_instance_plugins
        """
        reqs = service.mcp_post(
            "Es_cloudMcpDescribeInstancePlugins", {}, json.dumps(body)
        )

        return reqs

    @mcp.tool()
    def rename_instance(body: dict) -> str:
        """
        修改目标实例名称
        Call steps:
        1. Pass "rename_instance" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  rename_instance
        """
        reqs = service.mcp_post("Es_cloudMcpRenameInstance", {}, json.dumps(body))

        return reqs

    @mcp.tool()
    def modify_maintenance_setting(body: dict) -> str:
        """
        修改实例的可维护时间
        Call steps:
        1. Pass "modify_maintenance_setting" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  modify_maintenance_setting
        """
        reqs = service.mcp_post(
            "Es_cloudMcpModifyMaintenanceSetting", {}, json.dumps(body)
        )

        return reqs

    @mcp.tool()
    def modify_deletion_protection(body: dict) -> str:
        """
        启停实例的删除保护功能
        Call steps:
        1. Pass "modify_deletion_protection" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  modify_deletion_protection
        """
        reqs = service.mcp_post(
            "Es_cloudMcpModifyDeletionProtection", {}, json.dumps(body)
        )

        return reqs

    @mcp.tool()
    def describe_instance(body: dict) -> str:
        """
        查询指定实例的配置详情
        Call steps:
        1. Pass "describe_instance" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_instance
        """
        reqs = service.mcp_post("Es_cloudMcpDescribeInstance", {}, json.dumps(body))

        return reqs

    @mcp.tool()
    def restart_node(body: dict) -> str:
        """
        重启实例的特定成员节点
        Call steps:
        1. Pass "restart_node" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  restart_node
        """
        reqs = service.mcp_post("Es_cloudMcpRestartNode", {}, json.dumps(body))

        return reqs

    @mcp.tool()
    def describe_instance_nodes(body: dict) -> str:
        """
        查询实例的成员节点详情，包括节点类型、运行状态、资源配置等信息
        Call steps:
        1. Pass "describe_instance_nodes" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_instance_nodes
        """
        reqs = service.mcp_post(
            "Es_cloudMcpDescribeInstanceNodes", {}, json.dumps(body)
        )

        return reqs

    @mcp.tool()
    def create_instance(body: dict) -> str:
        """
        创建实例（仅下单，待支付）。支持创建 ElasticSearch (ES) 或 OpenSearch (OS) 实例。
        使用该接口创建实例时，必须配置专用 Master 节点，Master 节点数量为 3。
        Call steps:
        1. Pass "create_instance" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  create_instance
        """
        reqs = service.mcp_post("Es_cloudMcpCreateInstance", {}, json.dumps(body))

        return reqs

    return mcp
