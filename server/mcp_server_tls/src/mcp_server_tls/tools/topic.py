import logging
from typing import Optional

from mcp_server_tls.config import TLS_CONFIG
from mcp_server_tls.resources.topic import describe_topic_resource, describe_topics_resource
from mcp_server_tls.utils import get_sdk_auth_info

logger = logging.getLogger(__name__)

async def describe_topic_tool(
        topic_id: Optional[str] = None
) -> dict:
    """Retrieve VolcEngine TLS topic information using a topic ID.
    """
    try:

        from mcp_server_tls.server import mcp

        auth_info = get_sdk_auth_info(mcp.get_context())

        topic_id = topic_id or TLS_CONFIG.topic_id
        if not topic_id:
            raise ValueError("topic id is required")

        return await describe_topic_resource(
            auth_info=auth_info,
            topic_id=topic_id,
        )

    except Exception as e:
        logger.error("call tool error: describe_topic_tool, err is {}".format(str(e)))
        return {"error": str(e)}

async def describe_topics_tool(
        page_number: Optional[int] = 1,
        page_size: Optional[int] = 10,
        project_id: Optional[str] = None,
        project_name: Optional[str] = None,
        topic_id: Optional[str] = None,
        topic_name: Optional[str] = None,
) -> dict:
    """Retrieve VolcEngine TLS topic information using a project ID or other parameters.
       By default, each query returns up to 10 results.
    """
    try:

        from mcp_server_tls.server import mcp

        auth_info = get_sdk_auth_info(mcp.get_context())

        project_id = project_id or TLS_CONFIG.project_id
        if not project_id:
            raise ValueError("project id is required")

        return await describe_topics_resource(
            auth_info=auth_info,
            page_number=page_number,
            page_size=page_size,
            project_name=project_name,
            project_id=project_id,
            topic_name=topic_name,
            topic_id=topic_id,
        )

    except Exception as e:
        logger.error("call tool error: describe_topics_tool, err is {}".format(str(e)))
        return {"error": str(e)}
