from vcloud.veen.api.api import VeenedgeAPI
from mcp.server.fastmcp import FastMCP
from .note import note
from vcloud.utils.response import HandlerVolcResponse
import json

def create_mcp_server():
    service = VeenedgeAPI()
    mcp = FastMCP(
        "VEEN MCP",
        instructions="Apply, configure, and query for edge computing nodes, including virtual machines, images, bare metal, and corresponding network configurations.",
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
            func_name: The function name to get the description for.

        """
        return note.get(func_name)

    @mcp.tool()
    def start_cloud_server() -> str:
        """
        本接口用于根据边缘服务的 ID 启动边缘服务。
        Call steps:
        1. Pass "start_cloud_server" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
        2. After obtaining the parameter instructions, invoke  start_cloud_server
        """
        reqs = service.mcp_post("McpStartCloudServer", {}, json.dumps({}))

        return HandlerVolcResponse(reqs)

    # @mcp.tool()
    # def delete_cloud_server() -> str:
    #     """
    #     本接口用于根据边缘服务 ID 删除边缘服务。
    #     Call steps:
    #     1. Pass "delete_cloud_server" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
    #     2. After obtaining the parameter instructions, invoke  delete_cloud_server
    #     """
    #     reqs = service.mcp_post("McpDeleteCloudServer", {}, json.dumps({}))

    #     return HandlerVolcResponse(reqs)

    # @mcp.tool()
    # def stop_cloud_server() -> str:
    #     """
    #     本接口用于根据边缘服务的 ID 停止边缘服务。
    #     Call steps:
    #     1. Pass "stop_cloud_server" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
    #     2. After obtaining the parameter instructions, invoke  stop_cloud_server
    #     """
    #     reqs = service.mcp_post("McpStopCloudServer", {}, json.dumps({}))

    #     return HandlerVolcResponse(reqs)

    # @mcp.tool()
    # def reboot_cloud_server() -> str:
    #     """
    #     本接口用于根据边缘服务的 ID 重启边缘服务。
    #     Call steps:
    #     1. Pass "reboot_cloud_server" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
    #     2. After obtaining the parameter instructions, invoke  reboot_cloud_server
    #     """
    #     reqs = service.mcp_post("McpRebootCloudServer", {}, json.dumps({}))

    #     return HandlerVolcResponse(reqs)

    @mcp.tool()
    def create_cloud_server(body: dict) -> str:
        """
        本接口用于创建边缘服务。
        Call steps:
        1. Pass "create_cloud_server" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
        2. After obtaining the parameter instructions, invoke  create_cloud_server
        """
        reqs = service.mcp_post("McpCreateCloudServer", {}, json.dumps(body))

        return HandlerVolcResponse(reqs)

    # @mcp.tool()
    # def update_cloud_server(body: dict) -> str:
    #     """
    #     本接口用于修改边缘服务配置。
    #     Call steps:
    #     1. Pass "update_cloud_server" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
    #     2. After obtaining the parameter instructions, invoke  update_cloud_server
    #     """
    #     reqs = service.mcp_post("McpUpdateCloudServer", {}, json.dumps(body))

    #     return HandlerVolcResponse(reqs)

    @mcp.tool()
    def get_cloud_server(params: dict) -> str:
        """
        本接口用于根据边缘服务的 ID 获取边缘服务的详细信息。
        Call steps:
        1. Pass "get_cloud_server" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
        2. After obtaining the parameter instructions, invoke  get_cloud_server
        """
        reqs = service.mcp_get("McpGetCloudServer", params, json.dumps({}))

        return HandlerVolcResponse(reqs)

    # @mcp.tool()
    # def reboot_instances(body: dict) -> str:
    #     """
    #     本接口用于根据边缘实例 ID 重启实例。
    #     Call steps:
    #     1. Pass "reboot_instances" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
    #     2. After obtaining the parameter instructions, invoke  reboot_instances
    #     """
    #     reqs = service.mcp_post("McpRebootInstances", {}, json.dumps(body))

    #     return HandlerVolcResponse(reqs)

    @mcp.tool()
    def start_instances(body: dict) -> str:
        """
        本接口用于根据边缘实例 ID 启动实例。
        Call steps:
        1. Pass "start_instances" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
        2. After obtaining the parameter instructions, invoke  start_instances
        """
        reqs = service.mcp_post("McpStartInstances", {}, json.dumps(body))

        return HandlerVolcResponse(reqs)

    # @mcp.tool()
    # def stop_instances(body: dict) -> str:
    #     """
    #     本接口用于根据边缘实例 ID 停止实例。
    #     Call steps:
    #     1. Pass "stop_instances" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
    #     2. After obtaining the parameter instructions, invoke  stop_instances
    #     """
    #     reqs = service.mcp_post("McpStopInstances", {}, json.dumps(body))

    #     return HandlerVolcResponse(reqs)

    @mcp.tool()
    def list_instances(params: dict) -> str:
        """
        本接口用于列出指定的边缘服务或所有边缘服务下的边缘实例。
        Call steps:
        1. Pass "list_instances" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
        2. After obtaining the parameter instructions, invoke  list_instances
        """
        reqs = service.mcp_get("McpListInstances", params, json.dumps({}))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def get_instance(params: dict) -> str:
        """
        本接口根据边缘实例 ID 获取实例详细信息。
        Call steps:
        1. Pass "get_instance" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
        2. After obtaining the parameter instructions, invoke  get_instance
        """
        reqs = service.mcp_get("McpGetInstance", params, json.dumps({}))

        return HandlerVolcResponse(reqs)

    # @mcp.tool()
    # def reset_login_credential(body: dict) -> str:
    #     """
    #     本接口用于重置重置边缘实例的密码。密码类型允许修改。
    #     Call steps:
    #     1. Pass "reset_login_credential" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
    #     2. After obtaining the parameter instructions, invoke  reset_login_credential
    #     """
    #     reqs = service.mcp_post("McpResetLoginCredential", {}, json.dumps(body))

    #     return HandlerVolcResponse(reqs)

    @mcp.tool()
    def set_instance_name(body: dict) -> str:
        """
        本接口用于设置边缘实例的名称。
        Call steps:
        1. Pass "set_instance_name" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
        2. After obtaining the parameter instructions, invoke  set_instance_name
        """
        reqs = service.mcp_post("McpSetInstanceName", {}, json.dumps(body))

        return HandlerVolcResponse(reqs)

    # @mcp.tool()
    # def batch_reset_system(body: dict) -> str:
    #     """
    #     本接口用于重置指定边缘实例的操作系统或更换边缘实例的镜像。
    #     Call steps:
    #     1. Pass "batch_reset_system" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
    #     2. After obtaining the parameter instructions, invoke  batch_reset_system
    #     """
    #     reqs = service.mcp_post("McpBatchResetSystem", {}, json.dumps(body))

    #     return HandlerVolcResponse(reqs)

    # @mcp.tool()
    # def set_instances_bandwidth_peak(body: dict) -> str:
    #     """
    #     本接口用于批量设置边缘实例的带宽峰值。
    #     Call steps:
    #     1. Pass "set_instances_bandwidth_peak" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
    #     2. After obtaining the parameter instructions, invoke  set_instances_bandwidth_peak
    #     """
    #     reqs = service.mcp_post("McpSetInstancesBandwidthPeak", {}, json.dumps(body))

    #     return HandlerVolcResponse(reqs)

    @mcp.tool()
    def enable_instances_i_pv6(body: dict) -> str:
        """
        本接口用于批量开启边缘实例的 IPv6 功能。
        Call steps:
        1. Pass "enable_instances_i_pv6" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
        2. After obtaining the parameter instructions, invoke  enable_instances_i_pv6
        """
        reqs = service.mcp_post("McpEnableInstancesIPv6", {}, json.dumps(body))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def get_instances_i_pv6_upgrade_status(params: dict) -> str:
        """
        本接口用于获取边缘实例的 IPv6 开启状态。
        Call steps:
        1. Pass "get_instances_i_pv6_upgrade_status" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
        2. After obtaining the parameter instructions, invoke  get_instances_i_pv6_upgrade_status
        """
        reqs = service.mcp_get(
            "McpGetInstancesIPv6UpgradeStatus", params, json.dumps({})
        )

        return HandlerVolcResponse(reqs)

    # @mcp.tool()
    # def update_instances_spec(body: dict) -> str:
    #     """
    #     本接口用于变更边缘实例的实例规格。
    #     Call steps:
    #     1. Pass "update_instances_spec" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
    #     2. After obtaining the parameter instructions, invoke  update_instances_spec
    #     """
    #     reqs = service.mcp_post("McpUpdateInstancesSpec", {}, json.dumps(body))

    #     return HandlerVolcResponse(reqs)

    @mcp.tool()
    def list_instance_internal_ips(params: dict) -> str:
        """
        本接口用于获取边缘实例的私网 IP 地址的列表。
        Call steps:
        1. Pass "list_instance_internal_ips" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
        2. After obtaining the parameter instructions, invoke  list_instance_internal_ips
        """
        reqs = service.mcp_get("McpListInstanceInternalIps", params, json.dumps({}))

        return HandlerVolcResponse(reqs)

    # @mcp.tool()
    # def set_bound_eip_share_bandwidth_peak(body: dict) -> str:
    #     """
    #     本接口用于设置弹性公网 IP 的共享带宽峰值。共享带宽峰值指的是绑定在边缘实例私网 IP 地址（含主私网 IP 地址和辅助私网 IP 地址）上的所有弹性公网 IP 的共享公网带宽限速值。
    #     Call steps:
    #     1. Pass "set_bound_eip_share_bandwidth_peak" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
    #     2. After obtaining the parameter instructions, invoke  set_bound_eip_share_bandwidth_peak
    #     """
    #     reqs = service.mcp_post(
    #         "McpSetBoundEipShareBandwidthPeak", {}, json.dumps(body)
    #     )

    #     return HandlerVolcResponse(reqs)

    # @mcp.tool()
    # def batch_bind_eip_to_internal_ips_randomly(body: dict) -> str:
    #     """
    #     本接口用于批量随机绑定弹性公网 IP 到私网 IP 地址。
    #     Call steps:
    #     1. Pass "batch_bind_eip_to_internal_ips_randomly" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
    #     2. After obtaining the parameter instructions, invoke  batch_bind_eip_to_internal_ips_randomly
    #     """
    #     reqs = service.mcp_post(
    #         "McpBatchBindEipToInternalIpsRandomly", {}, json.dumps(body)
    #     )

    #     return HandlerVolcResponse(reqs)

    # @mcp.tool()
    # def batch_delete_internal_ips(body: dict) -> str:
    #     """
    #     本接口用于批量删除边缘实例的辅助私网 IP 地址。
    #     Call steps:
    #     1. Pass "batch_delete_internal_ips" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
    #     2. After obtaining the parameter instructions, invoke  batch_delete_internal_ips
    #     """
    #     reqs = service.mcp_post("McpBatchDeleteInternalIps", {}, json.dumps(body))

    #     return HandlerVolcResponse(reqs)

    @mcp.tool()
    def get_instance_cloud_disk_info(params: dict) -> str:
        """
        本接口用于获取边缘实例的云盘信息。
        Call steps:
        1. Pass "get_instance_cloud_disk_info" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
        2. After obtaining the parameter instructions, invoke  get_instance_cloud_disk_info
        """
        reqs = service.mcp_get("McpGetInstanceCloudDiskInfo", params, json.dumps({}))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def set_cloud_server_delete_protection(body: dict) -> str:
        """
        本接口用于为边缘服务配置删除保护。您可以通过该接口开启或关闭删除保护功能。
        删除保护功能可以防止您的边缘服务被误删除，保障数据安全。
        Call steps:
        1. Pass "set_cloud_server_delete_protection" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
        2. After obtaining the parameter instructions, invoke  set_cloud_server_delete_protection
        """
        reqs = service.mcp_post(
            "McpSetCloudServerDeleteProtection", {}, json.dumps(body)
        )

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def set_instance_delete_protection(body: dict) -> str:
        """
        本接口用于为一个或多个边缘实例配置删除保护。您可以通过该接口开启或关闭删除保护功能。
        删除保护功能可以防止您的边缘实例被误删除，保障数据安全。
        Call steps:
        1. Pass "set_instance_delete_protection" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
        2. After obtaining the parameter instructions, invoke  set_instance_delete_protection
        """
        reqs = service.mcp_post("McpSetInstanceDeleteProtection", {}, json.dumps(body))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def list_cloud_servers(params: dict) -> str:
        """
        本接口用于列出账号下的所有边缘服务信息。
        Call steps:
        1. Pass "list_cloud_servers" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
        2. After obtaining the parameter instructions, invoke  list_cloud_servers
        """
        reqs = service.mcp_get("McpListCloudServers", params, json.dumps({}))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def list_instance_types() -> str:
        """
        本接口用于获取边缘服务下可开通的实例规格。
        Call steps:
        1. Pass "list_instance_types" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
        2. After obtaining the parameter instructions, invoke  list_instance_types
        """
        reqs = service.mcp_get("McpListInstanceTypes", {}, json.dumps({}))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def list_available_resource_info(params: dict) -> str:
        """
        本接口用于获取边缘服务下某实例规格支持的地域和运营商。
        Call steps:
        1. Pass "list_available_resource_info" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
        2. After obtaining the parameter instructions, invoke  list_available_resource_info
        """
        reqs = service.mcp_get("McpListAvailableResourceInfo", params, json.dumps({}))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def create_instance(body: dict) -> str:
        """
        本接口用于创建边缘实例。
        Call steps:
        1. Pass "create_instance" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
        2. After obtaining the parameter instructions, invoke  create_instance
        """
        reqs = service.mcp_post("McpCreateInstance", {}, json.dumps(body))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def create_secondary_internal_ip_and_reboot(body: dict) -> str:
        """
        本接口用于为边缘实例新增辅助私网 IP 地址并重启该边缘实例。
        Call steps:
        1. Pass "create_secondary_internal_ip_and_reboot" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
        2. After obtaining the parameter instructions, invoke  create_secondary_internal_ip_and_reboot
        """
        reqs = service.mcp_post(
            "McpCreateSecondaryInternalIPAndReboot", {}, json.dumps(body)
        )

        return HandlerVolcResponse(reqs)

    # @mcp.tool()
    # def bind_eip_to_internal_ip(body: dict) -> str:
    #     """
    #     本接口用于绑定单个弹性公网 IP 到私网 IP 地址。
    #     Call steps:
    #     1. Pass "bind_eip_to_internal_ip" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
    #     2. After obtaining the parameter instructions, invoke  bind_eip_to_internal_ip
    #     """
    #     reqs = service.mcp_post("McpBindEipToInternalIP", {}, json.dumps(body))

    #     return HandlerVolcResponse(reqs)

    @mcp.tool()
    def list_images(params: dict) -> str:
        """
        本接口用于获取某一实例规格支持的镜像列表，包括公共镜像和自定义镜像。
        Call steps:
        1. Pass "list_images" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
        2. After obtaining the parameter instructions, invoke  list_images
        """
        reqs = service.mcp_get("McpListImages", params, json.dumps({}))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def get_image(params: dict) -> str:
        """
        本接口用于获取镜像详情。
        Call steps:
        1. Pass "get_image" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
        2. After obtaining the parameter instructions, invoke  get_image
        """
        reqs = service.mcp_get("McpGetImage", params, json.dumps({}))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def build_image_by_vm(body: dict) -> str:
        """
        本接口用于通过边缘实例创建镜像。
        Call steps:
        1. Pass "build_image_by_vm" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
        2. After obtaining the parameter instructions, invoke  build_image_by_vm
        """
        reqs = service.mcp_post("McpBuildImageByVM", {}, json.dumps(body))

        return HandlerVolcResponse(reqs)

    # @mcp.tool()
    # def upload_url_image(body: dict) -> str:
    #     """
    #     本接口用于导入镜像。
    #     Call steps:
    #     1. Pass "upload_url_image" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
    #     2. After obtaining the parameter instructions, invoke  upload_url_image
    #     """
    #     reqs = service.mcp_post("McpUploadURLImage", {}, json.dumps(body))

    #     return HandlerVolcResponse(reqs)

    # @mcp.tool()
    # def update_image(body: dict) -> str:
    #     """
    #     本接口用于编辑镜像的名称。
    #     Call steps:
    #     1. Pass "update_image" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
    #     2. After obtaining the parameter instructions, invoke  update_image
    #     """
    #     reqs = service.mcp_post("McpUpdateImage", {}, json.dumps(body))

    #     return HandlerVolcResponse(reqs)

    # @mcp.tool()
    # def delete_image(body: dict) -> str:
    #     """
    #     本接口用于删除镜像。
    #     Call steps:
    #     1. Pass "delete_image" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
    #     2. After obtaining the parameter instructions, invoke  delete_image
    #     """
    #     reqs = service.mcp_post("McpDeleteImage", {}, json.dumps(body))

    #     return HandlerVolcResponse(reqs)

    @mcp.tool()
    def get_veen_instance_usage(params: dict) -> str:
        """
        本接口用于获取指定时间范围内的算力用量。
        Call steps:
        1. Pass "get_veen_instance_usage" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
        2. After obtaining the parameter instructions, invoke  get_veen_instance_usage
        """
        reqs = service.mcp_get("McpGetVEENInstanceUsage", params, json.dumps({}))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def get_veew_instance_usage(params: dict) -> str:
        """
        本接口用于获取指定时间范围内的边缘网络的用量。
        Call steps:
        1. Pass "get_veew_instance_usage" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
        2. After obtaining the parameter instructions, invoke  get_veew_instance_usage
        """
        reqs = service.mcp_get("McpGetVEEWInstanceUsage", params, json.dumps({}))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def get_bandwidth_usage(params: dict) -> str:
        """
        本接口用于获取指定时间范围内的带宽用量。
        Call steps:
        1. Pass "get_bandwidth_usage" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
        2. After obtaining the parameter instructions, invoke  get_bandwidth_usage
        """
        reqs = service.mcp_get("McpGetBandwidthUsage", params, json.dumps({}))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def get_billing_usage_detail(params: dict) -> str:
        """
        本接口用于获取日用量趋势。
        Call steps:
        1. Pass "get_billing_usage_detail" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
        2. After obtaining the parameter instructions, invoke  get_billing_usage_detail
        """
        reqs = service.mcp_get("McpGetBillingUsageDetail", params, json.dumps({}))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def list_vpc_instances(params: dict) -> str:
        """
        本接口用于获取私有网络列表。
        Call steps:
        1. Pass "list_vpc_instances" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
        2. After obtaining the parameter instructions, invoke  list_vpc_instances
        """
        reqs = service.mcp_get("McpListVPCInstances", params, json.dumps({}))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def set_vpc_instance_desc(body: dict) -> str:
        """
        本接口用于修改私有网络的描述。
        Call steps:
        1. Pass "set_vpc_instance_desc" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
        2. After obtaining the parameter instructions, invoke  set_vpc_instance_desc
        """
        reqs = service.mcp_post("McpSetVPCInstanceDesc", {}, json.dumps(body))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def list_route_tables(params: dict) -> str:
        """
        本接口用于查询路由表的列表。
        Call steps:
        1. Pass "list_route_tables" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
        2. After obtaining the parameter instructions, invoke  list_route_tables
        """
        reqs = service.mcp_get("McpListRouteTables", params, json.dumps({}))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def get_route_table(params: dict) -> str:
        """
        本接口用于查询路由表的详情。
        Call steps:
        1. Pass "get_route_table" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
        2. After obtaining the parameter instructions, invoke  get_route_table
        """
        reqs = service.mcp_get("McpGetRouteTable", params, json.dumps({}))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def set_route_table_name_and_desc(body: dict) -> str:
        """
        本接口用于修改路由表的名称和描述信息。
        Call steps:
        1. Pass "set_route_table_name_and_desc" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
        2. After obtaining the parameter instructions, invoke  set_route_table_name_and_desc
        """
        reqs = service.mcp_post("McpSetRouteTableNameAndDesc", {}, json.dumps(body))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def list_route_entries(params: dict) -> str:
        """
        本接口用于查询路由条目列表。
        Call steps:
        1. Pass "list_route_entries" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
        2. After obtaining the parameter instructions, invoke  list_route_entries
        """
        reqs = service.mcp_get("McpListRouteEntries", params, json.dumps({}))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def create_route_entries(body: dict) -> str:
        """
        本接口用于批量增加自定义路由条目。
        Call steps:
        1. Pass "create_route_entries" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
        2. After obtaining the parameter instructions, invoke  create_route_entries
        """
        reqs = service.mcp_post("McpCreateRouteEntries", {}, json.dumps(body))

        return HandlerVolcResponse(reqs)

    # @mcp.tool()
    # def delete_route_entry(body: dict) -> str:
    #     """
    #     本接口用于删除路由条目。
    #     Call steps:
    #     1. Pass "delete_route_entry" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
    #     2. After obtaining the parameter instructions, invoke  delete_route_entry
    #     """
    #     reqs = service.mcp_post("McpDeleteRouteEntry", {}, json.dumps(body))

    #     return HandlerVolcResponse(reqs)

    @mcp.tool()
    def enable_route_entry(body: dict) -> str:
        """
        本接口用于启用路由条目。
        Call steps:
        1. Pass "enable_route_entry" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
        2. After obtaining the parameter instructions, invoke  enable_route_entry
        """
        reqs = service.mcp_post("McpEnableRouteEntry", {}, json.dumps(body))

        return HandlerVolcResponse(reqs)

    # @mcp.tool()
    # def disable_route_entry(body: dict) -> str:
    #     """
    #     本接口用于禁用路由条目。
    #     Call steps:
    #     1. Pass "disable_route_entry" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
    #     2. After obtaining the parameter instructions, invoke  disable_route_entry
    #     """
    #     reqs = service.mcp_post("McpDisableRouteEntry", {}, json.dumps(body))

    #     return HandlerVolcResponse(reqs)

    @mcp.tool()
    def set_route_entry_desc(body: dict) -> str:
        """
        本接口用于修改路由条目的描述信息。
        Call steps:
        1. Pass "set_route_entry_desc" as an input parameter to invoke the `get_note` method to obtain the parameter instructions.
        2. After obtaining the parameter instructions, invoke  set_route_entry_desc
        """
        reqs = service.mcp_post("McpSetRouteEntryDesc", {}, json.dumps(body))

        return HandlerVolcResponse(reqs)

    return mcp
