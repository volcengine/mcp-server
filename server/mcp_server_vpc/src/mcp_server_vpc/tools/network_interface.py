"""
网卡工具.
"""

from typing import Literal

from pydantic import BaseModel
from pydantic import Field
from volcenginesdkvpc import models

from mcp_server_vpc.common import client
from mcp_server_vpc.common import errors
from mcp_server_vpc.server import mcp


class AssociatedElasticIp(BaseModel):
    """网卡关联的公网IP"""
    allocation_id: str = Field(description="公网IP的ID")
    eip_address: str = Field(description="公网IP的地址")


class PrivateIpSet(BaseModel):
    """网卡的私有IP"""
    private_ip_address: str = Field(description="网卡的私网IPv4地址")
    primary: bool = Field(description="是否为主私网IPv4地址")
    associated_elastic_ip: AssociatedElasticIp | None = Field(description="网卡辅助私网IPv4地址关联的公网IP")


class NetworkInterface(BaseModel):
    """网卡"""
    network_interface_id: str = Field(description="网卡ID")
    network_interface_name: str = Field(description="网卡名称")
    description: str = Field(description="网卡描述信息")
    vpc_id: str = Field(description="网卡所属VPC的ID")
    zone_id: str = Field(description="网卡所属可用区的ID")
    subnet_id: str = Field(description="网卡所属子网的ID")
    mac_address: str = Field(description="网卡的Mac地址")
    device_id: str = Field(description="网卡绑定实例的ID")
    type: str = Field(description="网卡的类型")
    primary_ip_address: str = Field(description="网卡的主私网IPv4地址")
    associated_elastic_ip: AssociatedElasticIp | None = Field(description="网卡主私网IPv4地址绑定的公网IP的信息")
    private_ip_sets: list[PrivateIpSet] = Field(description="网卡私网IPv4地址列表")
    ipv6_sets: list[str] = Field(description="网卡的IPv6地址列表")
    status: str = Field(description="网卡的绑定状态")
    port_security_enabled: bool = Field(description="是否为网卡开启源/目的地址检查")
    service_managed: bool = Field(description="是否为火山引擎官方服务网卡")
    security_group_ids: list[str] = Field(description="网卡关联的安全组ID")
    project_name: str = Field(description="网卡所属项目的名称")
    created_at: str = Field(description="创建网卡的时间")
    updated_at: str = Field(description="更新网卡的时间")


@mcp.tool(description="查询满足指定条件的网卡")
def describe_network_interfaces(
        region: str | None = Field(description="请求的region", default=None),
        network_interface_name: str | None = Field(description="网卡的名称", default=None),
        network_interface_ids: list[str] | None = Field(
            description="网卡的ID，单次调用数量上限为100个", default=None),
        type: Literal[
            "primary",
            "secondary",
        ] | None = Field(description="网卡类型", default=None),
        instance_id: str | None = Field(description="网卡挂载的云服务器ID", default=None),
        vpc_id: str | None = Field(description="网卡所属VPC的ID", default=None),
        subnet_id: str | None = Field(description="网卡所属子网的ID", default=None),
        primary_ip_addresses: list[str] | None = Field(description="网卡的主私网IPv4地址", default=None),
        private_ip_addresses: list[str] | None = Field(description="网卡的辅助私网IPv4地址", default=None),
        ipv6_addresses: list[str] | None = Field(description="网卡的私网IPv6地址", default=None),
        security_group_id: str | None = Field(description="网卡关联安全组的ID", default=None),
        status: Literal[
            "Creating",
            "Available",
            "Attaching",
            "InUse",
            "Detaching",
            "Deleting",
        ] | None = Field(description="网卡状态", default=None),
        project_name: str | None = Field(description="网卡所属的项目", default=None),
        max_results: int = Field(description="查询的数量，默认为10，最大为100", default=10),
) -> list[NetworkInterface]:
    try:
        response = client.get_client(region=region).describe_network_interfaces(
            models.DescribeNetworkInterfacesRequest(
                network_interface_ids=network_interface_ids,
                network_interface_name=network_interface_name,
                type=type,
                instance_id=instance_id,
                vpc_id=vpc_id,
                subnet_id=subnet_id,
                primary_ip_addresses=primary_ip_addresses,
                private_ip_addresses=private_ip_addresses,
                ipv6_addresses=ipv6_addresses,
                security_group_id=security_group_id,
                status=status,
                project_name=project_name,
                max_results=max_results,
            ))
        if not response or not response.network_interface_sets:
            return []
        return [NetworkInterface(
            network_interface_id=i.network_interface_id,
            network_interface_name=i.network_interface_name,
            description=i.description,
            vpc_id=i.vpc_id,
            zone_id=i.zone_id,
            subnet_id=i.subnet_id,
            mac_address=i.mac_address,
            device_id=i.device_id,
            type=i.type,
            primary_ip_address=i.primary_ip_address,
            associated_elastic_ip=AssociatedElasticIp(
                allocation_id=i.associated_elastic_ip.allocation_id,
                eip_address=i.associated_elastic_ip.eip_address,
            ) if i.associated_elastic_ip else None,
            private_ip_sets=[PrivateIpSet(
                private_ip_address=j.private_ip_address,
                primary=j.primary,
                associated_elastic_ip=AssociatedElasticIp(
                    allocation_id=j.associated_elastic_ip.allocation_id,
                    eip_address=j.associated_elastic_ip.eip_address,
                ) if j.associated_elastic_ip else None,
            ) for j in i.private_ip_sets.private_ip_set]
            if i.private_ip_sets and i.private_ip_sets.private_ip_set else [],
            ipv6_sets=i.i_pv6_sets or [],
            status=i.status,
            port_security_enabled=i.port_security_enabled,
            service_managed=i.service_managed,
            security_group_ids=i.security_group_ids or [],
            project_name=i.project_name,
            created_at=i.created_at,
            updated_at=i.updated_at,
        ) for i in response.network_interface_sets]
    except Exception as e:
        raise errors.VPCError("查询弹性网卡失败", e)


@mcp.tool(description="查看指定网卡的详情")
def describe_network_interface_attributes(
        region: str | None = Field(description="请求的region", default=None),
        network_interface_id: str = Field(description="网卡的ID"),
) -> NetworkInterface:
    try:
        response = client.get_client(region=region).describe_network_interface_attributes(
            models.DescribeNetworkInterfaceAttributesRequest(
                network_interface_id=network_interface_id,
            ),
        )
        if not response or not response.network_interface_id:
            raise errors.VPCError(f"未查询到弹性网卡：{network_interface_id}")
        return NetworkInterface(
            network_interface_id=response.network_interface_id,
            network_interface_name=response.network_interface_name,
            description=response.description,
            vpc_id=response.vpc_id,
            zone_id=response.zone_id,
            subnet_id=response.subnet_id,
            mac_address=response.mac_address,
            device_id=response.device_id,
            type=response.type,
            primary_ip_address=response.primary_ip_address,
            associated_elastic_ip=AssociatedElasticIp(
                allocation_id=response.associated_elastic_ip.allocation_id,
                eip_address=response.associated_elastic_ip.eip_address,
            ) if response.associated_elastic_ip else None,
            private_ip_sets=[PrivateIpSet(
                private_ip_address=i.private_ip_address,
                primary=i.primary,
                associated_elastic_ip=AssociatedElasticIp(
                    allocation_id=i.associated_elastic_ip.allocation_id,
                    eip_address=i.associated_elastic_ip.eip_address,
                ) if i.associated_elastic_ip else None,
            ) for i in response.private_ip_sets.private_ip_set]
            if response.private_ip_sets and response.private_ip_sets.private_ip_set else [],
            ipv6_sets=response.i_pv6_sets or [],
            status=response.status,
            port_security_enabled=response.port_security_enabled,
            service_managed=response.service_managed,
            security_group_ids=response.security_group_ids or [],
            project_name=response.project_name,
            created_at=response.created_at,
            updated_at=response.updated_at,
        )
    except Exception as e:
        raise errors.VPCError("查询弹性网卡详情失败", e)
