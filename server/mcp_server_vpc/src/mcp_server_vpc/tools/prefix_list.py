"""
前缀列表工具.
"""

from typing import Literal

from pydantic import BaseModel
from pydantic import Field
from volcenginesdkvpc import models

from mcp_server_vpc.common import client
from mcp_server_vpc.common import errors
from mcp_server_vpc.server import mcp


class PrefixList(BaseModel):
    """前缀列表"""
    prefix_list_id: str = Field(description="VPC前缀列表的ID")
    prefix_list_name: str = Field(description="VPC前缀列表名称")
    description: str = Field(description="VPC前缀列表描述信息")
    ip_version: str = Field(description="前缀列表的IP版本")
    max_entries: int = Field(description="最大条目数，即前缀列表做多可添加条目的数量")
    cidrs: list[str] = Field(description="前缀列表的CIDR地址块信息")
    status: str = Field(description="前缀列表的状态")
    project_name: str = Field(description="前缀列表所属项目的名称")
    creation_time: str = Field(description="VPC前缀列表的创建时间")
    update_time: str = Field(description="VPC前缀列表的修改时间")


class PrefixListAssociation(BaseModel):
    """前缀列表关联的资源"""
    resource_id: str = Field(description="关联的资源ID")
    resource_type: str = Field(description="关联的资源类型")


class PrefixListEntry(BaseModel):
    """前缀列表的前缀条目"""
    prefix_list_id: str = Field(description="前缀列表的ID")
    description: str = Field(description="前缀列表条目的描述信息")
    cidr: str = Field(description="前缀列表条目的CIDR地址块")


@mcp.tool(description="查询满足指定条件的前缀列表")
def describe_prefix_lists(
        region: str | None = Field(description="请求的region", default=None),
        prefix_list_ids: list[str] | None = Field(
            description="前缀列表的ID列表，单次调用数量上限为100个", default=None),
        prefix_list_name: str | None = Field(description="要查询的前缀列表的名称", default=None),
        ip_version: Literal[
            "IPv4",
            "IPv6",
        ] | None = Field(description="前缀列表的IP版本", default=None),
        project_name: str | None = Field(description="前缀列表所属的项目", default=None),
        max_results: int = Field(description="查询的数量，默认为10，最大为100", default=10),
) -> list[PrefixList]:
    """查询满足指定条件的前缀列表"""
    try:
        response = client.get_client(region=region).describe_prefix_lists(
            models.DescribePrefixListsRequest(
                prefix_list_ids=prefix_list_ids,
                prefix_list_name=prefix_list_name,
                ip_version=ip_version,
                project_name=project_name,
                max_results=max_results,
            ))
        if not response or not response.prefix_lists:
            return []
        return [PrefixList(
            prefix_list_id=i.prefix_list_id,
            prefix_list_name=i.prefix_list_name,
            description=i.description,
            ip_version=i.ip_version,
            max_entries=i.max_entries,
            cidrs=i.cidrs or [],
            status=i.status,
            project_name=i.project_name,
            creation_time=i.creation_time,
            update_time=i.update_time,
        ) for i in response.prefix_lists]
    except Exception as e:
        raise errors.VPCError("查询前缀列表失败", e)


@mcp.tool(description="查询指定前缀列表关联的资源")
def describe_prefix_list_associations(
        region: str | None = Field(description="请求的region", default=None),
        prefix_list_id: str = Field(description="前缀列表的ID"),
        resource_type: Literal[
            "VpcRouteTable",
            "VpcSecurityGroup",
        ] | None = Field(description="关联资源类型", default=None),
        max_results: int = Field(description="查询的数量，默认为10，最大为100", default=10),
) -> list[PrefixListAssociation]:
    """查询前缀列表的关联资源"""
    try:
        response = client.get_client(region=region).describe_prefix_list_associations(
            models.DescribePrefixListAssociationsRequest(
                prefix_list_id=prefix_list_id,
                resource_type=resource_type,
                max_results=max_results,
            ))
        if not response or not response.prefix_list_associations:
            return []
        return [PrefixListAssociation(
            resource_id=i.resource_id,
            resource_type=i.resource_type,
        ) for i in response.prefix_list_associations]
    except Exception as e:
        raise errors.VPCError("查询前缀列表关联资源失败", e)


@mcp.tool(description="查看指定前缀列表的前缀条目")
def describe_prefix_list_entries(
        region: str | None = Field(description="请求的region", default=None),
        prefix_list_id: str = Field(description="前缀列表的ID"),
        max_results: int = Field(description="查询的数量，默认为10，最大为100", default=10),
) -> list[PrefixListEntry]:
    """查询前缀列表的条目"""
    try:
        response = client.get_client(region=region).describe_prefix_list_entries(
            models.DescribePrefixListEntriesRequest(
                prefix_list_id=prefix_list_id,
                max_results=max_results,
            ))
        if not response or not response.prefix_list_entries:
            return []
        return [PrefixListEntry(
            prefix_list_id=i.prefix_list_id,
            description=i.description,
            cidr=i.cidr,
        ) for i in response.prefix_list_entries]
    except Exception as e:
        raise errors.VPCError("查询前缀列表条目失败", e)
