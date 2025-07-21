"""
私有网络工具.
"""

from pydantic import BaseModel
from pydantic import Field
from volcenginesdkvpc import models

from mcp_server_vpc.common import client
from mcp_server_vpc.common import errors
from mcp_server_vpc.server import mcp


class Vpc(BaseModel):
    """私有网络"""
    vpc_id: str = Field(description="VPC的ID")
    status: str = Field(description="VPC的状态")
    vpc_name: str = Field(description="VPC的名称")
    creation_time: str = Field(description="创建VPC的时间")
    update_time: str = Field(description="更新VPC的时间")
    cidr_block: str = Field(description="VPC的IPv4网段")
    description: str = Field(description="VPC的描述信息")
    dns_servers: list[str] = Field(description="DNS服务器")
    secondary_cidr_blocks: list[str] = Field(description="VPC的辅助网段")
    user_cidr_blocks: list[str] = Field(description="VPC的用户网段")
    project_name: str = Field(description="VPC所属项目的名称")


@mcp.tool(description="查询满足指定条件的VPC")
def describe_vpcs(
        region: str | None = Field(description="请求的region", default=None),
        vpc_ids: list[str] | None = Field(description="VPC的ID，单次调用数量上限为100个", default=None),
        vpc_name: str | None = Field(description="VPC的名称", default=None),
        project_name: str | None = Field(description="VPC所属项目的名称", default=None),
        max_results: int = Field(description="查询的数量，默认为10，最大为100", default=10),
) -> list[Vpc]:
    try:
        response = client.get_client(region=region).describe_vpcs(
            models.DescribeVpcsRequest(
                vpc_ids=vpc_ids,
                vpc_name=vpc_name,
                project_name=project_name,
                max_results=max_results,
            ))
        if not response or not response.vpcs:
            return []
        return [Vpc(
            vpc_id=i.vpc_id,
            status=i.status,
            vpc_name=i.vpc_name,
            creation_time=i.creation_time,
            update_time=i.update_time,
            cidr_block=i.cidr_block,
            description=i.description,
            dns_servers=i.dns_servers or [],
            secondary_cidr_blocks=i.secondary_cidr_blocks or [],
            user_cidr_blocks=i.user_cidr_blocks or [],
            project_name=i.project_name,
        ) for i in response.vpcs]
    except Exception as e:
        raise errors.VPCError("查询VPC失败", e)


@mcp.tool(description="查看指定VPC的详情")
def describe_vpc_attributes(
        region: str | None = Field(description="请求的region", default=None),
        vpc_id: str = Field(description="要查看的VPC的ID"),
) -> Vpc:
    try:
        response = client.get_client(region=region).describe_vpc_attributes(
            models.DescribeVpcAttributesRequest(vpc_id=vpc_id),
        )
        if not response or not response.vpc_id:
            raise errors.VPCError(f"未查询到VPC信息：{vpc_id}")
        return Vpc(
            vpc_id=response.vpc_id,
            status=response.status,
            vpc_name=response.vpc_name,
            creation_time=response.creation_time,
            update_time=response.update_time,
            cidr_block=response.cidr_block,
            description=response.description,
            dns_servers=response.dns_servers or [],
            secondary_cidr_blocks=response.secondary_cidr_blocks or [],
            user_cidr_blocks=response.user_cidr_blocks or [],
            project_name=response.project_name,
        )
    except Exception as e:
        raise errors.VPCError("查询VPC失败", e)
