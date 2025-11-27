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
        Retrieves the list of available Availability Zones (AZs) in the current region. Use this tool before creating an instance to ensure the target zone supports deployment.
        Call steps:
        1. Pass "describe_zones" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_zones
        """
        reqs = service.mcp_post("Es_cloudMcpDescribeZones", {}, json.dumps(body))

        return reqs

    @mcp.tool()
    def describe_instances(body: dict) -> str:
        """
        Searches for instances using filters like ID, name, status, or version. Use this tool for discovery, listing, or finding instances based on criteria. Returns detailed configuration objects.
        Call steps:
        1. Pass "describe_instances" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_instances
        """
        reqs = service.mcp_post("Es_cloudMcpDescribeInstances", {}, json.dumps(body))

        return reqs

    @mcp.tool()
    def create_instance_in_one_step(body: dict) -> str:
        """
        Creates, pays for, and immediately provisions a new Elasticsearch or OpenSearch instance. Use this tool when the user wants to start using the instance right away. Warning: This action incurs immediate charges.
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
        Retrieves the list of installed plugins for a specific instance. Use this tool to verify if specific extensions (e.g., analysis plugins) are enabled.
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
        Updates the display name (alias) of an instance. Use this tool when the user wants to retag or organize their instances with human-readable names.
        Call steps:
        1. Pass "rename_instance" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  rename_instance
        """
        reqs = service.mcp_post("Es_cloudMcpRenameInstance", {}, json.dumps(body))

        return reqs

    @mcp.tool()
    def modify_maintenance_setting(body: dict) -> str:
        """
        Configures the preferred maintenance window for an instance. Use this tool to schedule system upgrades during off-peak hours.
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
        Toggles the "Deletion Protection" flag. Use this tool to lock an instance against accidental deletion or to unlock it prior to a valid deletion request.
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
        Retrieves the most comprehensive details for a single, specific instance ID. Use this tool when the exact ID is known and maximum granularity is required (more detailed than describe_instances).
        Call steps:
        1. Pass "describe_instance" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_instance
        """
        reqs = service.mcp_post("Es_cloudMcpDescribeInstance", {}, json.dumps(body))

        return reqs

    @mcp.tool()
    def restart_node(body: dict) -> str:
        """
        Restarts a specific node within an instance. Use this tool only when necessary for fault recovery or to force a configuration refresh on a specific node.
        Call steps:
        1. Pass "restart_node" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  restart_node
        """
        reqs = service.mcp_post("Es_cloudMcpRestartNode", {}, json.dumps(body))

        return reqs

    @mcp.tool()
    def describe_instance_nodes(body: dict) -> str:
        """
        Lists detailed information about the member nodes within a specific instance, including roles (Master/Data), hardware specs, and IP addresses. Use this tool for topology inspection or connection troubleshooting.
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
        Creates a pending, unpaid order for a new Elasticsearch or OpenSearch instance. Use this tool when the user wants to set up an instance configuration but proceed with payment manually later. Note: This does not provision the instance immediately.
        Constraint: When calling this tool, dedicated Master nodes are mandatory, and the quantity of Master nodes must be set to exactly 3.
        Call steps:
        1. Pass "create_instance" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  create_instance
        """
        reqs = service.mcp_post("Es_cloudMcpCreateInstance", {}, json.dumps(body))

        return reqs

    return mcp
