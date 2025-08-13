"""
路由表工具.
"""

from typing import Literal

from pydantic import BaseModel
from pydantic import Field
from volcenginesdkvpc import models

from mcp_server_vpc.common import client
from mcp_server_vpc.common import errors
from mcp_server_vpc.server import mcp


class RouteTable(BaseModel):
    """路由表"""
    vpc_id: str = Field(description="路由表所属的VPC ID")
    route_table_id: str = Field(description="路由表ID")
    route_table_name: str = Field(description="路由表名称")
    description: str = Field(description="路由表描述信息")
    route_table_type: str = Field(description="路由表的类型")
    subnet_ids: list[str] = Field(description="路由表绑定的子网列表")
    project_name: str = Field(description="路由表所属项目的名称")
    creation_time: str = Field(description="创建路由表的时间")
    update_time: str = Field(description="更新路由表的时间")


class RouteEntry(BaseModel):
    """路由条目"""
    description: str = Field(description="路由条目描述")
    destination_cidr_block: str = Field(description="路由条目的目标网段")
    route_entry_id: str = Field(description="路由条目ID")
    route_entry_name: str = Field(description="路由条目名称")
    route_table_id: str = Field(description="路由条目所属路由表的ID")
    status: str = Field(description="路由规则状态")
    type: str = Field(description="路由条目类型")
    vpc_id: str = Field(description="路由条目所属私有网络的ID")
    next_hop_id: str = Field(description="下一跳资源的ID")
    next_hop_type: str = Field(description="下一跳类型")
    prefix_list_cidr_blocks: list[str] = Field(description="前缀列表的CIDR")


@mcp.tool(description="查询满足指定条件的路由表")
def describe_route_table_list(
        region: str | None = Field(description="请求的region", default=None),
        vpc_id: str | None = Field(description="路由表所属VPC的ID", default=None),
        route_table_id: str | None = Field(description="要查询的路由表的ID", default=None),
        route_table_name: str | None = Field(description="要查询的路由表名称", default=None),
        project_name: str | None = Field(description="路由表所属项目的名称", default=None),
        max_results: int = Field(description="查询的数量，默认为10，最大为100", default=10),
) -> list[RouteTable]:
    try:
        response = client.get_client(region=region).describe_route_table_list(
            models.DescribeRouteTableListRequest(
                vpc_id=vpc_id,
                route_table_id=route_table_id,
                route_table_name=route_table_name,
                project_name=project_name,
                max_results=max_results,
            ))
        if not response or not response.router_table_list:
            return []
        return [RouteTable(
            vpc_id=i.vpc_id,
            route_table_id=i.route_table_id,
            route_table_name=i.route_table_name,
            description=i.description,
            route_table_type=i.route_table_type,
            subnet_ids=i.subnet_ids or [],
            project_name=i.project_name,
            creation_time=i.creation_time,
            update_time=i.update_time,
        ) for i in response.router_table_list]
    except Exception as e:
        raise errors.VPCError("查询路由表失败", e)


@mcp.tool(description="在指定路由表内查询满足指定条件的路由条目")
def describe_route_entry_list(
        region: str | None = Field(description="请求的region", default=None),
        route_table_id: str = Field(description="待查询路由表的ID"),
        route_entry_type: Literal[
            "Custom",
        ] | None = Field(description="路由条目的类型", default=None),
        route_entry_id: str | None = Field(description="路由条目的ID", default=None),
        route_entry_name: str | None = Field(description="路由条目的名称", default=None),
        next_hop_type: Literal[
            "Instance",
            "HaVip",
            "NetworkInterface",
            "NatGW",
            "VpcPeer",
            "RegionGW",
            "TransitRouter",
            "IPv6GW",
            "CloudConnector",
            "GWLBEndpoint",
            "InstanceGroup",
        ] | None = Field(description="路由条目的下一跳的类型", default=None),
        next_hop_id: str | None = Field(description="路由条目的下一跳资源ID", default=None),
        destination_cidr_block: str | None = Field(description="路由条目的目标网段", default=None),
        destination_prefix_list_id: str | None = Field(description="前缀列表的ID", default=None),
        max_results: int = Field(description="查询的数量，默认为10，最大为100", default=10),
) -> list[RouteEntry]:
    try:
        response = client.get_client(region=region).describe_route_entry_list(
            models.DescribeRouteEntryListRequest(
                route_table_id=route_table_id,
                route_entry_type=route_entry_type,
                route_entry_id=route_entry_id,
                route_entry_name=route_entry_name,
                next_hop_type=next_hop_type,
                next_hop_id=next_hop_id,
                destination_cidr_block=destination_cidr_block,
                destination_prefix_list_id=destination_prefix_list_id,
                max_results=max_results,
            ))
        if not response or not response.route_entries:
            return []
        return [RouteEntry(
            description=i.description,
            destination_cidr_block=i.destination_cidr_block,
            route_entry_id=i.route_entry_id,
            route_entry_name=i.route_entry_name,
            route_table_id=i.route_table_id,
            status=i.status,
            type=i.type,
            vpc_id=i.vpc_id,
            next_hop_id=i.next_hop_id,
            next_hop_type=i.next_hop_type,
            prefix_list_cidr_blocks=i.prefix_list_cidr_blocks or [],
        ) for i in response.route_entries]
    except Exception as e:
        raise errors.VPCError("查询路由条目失败", e)
