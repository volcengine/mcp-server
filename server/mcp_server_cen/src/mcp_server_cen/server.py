import logging
import os

from typing import Any, List, Optional, Dict
from mcp.server.fastmcp import FastMCP
from mcp_server_cen.base.cen import CENSDK

logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("CEN MCP Server", port=int(os.getenv("PORT", "8000")))

cen_resource = CENSDK()


@mcp.tool(
    name="describe_cens",
    description="根据CEN实例的ID、名称或项目名称查询满足条件的CEN实例的详细信息"
)
def describe_cens(
        cen_ids: Optional[List[str]] = None,
        cen_name: Optional[str] = None,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
        project_name: Optional[List[str]] = None,
        tag_filters: Optional[List[Dict[str, str]]] = None
) -> dict[str, Any]:
    """
    调用 DescribeCens 接口，查询满足指定条件的CEN实例。
    Args:
        cen_ids Optional(List[str]): CEN实例的ID列表。
        cen_name Optional(List[str]): CEN实例的名称。
        page_number Optional(int): 分页查询列表的页码。默认值为1。
        page_size Optional(int): 分页查询时每页的行数。取值范围为1～100，默认值为20。
        project_name Optional(List[str]): CEN实例所属项目的名称列表。
        tag_filters Optional(list[TagFilterForDescribeCensInput]): 标签键值对列表。
    Returns:
        dict[str, Any]: CEN实例的详细信息。
    """
    req = {
        "cen_ids": cen_ids,
        "cen_name": cen_name,
        "page_number": page_number,
        "page_size": page_size,
        "project_name": project_name,
        "tag_filters": tag_filters
    }

    resp = cen_resource.describe_cens(req)
    return resp.to_dict()


@mcp.tool(
    name="describe_cen_attributes",
    description="根据CEN实例的ID查询CEN实例的详细信息，也可以使用describe_cens进行查询"
)
def describe_cen_attributes(
        cen_id: str = None) -> dict[str, Any]:
    """
    调用 DescribeCenAttributes 接口，查询CEN实例的详细信息。
    Args:
        cen_id (str): 要查看的CEN实例的ID。
    Returns:
        dict[str, Any]: CEN实例的详细信息。
    Raises:
        ValueError: CEN实例的ID不能为空。
    """
    req = {
        "cen_id": cen_id
    }

    resp = cen_resource.describe_cen_attributes(req)
    return resp.to_dict()


@mcp.tool(
    name="describe_instance_granted_rules",
    description="查看满足指定条件的网络实例的跨账号授权信息,即本账号的网络实例授权给其他账号CEN实例的详细信息"
)
def describe_instance_granted_rules(
        instance_id: Optional[str] = None,
        instance_region_id: Optional[str] = None,
        instance_type: Optional[str] = None,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None) -> dict[str, Any]:
    """
    调用 DescribeInstanceGrantedRules 接口，查看满足指定条件的网络实例的跨账号授权信息。
    Args:
        instance_id (str): 网络实例所属账号的ID。
        instance_region_id (str): 网络实例所在的地域。
        instance_type (str): 网络实例的类型，如 VPC：私有网络；DCGW：专线网关。
        page_number Optional(int): 分页查询列表的页码。默认值为1。
        page_size Optional(int): 分页查询时每页的行数。取值范围为1～100，默认值为20。
    Returns:
        dict[str, Any]: 实例关联的CEN实例的详细信息。
    Raises:
        ValueError: 实例的ID不能为空。
    """
    req = {
        "instance_id": instance_id,
        "instance_region_id": instance_region_id,
        "instance_type": instance_type,
        "page_number": page_number,
        "page_size": page_size,
    }

    resp = cen_resource.describe_instance_granted_rules(req)
    return resp.to_dict()


@mcp.tool(
    name="describe_grant_rules_to_cen",
    description="查询本账号指定云企业网实例接受其他账号网络实例授权的信息"
)
def describe_grant_rules_to_cen(
        cen_id: str = None,
        instance_owner_id: Optional[str] = None,
        instance_region_id: Optional[str] = None,
        instance_type: Optional[str] = None,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None) -> dict[str, Any]:
    """
    调用 DescribeGrantRulesToCen 接口，查询本账号云企业网实例接受其他账号网络实例授权的信息。
    Args:
        cen_id (str): 要查看的CEN实例的ID。
        instance_owner_id Optional(str): 网络实例所属账号的ID。
        instance_region_id Optional(str): 网络实例所在的地域。
        instance_type Optional(str): 网络实例的类型，如 VPC：私有网络；DCGW：专线网关。
        page_number Optional(int): 分页查询列表的页码。默认值为1。
        page_size Optional(int): 分页查询时每页的行数。取值范围为1～100，默认值为20。
    Returns:
        dict[str, Any]: CEN实例关联的实例的详细信息。
    Raises:
        ValueError: CEN实例的ID不能为空。
    """
    req = {
        "cen_id": cen_id,
        "instance_owner_id": instance_owner_id,
        "instance_region_id": instance_region_id,
        "instance_type": instance_type,
        "page_number": page_number,
        "page_size": page_size,
    }

    resp = cen_resource.describe_grant_rules_to_cen(req)
    return resp.to_dict()


@mcp.tool(
    name="describe_cen_attached_instance_attributes",
    description="查看指定网络实例的详情"
)
def describe_cen_attached_instance_attributes(
        cen_id: str = None,
        instance_id: str = None,
        instance_region_id: str = None,
        instance_type: str = None) -> dict[str, Any]:
    """
    调用 DescribeCenAttachedInstanceAttributes 接口，查询网络实例的详细信息。
    Args:
        cen_id (str): 要查看的CEN实例的ID。
        instance_id (str): 网络实例的ID。
        instance_region_id (str): 网络实例所在的地域。
        instance_type (str): 网络实例的类型，取值如下：VPC：私有网络；DCGW：专线网关。
    Returns:
        dict[str, Any]: CEN实例关联的实例的详细信息。
    Raises:
        ValueError: CEN实例的ID不能为空。
    """
    req = {
        "cen_id": cen_id,
        "instance_id": instance_id,
        "instance_region_id": instance_region_id,
        "instance_type": instance_type,
    }

    resp = cen_resource.describe_cen_attached_instance_attributes(req)
    return resp.to_dict()


@mcp.tool(
    name="describe_cen_attached_instances",
    description="查询满足指定条件的网络实例列表,支持根据CEN实例ID、实例ID、实例区域ID、实例类型查询"
)
def describe_cen_attached_instances(
        cen_id: Optional[str] = None,
        instance_id: Optional[str] = None,
        instance_region_id: Optional[str] = None,
        instance_type: Optional[str] = None,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None) -> dict[str, Any]:
    """
    调用 DescribeCenAttachedInstances 接口，查询网络实例列表。
    Args:
        cen_id (str): 要查看的CEN实例的ID。
        instance_id (str): 实例ID。
        instance_region_id (str): 实例所在的区域ID。
        instance_type (str): 实例的类型。
        page_number Optional(int): 分页查询列表的页码。默认值为1。
        page_size Optional(int): 分页查询时每页的行数。取值范围为1～100，默认值为20。
    Returns:
        dict[str, Any]: CEN实例关联的实例的详细信息。
    Raises:
        ValueError: CEN实例的ID不能为空。
    """
    req = {
        "cen_id": cen_id,
        "instance_id": instance_id,
        "instance_region_id": instance_region_id,
        "instance_type": instance_type,
        "page_number": page_number,
        "page_size": page_size,
    }

    resp = cen_resource.describe_cen_attached_instances(req)
    return resp.to_dict()


@mcp.tool(
    name="describe_cen_bandwidth_packages",
    description="查询满足指定条件的带宽包信息,支持根据CEN实例ID、带宽包ID、带宽包名称、本地区域ID、对端区域ID、项目名称、标签筛选查询"
)
def describe_cen_bandwidth_packages(
        cen_bandwidth_package_ids: Optional[str] = None,
        cen_bandwidth_package_name: Optional[str] = None,
        cen_id: Optional[str] = None,
        local_geographic_region_set_id: Optional[str] = None,
        peer_geographic_region_set_id: Optional[str] = None,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
        project_name: Optional[str] = None,
        tag_filters: Optional[List[str]] = None) -> dict[str, Any]:
    """
    调用 DescribeCenBandwidthPackages 接口，查询满足指定条件的带宽包信息。
    Args:
        cen_id (str): 绑定的云企业网实例ID。
        cen_bandwidth_package_ids (str): 带宽包的ID列表。
        cen_bandwidth_package_name (str): 带宽包的名称。
        local_geographic_region_set_id (str): 云企业网互通的本端地理区域ID。
        peer_geographic_region_set_id (str): 云企业网互通的对端地理区域ID。
        page_number Optional(int): 分页查询列表的页码。默认值为1。
        page_size Optional(int): 分页查询时每页的行数。取值范围为1～100，默认值为20。
        project_name (str): 带宽包所属项目的名称。
        tag_filters (List[str]): 标签筛选条件。
    Returns:
        dict[str, Any]: CEN实例关联的带宽包的详细信息。
    """
    req = {
        "cen_id": cen_id,
        "cen_bandwidth_package_ids": cen_bandwidth_package_ids,
        "cen_bandwidth_package_name": cen_bandwidth_package_name,
        "local_geographic_region_set_id": local_geographic_region_set_id,
        "peer_geographic_region_set_id": peer_geographic_region_set_id,
        "page_number": page_number,
        "page_size": page_size,
        "project_name": project_name,
        "tag_filters": tag_filters,
    }

    resp = cen_resource.describe_cen_bandwidth_packages(req)
    return resp.to_dict()


@mcp.tool(
    name="describe_cen_bandwidth_package_attributes",
    description="查询指定带宽包实例的详细信息,支持根据带宽包ID查询"
)
def describe_cen_bandwidth_package_attributes(
        cen_bandwidth_package_id: str = None) -> dict[str, Any]:
    """
    调用 DescribeCenBandwidthPackageAttributes 接口，查询指定带宽包实例的详细信息。
    Args:
        cen_bandwidth_package_id (str): 带宽包ID。
    Returns:    
        dict[str, Any]: 带宽包的详细信息。
    """
    req = {
        "cen_bandwidth_package_id": cen_bandwidth_package_id
    }

    resp = cen_resource.describe_cen_bandwidth_package_attributes(req)
    return resp.to_dict()

@mcp.tool(
    name="describe_cen_bandwidth_packages_billing",
    description="查询满足指定条件的带宽包实例计费相关信息"
)
def describe_cen_bandwidth_packages_billing(
        cen_bandwidth_package_ids: str = None) -> dict[str, Any]:
    """
    调用 DescribeCenBandwidthPackagesBilling 接口，查询满足指定条件的带宽包实例计费相关信息。
    Args:
        cen_bandwidth_package_ids (str): 要查看的带宽包的ID。
    Returns:
        dict[str, Any]: 带宽包的计费信息。
    """
    req = {
        'cen_bandwidth_package_ids': cen_bandwidth_package_ids
    }

    resp = cen_resource.describe_cen_bandwidth_packages_billing(req)
    return resp.to_dict()

@mcp.tool(
    name="describe_cen_inter_region_bandwidth_attributes",
    description="查询指定云企业网实例域间带宽的详细信息,支持根据CEN域间带宽的ID查询"
)
def describe_cen_inter_region_bandwidth_attributes(
        inter_region_bandwidth_id: str = None) -> dict[str, Any]:
    """
    调用 DescribeCenInterRegionBandwidthAttributes 接口，查询指定云企业网实例域间带宽的详细信息。
    Args:
        inter_region_bandwidth_id (str): CEN域间带宽的ID。
    Returns:    
        dict[str, Any]: 跨区域带宽的详细信息。
    """
    req = {
        "inter_region_bandwidth_id": inter_region_bandwidth_id
    }

    resp = cen_resource.describe_cen_inter_region_bandwidth_attributes(req)
    return resp.to_dict()

@mcp.tool(
    name="describe_cen_inter_region_bandwidths",
    description="查询满足指定条件的云企业网实例域间带宽的列表"
)
def describe_cen_inter_region_bandwidths(
        cen_id: Optional[str] = None,
        inter_region_bandwidth_ids: Optional[list[str]] = None,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None) -> dict[str, Any]:
    """
    调用 DescribeCenInterRegionBandwidths 接口，查询满足指定条件的云企业网实例域间带宽的列表。
    Args:
        cen_id (str): 云企业网实例的ID。
        inter_region_bandwidth_ids (list[str]): CEN域间带宽的ID。
        page_number Optional(int): 分页查询列表的页码。默认值为1。
        page_size Optional(int): 分页查询时每页的行数。取值范围为1～100，默认值为20。
    Returns:
        dict[str, Any]: 跨区域带宽的详细信息。
    """
    req = {
        "cen_id": cen_id,
        "inter_region_bandwidth_ids": inter_region_bandwidth_ids,
        "page_number": page_number,
        "page_size": page_size
    }

    resp = cen_resource.describe_cen_inter_region_bandwidths(req)
    return resp.to_dict()

@mcp.tool(
    name="describe_cen_service_route_entries",
    description="查询满足指定条件的云服务访问路由的详细信息,支持根据CEN实例ID、云服务的地址段、云服务所属的地域、访问云服务时使用的私有网络实例(vpc)ID、路由条目的ID"
)
def describe_cen_service_route_entries(
        cen_id: Optional[str] = None,
        cen_route_entry_ids: Optional[list[str]] = None,
        destination_cidr_block: Optional[str] = None,
        service_region_id: Optional[str] = None,
        service_vpc_id: Optional[str] = None,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None) -> dict[str, Any]:
    """
    调用 DescribeCenServiceRouteEntries 接口，查询满足指定条件的云服务访问路由的详细信息。
    Args:
        cen_id (str): 云企业网实例的ID。
        cen_route_entry_ids (list[str]): 路由条目的ID。
        destination_cidr_block (str): 云服务的地址段，必须属于100.64.0.0/10或fd00:64::/32网段。
        service_region_id (str): 云服务所属的地域。
        service_vpc_id (str): 访问云服务时使用的私有网络实例(vpc)的ID。
        page_number Optional(int): 分页查询列表的页码。默认值为1。
        page_size Optional(int): 分页查询时每页的行数。取值范围为1～100，默认值为20。
    Returns:
        dict[str, Any]: 服务路由条目的详细信息。
    """
    req = {
        "cen_id": cen_id,
        "cen_route_entry_ids": cen_route_entry_ids,
        "destination_cidr_block": destination_cidr_block,
        "service_region_id": service_region_id,
        "service_vpc_id": service_vpc_id,
        "page_number": page_number,
        "page_size": page_size
    }

    resp = cen_resource.describe_cen_service_route_entries(req)
    return resp.to_dict()


@mcp.tool(
    name="describe_cen_route_entries",
    description="查询指定云企业网实例的路由条目,支持根据CEN实例ID、路由条目的目标CIDR块、路由条目的实例ID、路由条目的实例区域ID、路由条目的实例类型查询"
)
def describe_cen_route_entries(
        cen_id: Optional[str] = None,
        destination_cidr_block: Optional[str] = None,
        instance_id: Optional[str] = None,
        instance_region_id: Optional[str] = None,
        instance_type: Optional[str] = None,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None) -> dict[str, Any]:
    """
    调用 DescribeCenRouteEntries 接口，查询指定云企业网实例的路由条目。
    Args:
        cen_id (str): 云企业网实例的ID。
        destination_cidr_block (str): 路由条目的目标CIDR块。
        instance_id (str): 路由条目的实例ID。
        instance_region_id (str): 路由条目的实例区域ID。
        instance_type (str): 路由条目的实例类型。
        page_number Optional(int): 分页查询列表的页码。默认值为1。
        page_size Optional(int): 分页查询时每页的行数。取值范围为1～100，默认值为20。
    Returns:
        dict[str, Any]: 路由条目的详细信息。
    """
    req = {
        "cen_id": cen_id,
        "destination_cidr_block": destination_cidr_block,
        "instance_id": instance_id,
        "instance_region_id": instance_region_id,
        "instance_type": instance_type,
        "page_number": page_number,
        "page_size": page_size
    }

    resp = cen_resource.describe_cen_route_entries(req)
    return resp.to_dict()


@mcp.tool(
    name="describe_cen_summary_route_entries",
    description="查询满足指定条件的CEN汇总路由,支持根据CEN实例ID、路由条目的目标CIDR块查询"
)
def describe_cen_summary_route_entries(
        cen_id: str = None,
        destination_cidr_block: Optional[str] = None,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None) -> dict[str, Any]:
    """
    调用 DescribeCenSummaryRouteEntries 接口，查询满足指定条件的CEN汇总路由。
    Args:
        cen_id (str): 云企业网实例的ID。
        destination_cidr_block (str): 路由条目的目标CIDR块。
        page_number Optional(int): 分页查询列表的页码。默认值为1。
        page_size Optional(int): 分页查询时每页的行数。取值范围为1～100，默认值为20。
    Returns:
        dict[str, Any]: 路由条目的摘要信息。
    """
    req = {
        "cen_id": cen_id,
        "destination_cidr_block": destination_cidr_block,
        "page_number": page_number,
        "page_size": page_size
    }

    resp = cen_resource.describe_cen_summary_route_entries(req)
    return resp.to_dict()
