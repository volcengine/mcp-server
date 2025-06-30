import logging
import os

from typing import Any, List, Optional, Dict
from mcp.server.fastmcp import FastMCP
from mcp_server_eip.base.eip import EIPSDK

logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("EIP MCP Server", port=int(os.getenv("PORT", "8000")))

eip_resource = EIPSDK()


@mcp.tool(
    name="describe_eip_address_attributes",
    description="查看一个指定公网IP的详细信息"
)
def describe_eip_address_attributes(
        allocation_id: Optional[str] = None,
) -> dict[str, Any]:
    """
    调用 DescribeEipAddressAttributes 接口，查看一个指定公网IP的详细信息。
    Args:
        allocation_id (str): 公网IP的ID。
    Returns:
        dict[str, Any]: 公网IP的详细信息。
    Raises:
        ValueError: 公网IP的ID不能为空。
    """
    req = {"allocation_id": allocation_id}

    resp = eip_resource.describe_eip_address_attributes(req)
    return resp.to_dict()


@mcp.tool(
    name="describe_eip_addresses",
    description="查询满足指定条件的公网IP"
)
def describe_eip_addresses(
        allocation_ids: Optional[List[str]] = None,
        associated_instance_id: Optional[str] = None,
        associated_instance_type: Optional[str] = None,
        billing_type: Optional[int] = None,
        eip_addresses: Optional[List[str]] = None,
        isp: str = "BGP",
        ip_address_pool_id: Optional[str] = None,
        max_results: Optional[int] = None,
        name: Optional[str] = None,
        next_token: Optional[str] = None,
        page_number: int = 1,
        page_size: int = 20,
        project_name: Optional[str] = None,
        security_protection_enabled: Optional[bool] = None,
        status: Optional[str] = None,
        tag_filters: Optional[List[Dict[str, str]]] = None
) -> dict[str, Any]:
    """
    调用 DescribeEipAddresses 接口，查询满足指定条件的公网IP。
    调用说明:
    传入多个请求参数，按照传入的参数进行查询，返回符合所有条件的公网IP，若没有符合条件的公网IP，则返回空值。
    若请求参数非必选参数均未传入，则按照当前登录账号查询，返回当前账号下的所有公网IP。
    使用标签过滤公网IP实例时，最多可查询指定标签关联的1000个公网IP实例。如果指定标签关联的公网IP实例超过1000个，则请您使用
    ListTagsForResources接口查询。
    Args:
        allocation_ids (List[str], optional): 公网IP的ID列表。
        associated_instance_id (str, optional): 公网IP关联的实例ID。
        associated_instance_type (str, optional): 公网IP关联的实例类型。
        billing_type (int, optional): 公网IP的计费类型。
        eip_addresses (List[str], optional): 公网IP的地址列表。
        isp (str, optional): 公网IP的ISP。
        ip_address_pool_id (str, optional): 公网IP的地址池ID。
        max_results (int, optional): 最大返回结果数。
        name (str, optional): 公网IP的名称。
        next_token (str, optional): 分页标记。
        page_number (int, optional): 页码。
        page_size (int, optional): 每页大小。
        project_name (str, optional): 项目名称。
        security_protection_enabled (bool, optional): 是否启用安全防护。
        status (str, optional): 公网IP的状态。
        tag_filters (List[Dict[str, str]], optional): 标签过滤器。
    Returns:
        dict[str, Any]: 公网IP的信息。
    Raises:
        ValueError: 标签过滤器的格式不正确。

    """
    req = {
        "allocation_ids": allocation_ids,
        "associated_instance_id": associated_instance_id,
        "associated_instance_type": associated_instance_type,
        "billing_type": billing_type,
        "eip_addresses": eip_addresses,
        "isp": isp,
        "ip_address_pool_id": ip_address_pool_id,
        "max_results": max_results,
        "name": name,
        "next_token": next_token,
        "page_number": page_number,
        "page_size": page_size,
        "project_name": project_name,
        "security_protection_enabled": security_protection_enabled,
        "status": status,
        "tag_filters": tag_filters
    }

    req = {k: v for k, v in req.items() if v is not None}
    logger.info(req)

    if tag_filters is not None:
        for filter_item in tag_filters:
            if not isinstance(filter_item, dict) or 'Key' not in filter_item:
                raise ValueError("Each element in TagFilters must be a dictionary containing the Key field")

    resp = eip_resource.describe_eip_addresses(req)
    return resp.to_dict()


@mcp.tool(
    name="describe_bandwidth_packages",
    description="查询满足指定条件的共享带宽包"
)
def describe_bandwidth_packages(
        bandwidth_package_ids: Optional[List[str]] = None,
        bandwidth_package_name: Optional[str] = None,
        isp: str = "BGP",
        max_results: Optional[int] = 10,
        next_token: Optional[str] = None,
        page_number: int = 1,
        page_size: int = 20,
        project_name: Optional[str] = None,
        protocol: Optional[str] = None,
        security_protection_enabled: Optional[bool] = None,
        tag_filters: Optional[List[Dict[str, str]]] = None
) -> dict[str, Any]:
    """
    调用 DescribeBandwidthPackages 接口，查询满足指定条件的共享带宽包。
    调用说明:
    传入多个请求参数，按照传入的参数进行查询，返回符合所有条件的共享带宽包，若没有符合条件的共享带宽包，则返回空值。
    若请求参数非必选参数均未传入，则按照当前登录账号查询，返回当前账号下的所有共享带宽包。
    使用标签过滤共享带宽包实例时，最多可查询指定标签关联的1000个共享带宽包实例。如果指定标签关联的共享带宽包实例超过1000个，则请您使用
    ListTagsForResources接口查询。
    Args:
        bandwidth_package_ids (List[str], optional): 共享带宽包的ID列表。
        bandwidth_package_name (str, optional): 共享带宽包的名称。
        isp (str, optional): 共享带宽包的ISP。
        max_results (int, optional): 最大返回结果数。
        next_token (str, optional): 分页标记。
        page_number (int, optional): 页码。
        page_size (int, optional): 每页大小。
        project_name (str, optional): 项目名称。
        protocol (str, optional): 共享带宽包的协议。
        security_protection_enabled (bool, optional): 是否启用安全防护。
        tag_filters (List[Dict[str, str]], optional): 标签过滤器。
    Returns:
        dict[str, Any]: 共享带宽包的信息。
    Raises:
        ValueError: 标签过滤器的格式不正确。
    """
    req = {
        "bandwidth_package_ids": bandwidth_package_ids,
        "bandwidth_package_name": bandwidth_package_name,
        "isp": isp,
        "max_results": max_results,
        "next_token": next_token,
        "page_number": page_number,
        "page_size": page_size,
        "project_name": project_name,
        "protocol": protocol,
        "security_protection_enabled": security_protection_enabled,
        "tag_filters": tag_filters
    }

    req = {k: v for k, v in req.items() if v is not None}
    logger.info(req)

    if tag_filters is not None:
        for filter_item in tag_filters:
            if not isinstance(filter_item, dict) or 'Key' not in filter_item:
                raise ValueError("Each element in TagFilters must be a dictionary containing the Key field")

    resp = eip_resource.describe_bandwidth_packages(req)
    return resp.to_dict()
