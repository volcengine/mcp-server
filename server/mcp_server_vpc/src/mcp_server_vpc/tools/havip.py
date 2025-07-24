"""
高可用虚拟IP工具.
"""

from typing import Literal

from pydantic import BaseModel
from pydantic import Field
from volcenginesdkvpc import models

from mcp_server_vpc.common import client
from mcp_server_vpc.common import errors
from mcp_server_vpc.server import mcp


class HaVip(BaseModel):
    """高可用虚拟IP"""
    created_at: str = Field(description="创建HAVIP的时间")
    updated_at: str = Field(description="更新HAVIP的时间")
    status: str = Field(description="HAVIP的状态")
    description: str = Field(description="HAVIP的描述信息")
    ha_vip_id: str = Field(description="HAVIP的ID")
    ha_vip_name: str = Field(description="HAVIP的名称")
    ip_address: str = Field(description="HAVIP的IP地址")
    master_instance_id: str = Field(description="与HAVIP绑定的主实例的ID")
    vpc_id: str = Field(description="HAVIP所属私有网络的ID")
    subnet_id: str = Field(description="HAVIP所属子网的ID")
    associated_instance_type: str = Field(description="绑定HAVIP的实例类型")
    associated_instance_ids: list[str] = Field(description="绑定HAVIP的实例ID列表")
    associated_eip_id: str = Field(description="HAVIP绑定的公网IP的ID")
    associated_eip_address: str = Field(description="HAVIP绑定的公网IP的IP地址")
    project_name: str = Field(description="HAVIP的项目名称")


@mcp.tool(description="查询满足指定条件的高可用虚拟IP（HAVIP）")
def describe_ha_vips(
        region: str | None = Field(description="请求的region", default=None),
        vpc_id: str | None = Field(description="HAVIP所属私有网络的ID", default=None),
        subnet_id: str | None = Field(description="HAVIP所属子网的ID", default=None),
        ip_address: str | None = Field(description="HAVIP的IP地址", default=None),
        ha_vip_ids: list[str] | None = Field(description="HAVIP的ID，单次调用数量上限为100个", default=None),
        ha_vip_name: str | None = Field(description="HAVIP的名称", default=None),
        status: Literal[
            "Available",
            "Creating",
            "InUse",
            "Deleting",
        ] | None = Field(description="HAVIP的状态", default=None),
        project_name: str | None = Field(description="HAVIP的项目名称", default=None),
        max_results: int = Field(description="查询的数量，默认为10，最大为100", default=10),
) -> list[HaVip]:
    try:
        response = client.get_client(region=region).describe_ha_vips(
            models.DescribeHaVipsRequest(
                vpc_id=vpc_id,
                subnet_id=subnet_id,
                ip_address=ip_address,
                ha_vip_ids=ha_vip_ids,
                ha_vip_name=ha_vip_name,
                status=status,
                project_name=project_name,
                max_results=max_results,
            ))
        if not response or not response.ha_vips:
            return []
        return [HaVip(
            created_at=i.created_at,
            updated_at=i.updated_at,
            status=i.status,
            description=i.description,
            ha_vip_id=i.ha_vip_id,
            ha_vip_name=i.ha_vip_name,
            ip_address=i.ip_address,
            master_instance_id=i.master_instance_id,
            vpc_id=i.vpc_id,
            subnet_id=i.subnet_id,
            associated_instance_type=i.associated_instance_type,
            associated_instance_ids=i.associated_instance_ids or [],
            associated_eip_id=i.associated_eip_id,
            associated_eip_address=i.associated_eip_address,
            project_name=i.project_name,
        ) for i in response.ha_vips]
    except Exception as e:
        raise errors.VPCError("查询高可用虚拟IP失败", e)
