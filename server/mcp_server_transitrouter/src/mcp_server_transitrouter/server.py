import logging
import os

from typing import Any, List, Optional, Dict
from mcp.server.fastmcp import FastMCP
from mcp_server_transitrouter.base.transitrouter import TRSDK

logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("TR MCP Server", port=int(os.getenv("PORT", "8008")))

tr_resource = TRSDK()


@mcp.tool(
    name="describe_transit_routers",
    description="查询满足指定条件的中转路由器实例"
)
def describe_transit_routers(
        transit_router_ids: Optional[List[str]] = None,
        transit_router_name: Optional[str] = None,
        project_name: Optional[str] = None
) -> dict[str, Any]:
    """
    调用 DescribeTransitRouters 接口，查询满足指定条件的中转路由器实例。
    Args:
        transit_router_ids Optional(List[str]): 中转路由器实例的ID列表。
        transit_router_name Optional(str): 中转路由器实例的名称。
        project_name Optional(List[str]): 中转路由器实例所属项目的名称列表。
    Returns:
        dict[str, Any]: 中转路由器实例的详细信息。
    """
    req = {
        "transit_router_ids": transit_router_ids,
        "transit_router_name": transit_router_name,
        "project_name": project_name
    }

    resp = tr_resource.describe_transit_routers(req)
    return resp.to_dict()

@mcp.tool(
    name="describe_transit_router_attachments",
    description="查询满足指定条件的中转路由器实例"
)
def describe_transit_router_attachments(
        transit_router_id: Optional[str] = None,
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        transit_router_forward_policy_table_id: Optional[str] = None,
        transit_router_traffic_qos_marking_policy_id: Optional[str] = None,
        transit_router_traffic_qos_queue_policy_id: Optional[str] = None,
        transit_router_attachment_ids: Optional[List[str]] = None,
) -> dict[str, Any]:
    """
    调用 DescribeTransitRouterAttachments 接口，查询实例共享列表。
    Args:
        transit_router_id Optional(str): 中转路由器实例的ID。
        resource_type Optional(str): 资源类型。
        resource_id Optional(str): 资源ID。
        transit_router_forward_policy_table_id Optional(str): 路由策略表ID。
        transit_router_traffic_qos_marking_policy_id Optional(str): 流量QoS标记策略ID。
        transit_router_traffic_qos_queue_policy_id Optional(str): 流量QoS队列策略ID。
        transit_router_attachment_ids Optional(List[str]): 实例共享关系ID列表。
    Returns:
        dict[str, Any]: 中转路由器实例的详细信息。
    """
    req = {
        "transit_router_id": transit_router_id,
        "resource_type": resource_type,
        "resource_id": resource_id,
        "transit_router_forward_policy_table_id": transit_router_forward_policy_table_id,
        "transit_router_traffic_qos_marking_policy_id": transit_router_traffic_qos_marking_policy_id,
        "transit_router_traffic_qos_queue_policy_id": transit_router_traffic_qos_queue_policy_id,
        "transit_router_attachment_ids": transit_router_attachment_ids,
    }

    resp = tr_resource.describe_transit_router_attachments(req)
    return resp.to_dict()

@mcp.tool(
    name="describe_transit_router_vpc_attachments",
    description="查询满足指定条件的VPC类型网络实例连接"
)
def describe_transit_router_vpc_attachments(
        transit_router_id: str = None,
        vpc_id: Optional[str] = None,
        transit_router_attachment_ids: Optional[List[str]] = None
) -> dict[str, Any]:
    """
    调用 DescribeTransitRouterVpcAttachments 接口，查询满足指定条件的VPC类型网络实例连接。
    Args:
        transit_router_id (str, optional): 中转路由器实例的ID。
        vpc_id (str, optional): VPC实例的ID。
        transit_router_attachment_ids (list[str], optional): 实例连接的ID列表。
    Returns:
        dict[str, Any]: 实例共享的详细信息。
    """
    req = {
        "transit_router_id": transit_router_id,
        "vpc_id": vpc_id,
        "transit_router_attachment_ids": transit_router_attachment_ids
    }

    resp = tr_resource.describe_transit_router_vpc_attachments(req)
    return resp.to_dict()

@mcp.tool(
    name="describe_transit_router_vpn_attachments",
    description="查询满足指定条件的VPN类型网络实例连接"
)
def describe_transit_router_vpn_attachments(
        transit_router_id: str = None,
        transit_router_attachment_ids: Optional[List[str]] = None,
        vpn_connection_id: Optional[str] = None
) -> dict[str, Any]:
    """
    调用 describe_transit_router_vpn_attachments 接口，查询满足指定条件的VPN类型网络实例连接。
    Args:
        transit_router_id (str, optional): 中转路由器实例的ID。
        transit_router_attachment_ids (list[str], optional): VPN类型网络实例连接的ID列表。
        vpn_connection_id (str, optional): VPN连接的ID。
    Returns:
        dict[str, Any]: VPN类型网络实例连接的详细信息。
    """
    req = {
        "transit_router_id": transit_router_id,
        "transit_router_attachment_ids": transit_router_attachment_ids,
        "vpn_connection_id": vpn_connection_id,
    }

    resp = tr_resource.describe_transit_router_vpn_attachments(req)
    return resp.to_dict()

@mcp.tool(
    name="describe_transit_router_direct_connect_gateway_attachments",
    description="查询满足指定条件的专线网关类型网络实例连接"
)
def describe_transit_router_direct_connect_gateway_attachments(
        transit_router_id: str = None,
        direct_connect_gateway_id: Optional[str] = None,
        transit_router_attachment_ids: Optional[List[str]] = None
) -> dict[str, Any]:
    """
    调用 describe_transit_router_direct_connect_gateway_attachments 接口，查询满足指定条件的专线网关类型网络实例连接。
    Args:
        transit_router_id (str, optional): 中转路由器实例的ID。
        direct_connect_gateway_id (str, optional): 专线网关实例的ID。
        transit_router_attachment_ids (list[str], optional): 实例连接的ID列表。
    Returns:
        dict[str, Any]: 实例共享的详细信息。
    """
    req = {
        "transit_router_id": transit_router_id,
        "direct_connect_gateway_id": direct_connect_gateway_id,
        "transit_router_attachment_ids": transit_router_attachment_ids,
    }

    resp = tr_resource.describe_transit_router_direct_connect_gateway_attachments(req)
    return resp.to_dict()

@mcp.tool(
    name="describe_transit_router_bandwidth_packages",
    description="查询满足指定条件的中转路由器带宽包。"
)
def describe_transit_router_bandwidth_packages(
        transit_router_bandwidth_package_ids: Optional[List[str]] = None,
        local_geographic_region_set_id: Optional[str] = None,
        peer_geographic_region_set_id: Optional[str] = None,
        transit_router_peer_attachment_id: Optional[str] = None,
        transit_router_bandwidth_package_name: Optional[str] = None
) -> dict[str, Any]:
    """
    调用 describe_transit_router_bandwidth_packages 接口，查询中转路由器带宽包列表
    Args:
        transit_router_bandwidth_package_ids (list[str], optional): 实例连接的ID列表。
        local_geographic_region_set_id (str, optional): 本地地域集合的ID。
        peer_geographic_region_set_id (str, optional): 对等地域集合的ID。
        transit_router_peer_attachment_id (str, optional): 对等连接实例的ID。
        transit_router_bandwidth_package_name (str, optional): 带宽包实例的名称。
    Returns:
        dict[str, Any]: 实例共享的详细信息。
    """
    req = {
        "transit_router_bandwidth_package_ids": transit_router_bandwidth_package_ids,
        "local_geographic_region_set_id": local_geographic_region_set_id,
        "peer_geographic_region_set_id": peer_geographic_region_set_id,
        "transit_router_peer_attachment_id": transit_router_peer_attachment_id,
        "transit_router_bandwidth_package_name": transit_router_bandwidth_package_name,
    }
    resp = tr_resource.describe_transit_router_bandwidth_packages(req)
    return resp.to_dict()

@mcp.tool(
    name="describe_transit_router_regions",
    description="查询中转路由器地域信息"
)
def describe_transit_router_regions(
        geographic_region_set_id: Optional[str] = None,
        region_ids: Optional[List[str]] = None,
) -> dict[str, Any]:
    """
    调用 describe_transit_router_regions 接口，查询中转路由器地域信息
    Args:
        geographic_region_set_id (str, optional): 地域集合的ID。
        region_ids (list[str], optional): 地域实例的ID列表。
    Returns:
        dict[str, Any]: 实例共享的详细信息。
    """
    req = {
        "geographic_region_set_id": geographic_region_set_id,
        "region_ids": region_ids,
    }
    resp = tr_resource.describe_transit_router_regions(req)
    return resp.to_dict()

@mcp.tool(
    name="describe_transit_router_bandwidth_packages_billing",
    description="查询中转路由器带宽包计费方式列表"
)
def describe_transit_router_bandwidth_packages_billing(
        transit_router_bandwidth_package_ids: Optional[List[str]] = None,
) -> dict[str, Any]:
    """
    调用 describe_transit_router_bandwidth_packages_billing 查询中转路由器带宽包计费方式列表
    Args:
        transit_router_bandwidth_package_ids (list[str], optional): 实例连接的ID列表。
    Returns:
        dict[str, Any]: 实例共享的详细信息。
    """
    req = {
        "transit_router_bandwidth_package_ids": transit_router_bandwidth_package_ids,
    }
    resp = tr_resource.describe_transit_router_bandwidth_packages_billing(req)
    return resp.to_dict()

@mcp.tool(
    name="describe_transit_router_peer_attachments",
    description="查询满足指定条件的跨地域连接"
)
def describe_transit_router_peer_attachments(
        transit_router_id: Optional[str] = None,
        transit_router_attachment_ids: Optional[List[str]] = None,
        peer_transit_router_id: Optional[str] = None,
        peer_transit_router_region_id: Optional[str] = None,
) -> dict[str, Any]:
    """
    调用 describe_transit_router_peer_attachments 查询满足指定条件的对等连接实例
    Args:
        transit_router_attachment_ids (list[str], optional): 跨地域连接的ID。
        transit_router_id (str, optional): 跨地域连接关联的本端中转路由器实例的ID。
        peer_transit_router_id (str, optional): 对端中转路由器实例的ID。
        peer_transit_router_region_id (str, optional): 对端中转路由器所属地域的ID。
    Returns:
        dict[str, Any]: 实例共享的详细信息。
    """
    req = {
        "transit_router_attachment_ids": transit_router_attachment_ids,
        "transit_router_id": transit_router_id,
        "peer_transit_router_id": peer_transit_router_id,
        "peer_transit_router_region_id": peer_transit_router_region_id,
    }
    resp = tr_resource.describe_transit_router_peer_attachments(req)
    return resp.to_dict()

@mcp.tool(
    name="describe_transit_router_route_tables",
    description="查询满足指定条件的路由表"
)
def describe_transit_router_route_tables(
        transit_router_route_table_ids: Optional[List[str]] = None,
        transit_router_id: str = None,
        transit_router_route_table_type: Optional[str] = None,
) -> dict[str, Any]:
    """
    调用 describe_transit_router_route_tables 查询满足指定条件的路由表
    Args:
        transit_router_route_table_ids (list[str], optional): 路由表的ID列表。
        transit_router_id (str, optional): 路由表关联的本端中转路由器实例的ID。
        transit_router_route_table_type (str, optional): 路由表的类型。
    Returns:
        dict[str, Any]: 实例共享的详细信息。
    """
    req = {
        "transit_router_route_table_ids": transit_router_route_table_ids,
        "transit_router_id": transit_router_id,
        "transit_router_route_table_type": transit_router_route_table_type
    }
    resp = tr_resource.describe_transit_router_route_tables(req)
    return resp.to_dict()

@mcp.tool(
    name="describe_transit_router_route_entries",
    description="查询满足指定条件的路由条目"
)
def describe_transit_router_route_entries(
    transit_router_route_entry_type: Optional[str] = None,
    transit_router_route_entry_next_hop_type: Optional[str] = None,
    transit_router_route_entry_next_hop_resource_type: Optional[str] = None,
    transit_router_route_table_id: str = None,
    destination_cidr_block: Optional[str] = None,
    status: Optional[str] = None,
    transit_router_route_entry_name: Optional[str] = None,
    transit_router_route_entry_ids: Optional[List[str]] = None
) -> dict[str, Any]:
    """
    调用 describe_transit_router_route_entries 查询满足指定条件的路由条目
    Args:
        transit_router_route_entry_type (str, optional): 路由条目类型。
        transit_router_route_entry_next_hop_type (str, optional): 路由条目的下一跳类型。
        transit_router_route_entry_next_hop_resource_type (str, optional): 路由条目的下一跳资源类型。
        transit_router_route_table_id (str, optional): 路由表的ID。
        destination_cidr_block (str, optional): 路由条目的目标网段。
        status (str, optional): 路由条目的状态。
        transit_router_route_entry_name (str, optional): 路由条目的名称。
        transit_router_route_entry_ids (list[str], optional): 路由条目的ID列表。
    Returns:
        dict[str, Any]: 实例共享的详细信息。
    """
    req = {
        "transit_router_route_entry_type": transit_router_route_entry_type,
        "transit_router_route_entry_next_hop_type": transit_router_route_entry_next_hop_type,
        "transit_router_route_entry_next_hop_resource_type": transit_router_route_entry_next_hop_resource_type,
        "transit_router_route_table_id": transit_router_route_table_id,
        "destination_cidr_block": destination_cidr_block,
        "status": status,
        "transit_router_route_entry_name": transit_router_route_entry_name,
        "transit_router_route_entry_ids": transit_router_route_entry_ids,
    }
    resp = tr_resource.describe_transit_router_route_entries(req)
    return resp.to_dict()

@mcp.tool(
    name="describe_transit_router_route_table_associations",
    description="查询满足指定条件的关联转发"
)
def describe_transit_router_route_table_associations(
    transit_router_route_table_id: str = None,
    transit_router_attachment_id: Optional[str] = None,
) -> dict[str, Any]:
    """
    调用 describe_transit_router_route_table_associations 查询满足指定条件的关联转发
    Args:
        transit_router_route_table_id (str, optional): 关联转发关联的路由表实例的ID。
        transit_router_attachment_id (str, optional): 关联转发关联的本端关联实例的ID。
    Returns:
        dict[str, Any]: 实例共享的详细信息。
    """
    req = {
        "transit_router_route_table_id": transit_router_route_table_id,
        "transit_router_attachment_id": transit_router_attachment_id,
    }
    resp = tr_resource.describe_transit_router_route_table_associations(req)
    return resp.to_dict()

@mcp.tool(
    name="describe_transit_router_route_table_propagations",
    description="查询满足指定条件的路由表传播"
)
def describe_transit_router_route_table_propagations(
        transit_router_route_table_id: str = None,
        transit_router_attachment_id: Optional[str] = None,
) -> dict[str, Any]:
    """
    调用 describe_transit_router_route_table_propagations 查询满足指定条件的路由表传播
    Args:
        transit_router_route_table_id (str, optional): 路由表传播关联的路由表实例的ID。
        transit_router_attachment_id (str, optional): 路由表传播关联的本端关联实例的ID。
    Returns:
        dict[str, Any]: 实例共享的详细信息。
    """
    req = {
        "transit_router_route_table_id": transit_router_route_table_id,
        "transit_router_attachment_id": transit_router_attachment_id,
    }
    resp = tr_resource.describe_transit_router_route_table_propagations(req)
    return resp.to_dict()

@mcp.tool(
    name="describe_transit_router_route_policy_entries",
    description="查询满足指定条件的路由策略条目"
)
def describe_transit_router_route_policy_entries(
    transit_router_route_policy_table_id: str = None,
    transit_router_route_policy_entry_ids: Optional[List[str]] = None,
    direction: Optional[str] = None,
) -> dict[str, Any]:
    """
    调用 describe_transit_router_route_policy_entries 查询满足指定条件的路由策略条目
    Args:
        transit_router_route_policy_table_id (str, optional): 路由策略实例的ID。
        transit_router_route_policy_entry_ids (list[str], optional): 路由策略条目的ID列表。
        direction (str, optional): 路由策略的作用方向。
    Returns:
        dict[str, Any]: 实例共享的详细信息。
    """
    req = {
        "transit_router_route_policy_table_id": transit_router_route_policy_table_id,
        "transit_router_route_policy_entry_ids": transit_router_route_policy_entry_ids,
        "direction": direction,
    }
    resp = tr_resource.describe_transit_router_route_policy_entries(req)
    return resp.to_dict()

@mcp.tool(
    name="describe_transit_router_route_policy_tables",
    description="查询满足指定条件的路由策略。"
)
def describe_transit_router_route_policy_tables(
    transit_router_id: str = None,
    transit_router_route_policy_table_ids: Optional[List[str]] = None,
    transit_router_route_policy_table_name: Optional[str] = None,
    direction: Optional[str] = None,
) -> dict[str, Any]:
    """
    调用 describe_transit_router_route_policy_tables 查询满足指定条件的路由策略。
    Args:
        transit_router_id (str, optional): 路由策略实例的ID列表。
        transit_router_route_policy_table_ids (list[str], optional): 路由策略实例的ID列表。
        transit_router_route_policy_table_name (str, optional): 路由策略实例的名称。
        direction (str, optional): 路由策略的作用方向。
    Returns:
        dict[str, Any]: 实例共享的详细信息。
    """
    req = {
        "transit_router_id": transit_router_id,
        "transit_router_route_policy_table_ids": transit_router_route_policy_table_ids,
        "transit_router_route_policy_table_name": transit_router_route_policy_table_name,
        "direction": direction,
    }
    resp = tr_resource.describe_transit_router_route_policy_tables(req)
    return resp.to_dict()

@mcp.tool(
    name="describe_transit_router_forward_policy_entries",
    description="查询满足指定条件的转发策略条目"
)
def describe_transit_router_forward_policy_entries(
    source_cidr_block: Optional[str] = None,
    destination_cidr_block: Optional[str] = None,
    transit_router_forward_policy_entry_ids: Optional[List[str]] = None,
    transit_router_forward_policy_table_id: str = None,
    transit_router_route_table_id: Optional[str] = None,
) -> dict[str, Any]:
    """
    调用 describe_transit_router_forward_policy_entries 查询满足指定条件的转发策略条目
    Args:
        source_cidr_block (str, optional): 路由策略实例的ID列表。
        destination_cidr_block (list[str], optional): 路由策略实例的ID列表。
        transit_router_forward_policy_entry_ids (str, optional): 路由策略的作用方向。
        transit_router_forward_policy_table_id (str, optional): 路由策略实例的ID列表。
        transit_router_route_table_id (str, optional): 路由策略实例的ID列表。
    Returns:
        dict[str, Any]: 实例共享的详细信息。
    """
    req = {
        "source_cidr_block": source_cidr_block,
        "destination_cidr_block": destination_cidr_block,
        "transit_router_forward_policy_entry_ids": transit_router_forward_policy_entry_ids,
        "transit_router_forward_policy_table_id": transit_router_forward_policy_table_id,
        "transit_router_route_table_id": transit_router_route_table_id,
    }
    resp = tr_resource.describe_transit_router_forward_policy_entries(req)
    return resp.to_dict()

@mcp.tool(
    name="describe_transit_router_forward_policy_tables",
    description="查询满足指定条件的转发策略"
)
def describe_transit_router_forward_policy_tables(
    transit_router_forward_policy_table_ids: Optional[List[str]] = None,
    transit_router_forward_policy_table_name: Optional[str] = None,
    transit_router_id: str = None,
) -> dict[str, Any]:
    """
    调用 describe_transit_router_forward_policy_tables 查询满足指定条件的转发策略
    Args:
        transit_router_forward_policy_table_ids (list[str], optional): 路由策略实例的ID列表。
        transit_router_forward_policy_table_name (str, optional): 路由策略实例的名称。
        transit_router_id (str, optional): 路由策略实例的ID列表。
    Returns:
        dict[str, Any]: 实例共享的详细信息。
    """
    req = {
        "transit_router_forward_policy_table_ids": transit_router_forward_policy_table_ids,
        "transit_router_forward_policy_table_name": transit_router_forward_policy_table_name,
        "transit_router_id": transit_router_id,
    }
    resp = tr_resource.describe_transit_router_forward_policy_tables(req)
    return resp.to_dict()


@mcp.tool(
    name="describe_transit_router_traffic_qos_marking_policies",
    description="查询满足指定条件的流标记策略"
)
def describe_transit_router_traffic_qos_marking_policies(
    transit_router_traffic_qos_marking_policy_ids: Optional[List[str]] = None,
    transit_router_traffic_qos_marking_policy_name: Optional[List[str]] = None,
    transit_router_id: str = None,
) -> dict[str, Any]:
    """
    调用 describe_transit_router_traffic_qos_marking_policies 查询满足指定条件的流标记策略
    Args:
        transit_router_traffic_qos_marking_policy_ids (list[str], optional): 流标记策略的ID。
        transit_router_traffic_qos_marking_policy_name (str, optional): 路由策略实例的名称。
        transit_router_id (str, optional): 路由策略实例的ID列表。
    Returns:
        dict[str, Any]: 实例共享的详细信息。
    """
    req = {
        "transit_router_traffic_qos_marking_policy_ids": transit_router_traffic_qos_marking_policy_ids,
        "transit_router_traffic_qos_marking_policy_name": transit_router_traffic_qos_marking_policy_name,
        "transit_router_id": transit_router_id,
    }
    resp = tr_resource.describe_transit_router_traffic_qos_marking_policies(req)
    return resp.to_dict()

@mcp.tool(
    name="describe_transit_router_traffic_qos_marking_entries",
    description="查询流标记策略中满足指定条件的标记规则。"
)
def describe_transit_router_traffic_qos_marking_entries(
    transit_router_traffic_qos_marking_policy_id: str = None,
    transit_router_traffic_qos_marking_entry_ids: Optional[List[str]] = None,
    transit_router_traffic_qos_marking_entry_name: Optional[str] = None,
    protocol: Optional[str] = None,
    source_cidr_block: Optional[str] = None,
    destination_cidr_block: Optional[str] = None,
    match_dscp: Optional[str] = None,
    remarking_dscp: Optional[str] = None,
) -> dict[str, Any]:
    """
    调用 describe_transit_router_traffic_qos_marking_entries 查询流标记策略中满足指定条件的标记规则。
    Args:
        transit_router_traffic_qos_marking_policy_id (str, optional): 流量标记策略实例的ID。
        transit_router_traffic_qos_marking_entry_ids (list[str], optional): 流量标记条目的ID列表。
        transit_router_traffic_qos_marking_entry_name (str, optional): 流量标记条目的名称。
        protocol (str, optional): 流量标记条目的协议。
        source_cidr_block (str, optional): 流量标记条目的源IP地址范围。
        destination_cidr_block (str, optional): 流量标记条目的目标IP地址范围。
        match_dscp (str, optional): 流量标记条目的DSCP值。
        remarking_dscp (str, optional): 流量标记条目的重写DSCP值。
    Returns:
        dict[str, Any]: 实例共享的详细信息。
    """
    req = {
        "transit_router_traffic_qos_marking_policy_id": transit_router_traffic_qos_marking_policy_id,
        "transit_router_traffic_qos_marking_entry_ids": transit_router_traffic_qos_marking_entry_ids,
        "transit_router_traffic_qos_marking_entry_name": transit_router_traffic_qos_marking_entry_name,
        "protocol": protocol,
        "source_cidr_block": source_cidr_block,
        "destination_cidr_block": destination_cidr_block,
        "match_dscp": match_dscp,
        "remarking_dscp": remarking_dscp,
    }
    resp = tr_resource.describe_transit_router_traffic_qos_marking_entries(req)
    return resp.to_dict()

@mcp.tool(
    name="describe_transit_router_traffic_qos_queue_policies",
    description="查询满足指定条件的流量调度策略。"
)
def describe_transit_router_traffic_qos_queue_policies(
    transit_router_id: str = None,
    transit_router_traffic_qos_queue_policy_ids: Optional[List[str]] = None,
    transit_router_traffic_qos_queue_policy_name: Optional[str] = None,
) -> dict[str, Any]:
    """
    调用 describe_transit_router_traffic_qos_queue_policies 查询满足指定条件的流量调度策略。
    Args:
        transit_router_id (str, optional): 流量调度策略实例的ID。
        transit_router_traffic_qos_queue_policy_ids (list[str], optional): 流量调度策略实例的ID列表。
        transit_router_traffic_qos_queue_policy_name (str, optional): 流量调度策略实例的名称。
    Returns:
        dict[str, Any]: 实例共享的详细信息。
    """
    req = {
        "transit_router_id": transit_router_id,
        "transit_router_traffic_qos_queue_policy_ids": transit_router_traffic_qos_queue_policy_ids,
        "transit_router_traffic_qos_queue_policy_name": transit_router_traffic_qos_queue_policy_name,
    }
    resp = tr_resource.describe_transit_router_traffic_qos_queue_policies(req)
    return resp.to_dict()

@mcp.tool(
    name="describe_transit_router_traffic_qos_queue_entries",
    description="查询满足指定条件的流队列。"
)
def describe_transit_router_traffic_qos_queue_entries(
    transit_router_traffic_qos_queue_policy_id: str = None,
    transit_router_traffic_qos_queue_entry_ids: Optional[List[str]] = None,
    transit_router_traffic_qos_queue_entry_name: Optional[str] = None,
) -> dict[str, Any]:
    """
    调用 describe_transit_router_traffic_qos_queue_entries 查询满足指定条件的流队列。
    Args:
        transit_router_traffic_qos_queue_policy_id (str, optional): 流量调度策略实例的ID。
        transit_router_traffic_qos_queue_entry_ids (list[str], optional): 流量调度队列实例的ID列表。
        transit_router_traffic_qos_queue_entry_name (str, optional): 流量调度队列实例的名称。
    Returns:
        dict[str, Any]: 实例共享的详细信息。
    """
    req = {
        "transit_router_traffic_qos_queue_policy_id": transit_router_traffic_qos_queue_policy_id,
        "transit_router_traffic_qos_queue_entry_ids": transit_router_traffic_qos_queue_entry_ids,
        "transit_router_traffic_qos_queue_entry_name": transit_router_traffic_qos_queue_entry_name,
    }
    resp = tr_resource.describe_transit_router_traffic_qos_queue_entries(req)
    return resp.to_dict()


if __name__ == "__main__":
    mcp.run()