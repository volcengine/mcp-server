import logging
import os

from typing import Any, List, Optional, Dict
from mcp.server.fastmcp import FastMCP
from mcp_server_cen.base.cen import CENSDK

logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("CEN MCP Server", port=int(os.getenv("PORT", "8008")))

cen_resource = CENSDK()


@mcp.tool(
    name="describe_cens",
    description="查询满足指定条件的CEN实例"
)
def describe_cens(
        cen_ids: Optional[List[str]] = None,
        cen_names: Optional[List[str]] = None
) -> dict[str, Any]:
    """
    调用 DescribeCens 接口，查询满足指定条件的CEN实例。
    Args:
        cen_ids Optional(List[str]): CEN实例的ID列表。
        cen_names Optional(List[str]): CEN实例的名称列表。
    Returns:
        dict[str, Any]: CEN实例的详细信息。
    """
    req = {
        "cen_ids": cen_ids,
        "cen_name": cen_names
    }

    resp = cen_resource.describe_cens(req)
    return resp.to_dict()


@mcp.tool(
    name="describe_cen_attributes",
    description="查询CEN实例的详细信息"
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
    description="查看满足指定条件的网络实例的跨账号授权信息"
)
def describe_instance_granted_rules(
        instance_id: str = None) -> dict[str, Any]:
    """
    调用 DescribeInstanceGrantedRules 接口，查看满足指定条件的网络实例的跨账号授权信息。
    Args:
        instance_id (str): 要查看的实例的ID。
    Returns:
        dict[str, Any]: 实例关联的CEN实例的详细信息。
    Raises:
        ValueError: 实例的ID不能为空。
    """
    req = {
        "instance_id": instance_id
    }

    resp = cen_resource.describe_instance_granted_rules(req)
    return resp.to_dict()


@mcp.tool(
    name="describe_grant_rules_to_cen",
    description="查询CEN实例关联的实例"
)
def describe_grant_rules_to_cen(
        cen_id: str = None) -> dict[str, Any]:
    """
    调用 DescribeGrantRulesToCen 接口，查询CEN实例关联的实例。
    Args:
        cen_id (str): 要查看的CEN实例的ID。
    Returns:
        dict[str, Any]: CEN实例关联的实例的详细信息。
    Raises:
        ValueError: CEN实例的ID不能为空。
    """
    req = {
        "cen_id": cen_id
    }

    resp = cen_resource.describe_grant_rules_to_cen(req)
    return resp.to_dict()