import logging
from typing import Optional, List

from mcp_server_tls.config import TLS_CONFIG
from mcp_server_tls.resources.project import describe_project_resource, describe_projects_resource, create_project_resource, delete_project_resource
from mcp_server_tls.utils import get_sdk_auth_info

logger = logging.getLogger(__name__)

async def describe_project_tool(
        project_id: Optional[str] = None
) -> dict:
    """Retrieve VolcEngine TLS project information using a project ID.
    """
    try:

        from mcp_server_tls.server import mcp

        auth_info = get_sdk_auth_info(mcp.get_context())

        project_id = project_id or TLS_CONFIG.project_id
        if not project_id:
            raise ValueError("project id is required")

        return await describe_project_resource(
            auth_info=auth_info,
            project_id=project_id,
        )

    except Exception as e:
        logger.error("call tool error: describe_project_tool, err is {}".format(str(e)))
        return {"error": str(e)}

async def describe_projects_tool(
        page_number: Optional[int] = 1,
        page_size: Optional[int] = 10,
        project_id: Optional[str] = None,
        project_name: Optional[str] = None,
        is_full_name: Optional[bool] = False,
        iam_project_name: Optional[str] = None,
) -> dict:
    """Retrieve VolcEngine TLS project information using a project ID or other parameters.
       By default, each query returns up to 10 results.
    """
    try:

        from mcp_server_tls.server import mcp

        auth_info = get_sdk_auth_info(mcp.get_context())

        return await describe_projects_resource(
            auth_info=auth_info,
            page_number=page_number,
            page_size=page_size,
            project_id=project_id,
            project_name=project_name,
            is_full_name=is_full_name,
            iam_project_name=iam_project_name,
        )

    except Exception as e:
        logger.error("call tool error: describe_projects_tool, err is {}".format(str(e)))
        return {"error": str(e)}

async def create_project_tool(
        project_name: str,
        region: Optional[str] = None,
        description: Optional[str] = None,
        iam_project_name: Optional[str] = None,
        tags: Optional[List] = None,
) -> dict:
    """Create a new VolcEngine TLS project.

    This tool allows you to create a new TLS project with specified configuration parameters.
    A project is the top-level container for organizing log topics and resources in TLS service.

    Args:
        project_name: Name of the log project (required)
        region: Region information, if not provided uses the globally configured region (optional)
        description: Log project description information (optional)
        iam_project_name: IAM project name that the log project belongs to, defaults to "default" if not specified (optional)
        tags: Log project tag information, List[TagInfo] format where TagInfo contains key and value fields (optional)

    Returns:
        Dictionary containing the created project information including project_id, project_name,
        region, and other configuration details.

    Examples:
        # Create basic project
        create_project_tool("my-log-project")

        # Create project with description
        create_project_tool("production-logs", description="Production environment log project")

        # Create project in specific region
        create_project_tool("beijing-logs", region="cn-beijing")

        # Create project with tags
        create_project_tool("test-project", tags=[{"key": "env", "value": "test"}, {"key": "team", "value": "dev"}])
    """
    try:

        from mcp_server_tls.server import mcp

        auth_info = get_sdk_auth_info(mcp.get_context())

        region = region or TLS_CONFIG.region
        if not region:
            raise ValueError("region is required")

        return await create_project_resource(
            auth_info=auth_info,
            project_name=project_name,
            region=region,
            description=description,
            iam_project_name=iam_project_name,
            tags=tags,
        )

    except Exception as e:
        logger.error("call tool error: create_project_tool, err is {}".format(str(e)))
        return {"error": str(e)}

async def delete_project_tool(
        project_id: str
) -> dict:
    """Delete a VolcEngine TLS project.

    This tool allows you to delete a TLS project by specifying the project ID.
    Note that you can only delete projects that do not contain any log topics.

    Args:
        project_id: ID of the project to delete (required).

    Returns:
        Dictionary containing the request ID for tracking the deletion operation.

    Examples:
        # Delete specific project
        delete_project_tool("project-123456")
    """
    try:

        from mcp_server_tls.server import mcp

        auth_info = get_sdk_auth_info(mcp.get_context())

        if not project_id:
            raise ValueError("project id is required")

        return await delete_project_resource(
            auth_info=auth_info,
            project_id=project_id,
        )

    except Exception as e:
        logger.error("call tool error: delete_project_tool, err is {}".format(str(e)))
        return {"error": str(e)}
