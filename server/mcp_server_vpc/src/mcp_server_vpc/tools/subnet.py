"""
子网工具.
"""

from pydantic import BaseModel
from pydantic import Field
from volcenginesdkvpc import models

from mcp_server_vpc.common import client
from mcp_server_vpc.common import errors
from mcp_server_vpc.server import mcp


class RouteTableInfo(BaseModel):
    """路由表信息"""
    route_table_id: str = Field(description="子网关联的路由表ID")
    route_table_type: str = Field(description="子网关联的路由表的类型")


class Subnet(BaseModel):
    """子网"""
    subnet_id: str = Field(description="子网的ID")
    vpc_id: str = Field(description="子网所属VPC的ID")
    status: str = Field(description="子网的状态")
    cidr_block: str = Field(description="子网的IPv4网段")
    ipv6_cidr_block: str = Field(description="子网的IPv6网段")
    zone_id: str = Field(description="子网所属的可用区")
    description: str = Field(description="子网的描述信息")
    subnet_name: str = Field(description="子网的名称")
    creation_time: str = Field(description="子网的创建时间")
    update_time: str = Field(description="子网的更新的时间")
    network_acl_id: str = Field(description="子网关联的网络ACL的ID")
    route_table: RouteTableInfo = Field(description="路由表信息")
    project_name: str = Field(description="子网所属项目的名称")


@mcp.tool(description="查询满足指定条件的子网")
def describe_subnets(
        region: str | None = Field(description="请求的region", default=None),
        zone_id: str | None = Field(description="子网所属可用区的ID", default=None),
        vpc_id: str | None = Field(description="子网所属VPC的ID", default=None),
        subnet_ids: list[str] | None = Field(description="子网的ID，单次调用数量上限为100个", default=None),
        subnet_name: str | None = Field(description="子网的名称", default=None),
        route_table_id: str | None = Field(description="子网关联路由表的ID", default=None),
        project_name: str | None = Field(description="子网所在VPC实例所属项目的名称", default=None),
        max_results: int = Field(description="查询的数量，默认为10，最大为100", default=10),
) -> list[Subnet]:
    try:
        response = client.get_client(region=region).describe_subnets(
            models.DescribeSubnetsRequest(
                zone_id=zone_id,
                vpc_id=vpc_id,
                subnet_ids=subnet_ids,
                subnet_name=subnet_name,
                route_table_id=route_table_id,
                project_name=project_name,
                max_results=max_results,
            ))
        if not response or not response.subnets:
            return []
        return [Subnet(
            subnet_id=i.subnet_id,
            vpc_id=i.vpc_id,
            status=i.status,
            cidr_block=i.cidr_block,
            ipv6_cidr_block=i.ipv6_cidr_block,
            zone_id=i.zone_id,
            description=i.description,
            subnet_name=i.subnet_name,
            creation_time=i.creation_time,
            update_time=i.update_time,
            network_acl_id=i.network_acl_id,
            route_table=RouteTableInfo(
                route_table_id=i.route_table.route_table_id,
                route_table_type=i.route_table.route_table_type,
            ) if i.route_table else None,
            project_name=i.project_name,
        ) for i in response.subnets]
    except Exception as e:
        raise errors.VPCError("查询子网失败", e)


@mcp.tool(description="查看指定子网的详细信息")
def describe_subnet_attributes(
        region: str | None = Field(description="请求的region", default=None),
        subnet_id: str = Field(description="子网的ID"),
) -> Subnet:
    try:
        response = client.get_client(region=region).describe_subnet_attributes(
            models.DescribeSubnetAttributesRequest(subnet_id=subnet_id),
        )
        if not response or not response.subnet_id:
            raise errors.VPCError(f"未查询到子网：{subnet_id}")
        return Subnet(
            subnet_id=response.subnet_id,
            vpc_id=response.vpc_id,
            status=response.status,
            cidr_block=response.cidr_block,
            ipv6_cidr_block=response.ipv6_cidr_block,
            zone_id=response.zone_id,
            description=response.description,
            subnet_name=response.subnet_name,
            creation_time=response.creation_time,
            update_time=response.update_time,
            network_acl_id=response.network_acl_id,
            route_table=RouteTableInfo(
                route_table_id=response.route_table.route_table_id,
                route_table_type=response.route_table.route_table_type,
            ) if response.route_table else None,
            project_name=response.project_name,
        )
    except Exception as e:
        raise errors.VPCError("查询子网详情失败", e)
