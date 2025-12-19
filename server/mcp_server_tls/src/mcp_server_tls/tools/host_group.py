import logging
from typing import Optional, Dict, Any, List

from mcp_server_tls.config import TLS_CONFIG
from mcp_server_tls.resources.host_group import (
    create_host_group_resource,
    delete_host_group_resource,
    describe_host_group_resource,
    describe_host_groups_resource,
    describe_hosts_resource,
    describe_host_group_rules_resource
)
from mcp_server_tls.utils import get_sdk_auth_info

logger = logging.getLogger(__name__)


async def create_host_group_tool(
    host_group_name: str,
    host_group_type: str,
    host_ip_list: Optional[List[str]] = None,
    host_identifier: Optional[str] = None,
    auto_update: Optional[bool] = False,
    update_start_time: Optional[str] = None,
    update_end_time: Optional[str] = None,
    service_logging: Optional[bool] = False,
    iam_project_name: Optional[str] = None,
) -> dict:
    """Create a host group.

    This tool creates a host group for log collection management.
    Host groups can be organized by IP addresses or host identifiers.

    Args:
        host_group_name: Name of the host group (required)
        host_group_type: Type of host group ('IP' or 'Label') (required)
        host_ip_list: List of host IP addresses (required when type is 'IP')
        host_identifier: Host identifier (required when type is 'Label')
        auto_update: Whether to enable automatic update (optional, defaults to False)
        update_start_time: Update start time in HH:MM format (optional)
        update_end_time: Update end time in HH:MM format (optional)
        service_logging: Whether to enable service logging (optional, defaults to False)
        iam_project_name: IAM project name (optional)

    Returns:
        Dictionary containing host_group_id and other information

    Examples:
        # Create IP-based host group
        create_host_group_tool(
            host_group_name="web-servers",
            host_group_type="IP",
            host_ip_list=["192.168.1.1", "192.168.1.2"],
            auto_update=True
        )

        # Create Label-based host group
        create_host_group_tool(
            host_group_name="app-servers",
            host_group_type="Label",
            host_identifier="app-server-*",
            auto_update=False
        )
    """
    try:

        from mcp_server_tls.server import mcp

        auth_info = get_sdk_auth_info(mcp.get_context())
        
        # Validate type-specific parameters
        if host_group_type == "IP" and not host_ip_list:
            raise ValueError("host_ip_list is required when host_group_type is 'IP'")
        if host_group_type == "Label" and not host_identifier:
            raise ValueError("host_identifier is required when host_group_type is 'Label'")

        return await create_host_group_resource(
            auth_info=auth_info,
            host_group_name=host_group_name,
            host_group_type=host_group_type,
            host_ip_list=host_ip_list,
            host_identifier=host_identifier,
            auto_update=auto_update,
            update_start_time=update_start_time,
            update_end_time=update_end_time,
            service_logging=service_logging,
            iam_project_name=iam_project_name,
        )

    except Exception as e:
        logger.error("call tool error: create_host_group_tool, err is {}".format(str(e)))
        return {"error": str(e)}


async def delete_host_group_tool(
    host_group_id: str,
) -> dict:
    """Delete a host group.

    This tool deletes a host group by its ID.

    Args:
        host_group_id: Host group ID (required)

    Returns:
        Dictionary containing operation result

    Examples:
        # Delete host group
        delete_host_group_tool("host-group-123456")
    """
    try:

        from mcp_server_tls.server import mcp

        auth_info = get_sdk_auth_info(mcp.get_context())

        if not host_group_id or not host_group_id.strip():
            raise ValueError("host_group_id is required")

        return await delete_host_group_resource(
            auth_info=auth_info,
            host_group_id=host_group_id,
        )

    except Exception as e:
        logger.error("call tool error: delete_host_group_tool, err is {}".format(str(e)))
        return {"error": str(e)}


async def describe_host_group_tool(
    host_group_id: str,
) -> dict:
    """Describe a host group.

    This tool gets detailed information about a specific host group.

    Args:
        host_group_id: Host group ID (required)

    Returns:
        Dictionary containing host group detailed information

    Examples:
        # Get host group details
        describe_host_group_tool("host-group-123456")
    """
    try:

        from mcp_server_tls.server import mcp

        auth_info = get_sdk_auth_info(mcp.get_context())

        if not host_group_id or not host_group_id.strip():
            raise ValueError("host_group_id is required")

        return await describe_host_group_resource(
            auth_info=auth_info,
            host_group_id=host_group_id,
        )

    except Exception as e:
        logger.error("call tool error: describe_host_group_tool, err is {}".format(str(e)))
        return {"error": str(e)}


async def describe_host_groups_tool(
    host_group_id: Optional[str] = None,
    host_group_name: Optional[str] = None,
    page_number: Optional[int] = 1,
    page_size: Optional[int] = 20,
    auto_update: Optional[bool] = None,
    host_identifier: Optional[str] = None,
    service_logging: Optional[bool] = None,
    iam_project_name: Optional[str] = None,
) -> dict:
    """Describe host groups with filtering.

    This tool queries host groups with various filtering options and pagination.

    Args:
        host_group_id: Host group ID for filtering (optional)
        host_group_name: Host group name for filtering (optional)
        page_number: Page number for pagination (optional, defaults to 1)
        page_size: Page size for pagination (optional, defaults to 20, max 100)
        auto_update: Filter by auto update status (optional)
        host_identifier: Filter by host identifier (optional)
        service_logging: Filter by service logging status (optional)
        iam_project_name: Filter by IAM project name (optional)

    Returns:
        Dictionary containing total count and host groups list

    Examples:
        # Query all host groups
        describe_host_groups_tool()

        # Query with pagination
        describe_host_groups_tool(
            page_number=1,
            page_size=10
        )

        # Query by name filter
        describe_host_groups_tool(
            host_group_name="web-servers"
        )
    """
    try:

        from mcp_server_tls.server import mcp

        auth_info = get_sdk_auth_info(mcp.get_context())

        return await describe_host_groups_resource(
            auth_info=auth_info,
            host_group_id=host_group_id,
            host_group_name=host_group_name,
            page_number=page_number,
            page_size=page_size,
            auto_update=auto_update,
            host_identifier=host_identifier,
            service_logging=service_logging,
            iam_project_name=iam_project_name,
        )

    except Exception as e:
        logger.error("call tool error: describe_host_groups_tool, err is {}".format(str(e)))
        return {"error": str(e)}


async def describe_hosts_tool(
    host_group_id: str,
    ip: Optional[str] = None,
    heartbeat_status: Optional[int] = None,
    page_number: Optional[int] = 1,
    page_size: Optional[int] = 20,
) -> dict:
    """Describe hosts in a host group.

    This tool queries hosts within a specified host group.

    Args:
        host_group_id: Host group ID (required)
        ip: Host IP for filtering (optional)
        heartbeat_status: Heartbeat status for filtering (optional)
        page_number: Page number for pagination (optional, defaults to 1)
        page_size: Page size for pagination (optional, defaults to 20, max 100)

    Returns:
        Dictionary containing total count and hosts list

    Examples:
        # Query all hosts in a host group
        describe_hosts_tool("host-group-123456")

        # Query hosts with IP filter
        describe_hosts_tool(
            host_group_id="host-group-123456",
            ip="192.168.1.1"
        )
    """
    try:

        from mcp_server_tls.server import mcp

        auth_info = get_sdk_auth_info(mcp.get_context())

        if not host_group_id or not host_group_id.strip():
            raise ValueError("host_group_id is required")

        return await describe_hosts_resource(
            auth_info=auth_info,
            host_group_id=host_group_id,
            ip=ip,
            heartbeat_status=heartbeat_status,
            page_number=page_number,
            page_size=page_size,
        )

    except Exception as e:
        logger.error("call tool error: describe_hosts_tool, err is {}".format(str(e)))
        return {"error": str(e)}


async def describe_host_group_rules_tool(
    host_group_id: str,
    page_number: Optional[int] = 1,
    page_size: Optional[int] = 20,
) -> dict:
    """Describe rules associated with a host group.

    This tool queries collection rules associated with a specified host group.

    Args:
        host_group_id: Host group ID (required)
        page_number: Page number for pagination (optional, defaults to 1)
        page_size: Page size for pagination (optional, defaults to 20, max 100)

    Returns:
        Dictionary containing total count and rule list

    Examples:
        # Query rules for a host group
        describe_host_group_rules_tool("host-group-123456")
    """
    try:

        from mcp_server_tls.server import mcp

        auth_info = get_sdk_auth_info(mcp.get_context())

        if not host_group_id or not host_group_id.strip():
            raise ValueError("host_group_id is required")

        return await describe_host_group_rules_resource(
            auth_info=auth_info,
            host_group_id=host_group_id,
            page_number=page_number,
            page_size=page_size,
        )

    except Exception as e:
        logger.error("call tool error: describe_host_group_rules_tool, err is {}".format(str(e)))
        return {"error": str(e)}