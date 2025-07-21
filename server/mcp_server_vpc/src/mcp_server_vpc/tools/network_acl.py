"""
网络ACL工具.
"""

from pydantic import BaseModel
from pydantic import Field
from volcenginesdkvpc import models

from mcp_server_vpc.common import client
from mcp_server_vpc.common import errors
from mcp_server_vpc.server import mcp


class IngressAclEntry(BaseModel):
    """网络ACL入方向规则"""
    network_acl_entry_id: str = Field(description="入方向规则的ID")
    network_acl_entry_name: str = Field(description="入方向规则的名称")
    description: str = Field(description="入方向规则的描述信息")
    policy: str = Field(description="入方向规则的授权策略")
    source_cidr_ip: str = Field(description="源地址的网段")
    protocol: str = Field(description="协议类型")
    priority: int = Field(description="入方向规则的优先级，数字越小，代表优先级越高")
    port: str = Field(description="入方向规则的目的端口范围")


class EgressAclEntry(BaseModel):
    """网络ACL出方向规则"""
    network_acl_entry_id: str = Field(description="出方向规则的ID")
    network_acl_entry_name: str = Field(description="出方向规则的名称")
    description: str = Field(description="出方向规则的描述信息")
    policy: str = Field(description="授权策略")
    destination_cidr_ip: str = Field(description="目标地址的网段")
    protocol: str = Field(description="协议类型")
    priority: int = Field(description="出方向规则的优先级，数字越小，代表优先级越高")
    port: str = Field(description="出方向规则的目的端口范围")


class Resource(BaseModel):
    """网络ACL关联资源"""
    resource_id: str = Field(description="网络ACL关联资源的ID")
    status: str = Field(description="网络ACL关联资源的状态")


class NetworkAcl(BaseModel):
    """网络ACL"""
    network_acl_id: str = Field(description="网络ACL的ID")
    network_acl_name: str = Field(description="网络ACL的名称")
    description: str = Field(description="网络ACL的描述信息")
    vpc_id: str = Field(description="网络ACL所属的VPC")
    ingress_acl_entries: list[IngressAclEntry] = Field(description="网络ACL入方向规则的信息")
    egress_acl_entries: list[EgressAclEntry] = Field(description="网络ACL出方向规则的详细信息")
    resources: list[Resource] = Field(description="网络ACL关联资源的详细信息")
    status: str = Field(description="网络ACL的状态")
    project_name: str = Field(description="网络ACL所属项目的名称")
    creation_time: str = Field(description="创建网络ACL的时间")
    update_time: str = Field(description="更新网络ACL的时间")


@mcp.tool(description="查询满足指定条件的网络ACL")
def describe_network_acls(
        region: str | None = Field(description="请求的region", default=None),
        vpc_id: str | None = Field(description="网络ACL所属VPC的ID", default=None),
        network_acl_ids: list[str] | None = Field(
            description="网络ACL的ID，单次调用数量上限为100个", default=None),
        subnet_id: str | None = Field(description="网络ACL关联的子网的ID", default=None),
        network_acl_name: str | None = Field(description="网络ACL的名称", default=None),
        project_name: str | None = Field(description="网络ACL所属的项目", default=None),
        max_results: int = Field(description="查询的数量，默认为10，最大为100", default=10),
) -> list[NetworkAcl]:
    try:
        response = client.get_client(region=region).describe_network_acls(
            models.DescribeNetworkAclsRequest(
                vpc_id=vpc_id,
                network_acl_ids=network_acl_ids,
                subnet_id=subnet_id,
                network_acl_name=network_acl_name,
                project_name=project_name,
                max_results=max_results,
            ))
        if not response or not response.network_acls:
            return []
        return [NetworkAcl(
            network_acl_id=i.network_acl_id,
            network_acl_name=i.network_acl_name,
            description=i.description,
            vpc_id=i.vpc_id,
            ingress_acl_entries=[IngressAclEntry(
                network_acl_entry_id=j.network_acl_entry_id,
                network_acl_entry_name=j.network_acl_entry_name,
                description=j.description,
                policy=j.policy,
                source_cidr_ip=j.source_cidr_ip,
                protocol=j.protocol,
                priority=j.priority,
                port=j.port,
            ) for j in i.ingress_acl_entries] if i.ingress_acl_entries else [],
            egress_acl_entries=[EgressAclEntry(
                network_acl_entry_id=j.network_acl_entry_id,
                network_acl_entry_name=j.network_acl_entry_name,
                description=j.description,
                policy=j.policy,
                destination_cidr_ip=j.destination_cidr_ip,
                protocol=j.protocol,
                priority=j.priority,
                port=j.port,
            ) for j in i.egress_acl_entries] if i.egress_acl_entries else [],
            resources=[Resource(
                resource_id=j.resource_id,
                status=j.status,
            ) for j in i.resources] if i.resources else [],
            status=i.status,
            project_name=i.project_name,
            creation_time=i.creation_time,
            update_time=i.update_time,
        ) for i in response.network_acls]
    except Exception as e:
        raise errors.VPCError("查询网络ACL失败", e)


@mcp.tool(description="查看指定网络ACL的详情")
def describe_network_acl_attributes(
        region: str | None = Field(description="请求的region", default=None),
        network_acl_id: str = Field(description="待查看网络ACL的ID"),
) -> NetworkAcl:
    try:
        response = client.get_client(region=region).describe_network_acl_attributes(
            models.DescribeNetworkAclAttributesRequest(network_acl_id=network_acl_id),
        )
        acl = response.network_acl_attribute
        if not response or not acl or not acl.network_acl_id:
            raise errors.VPCError(f"未查询到网络ACL：{network_acl_id}")
        return NetworkAcl(
            network_acl_id=acl.network_acl_id,
            network_acl_name=acl.network_acl_name,
            description=acl.description,
            vpc_id=acl.vpc_id,
            ingress_acl_entries=[IngressAclEntry(
                network_acl_entry_id=i.network_acl_entry_id,
                network_acl_entry_name=i.network_acl_entry_name,
                description=i.description,
                policy=i.policy,
                source_cidr_ip=i.source_cidr_ip,
                protocol=i.protocol,
                priority=i.priority,
                port=i.port,
            ) for i in acl.ingress_acl_entries] if acl.ingress_acl_entries else [],
            egress_acl_entries=[EgressAclEntry(
                network_acl_entry_id=i.network_acl_entry_id,
                network_acl_entry_name=i.network_acl_entry_name,
                description=i.description,
                policy=i.policy,
                destination_cidr_ip=i.destination_cidr_ip,
                protocol=i.protocol,
                priority=i.priority,
                port=i.port,
            ) for i in acl.egress_acl_entries] if acl.egress_acl_entries else [],
            resources=[Resource(
                resource_id=i.resource_id,
                status=i.status,
            ) for i in acl.resources] if acl.resources else [],
            status=acl.status,
            project_name=acl.project_name,
            creation_time=acl.creation_time,
            update_time=acl.update_time,
        )
    except Exception as e:
        raise errors.VPCError("查询网络ACL详情失败", e)
