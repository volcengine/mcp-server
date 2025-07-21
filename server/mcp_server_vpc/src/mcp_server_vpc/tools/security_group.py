"""
安全组工具.
"""

from typing import Literal

from pydantic import BaseModel
from pydantic import Field
from volcenginesdkvpc import models

from mcp_server_vpc.common import client
from mcp_server_vpc.common import errors
from mcp_server_vpc.server import mcp


class SecurityGroup(BaseModel):
    """安全组"""
    creation_time: str = Field(description="安全组的创建时间")
    description: str = Field(description="安全组描述信息")
    security_group_id: str = Field(description="安全组ID")
    security_group_name: str = Field(description="安全组名称")
    vpc_id: str = Field(description="安全组所属的VPC")
    status: str = Field(description="安全组的状态")
    type: str = Field(description="安全组的类型")
    service_managed: bool = Field(description="安全组是否为托管安全组")
    project_name: str = Field(description="安全组所属项目的名称")


class Permission(BaseModel):
    """安全组规则"""
    source_group_id: str = Field(description="安全组ID")
    direction: str = Field(description="授权方向")
    priority: int = Field(description="规则优先级")
    policy: str = Field(description="访问策略")
    protocol: str = Field(description="协议类型")
    port_start: int = Field(description="端口起始")
    port_end: int = Field(description="端口结束")
    cidr_ip: str = Field(description="IP地址段，用于安全组出入方向规则的授权")
    prefix_list_id: str = Field(description="前缀列表的ID")
    prefix_list_cidrs: list[str] = Field(description="前缀列表的CIDR")
    description: str = Field(description="安全组规则的描述信息")
    creation_time: str = Field(description="创建安全组规则的时间")
    update_time: str = Field(description="更新安全组规则的时间")


class SecurityGroupDetail(SecurityGroup):
    """安全组详情"""
    vpc_id: str = Field(description="VPC的ID")
    security_group_id: str = Field(description="目标安全组ID")
    security_group_name: str = Field(description="目标安全组名称")
    description: str = Field(description="安全组描述信息")
    type: str = Field(description="安全组的类型")
    service_managed: bool = Field(description="安全组是否为托管安全组")
    status: str = Field(description="安全组的状态")
    permissions: list[Permission] = Field(description="安全组规则集合")
    project_name: str = Field(description="安全组所在项目的名称")
    creation_time: str = Field(description="创建安全组的时间")
    update_time: str = Field(description="更新安全组的时间")


@mcp.tool(description="查询满足指定条件的安全组")
def describe_security_groups(
        region: str | None = Field(description="请求的region", default=None),
        vpc_id: str | None = Field(description="安全组所在VPC的ID", default=None),
        security_group_ids: list[str] | None = Field(
            description="安全组的ID列表，单次调用数量上限为100个", default=None),
        security_group_names: list[str] | None = Field(
            description="安全组名称列表，单次调用数量上限为100个", default=None),
        project_name: str | None = Field(description="安全组所属的项目", default=None),
        max_results: int = Field(description="查询的数量，默认为10，最大为100", default=10),
) -> list[SecurityGroup]:
    try:
        response = client.get_client(region=region).describe_security_groups(
            models.DescribeSecurityGroupsRequest(
                vpc_id=vpc_id,
                security_group_ids=security_group_ids,
                security_group_names=security_group_names,
                project_name=project_name,
                max_results=max_results,
            ))
        if not response or not response.security_groups:
            return []
        return [SecurityGroup(
            creation_time=sg.creation_time,
            description=sg.description,
            security_group_id=sg.security_group_id,
            security_group_name=sg.security_group_name,
            vpc_id=sg.vpc_id,
            status=sg.status,
            type=sg.type,
            service_managed=sg.service_managed,
            project_name=sg.project_name,
        ) for sg in response.security_groups]
    except Exception as e:
        raise errors.VPCError("查询安全组失败", e)


@mcp.tool(description="在指定安全组内查询满足指定条件的安全组规则")
def describe_security_group_attributes(
        region: str | None = Field(description="请求的region", default=None),
        security_group_id: str = Field(description="规则所属安全组的ID"),
        direction: Literal[
            "egress",
            "ingress",
        ] | None = Field(description="安全组规则授权方向", default=None),
        protocol: Literal[
            "tcp",
            "udp",
            "icmp",
            "icmpv6",
            "all",
        ] | None = Field(description="协议类型", default=None),
        cidr_ip: str | None = Field(description="IP地址段，用于安全组出入方向规则的授权", default=None),
        source_group_id: str | None = Field(description="源地址或目的地址的安全组ID", default=None),
        prefix_list_id: str | None = Field(description="前缀列表的ID", default=None),
) -> SecurityGroupDetail:
    try:
        response = client.get_client(region=region).describe_security_group_attributes(
            models.DescribeSecurityGroupAttributesRequest(
                security_group_id=security_group_id,
                direction=direction,
                protocol=protocol,
                cidr_ip=cidr_ip,
                source_group_id=source_group_id,
                prefix_list_id=prefix_list_id,
            ),
        )
        if not response or not response.security_group_id:
            raise errors.VPCError(f"未查询到安全组：{security_group_id}")
        return SecurityGroupDetail(
            vpc_id=response.vpc_id,
            security_group_id=response.security_group_id,
            security_group_name=response.security_group_name,
            description=response.description,
            type=response.type,
            service_managed=response.service_managed,
            status=response.status,
            permissions=[Permission(
                source_group_id=i.source_group_id,
                direction=i.direction,
                priority=i.priority,
                policy=i.policy,
                protocol=i.protocol,
                port_start=i.port_start,
                port_end=i.port_end,
                cidr_ip=i.cidr_ip,
                prefix_list_id=i.prefix_list_id,
                prefix_list_cidrs=i.prefix_list_cidrs or [],
                description=i.description,
                creation_time=i.creation_time,
                update_time=i.update_time,
            ) for i in response.permissions] if response.permissions else [],
            project_name=response.project_name,
            creation_time=response.creation_time,
            update_time=response.update_time,
        )
    except Exception as e:
        raise errors.VPCError("查询安全组详情失败", e)
