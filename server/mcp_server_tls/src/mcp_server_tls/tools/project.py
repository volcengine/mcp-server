import logging
from typing import Optional

from mcp_server_tls.config import TLS_CONFIG
from mcp_server_tls.resources.project import describe_project_resource, describe_projects_resource
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
