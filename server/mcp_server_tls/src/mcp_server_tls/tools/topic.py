import logging
from typing import Optional, List

from mcp_server_tls.config import TLS_CONFIG
from mcp_server_tls.resources.topic import describe_topic_resource, describe_topics_resource, create_topic_resource, delete_topic_resource
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

async def create_topic_tool(
        topic_name: str,
        project_id: Optional[str] = None,
        ttl: int = 30,
        shard_count: int = 2,
        description: Optional[str] = None,
        auto_split: bool = True,
        max_split_shard: int = 50,
        enable_tracking: bool = False,
        time_key: Optional[str] = None,
        time_format: Optional[str] = None,
        tags: Optional[List] = None,
        log_public_ip: bool = True,
        enable_hot_ttl: bool = False,
        hot_ttl: Optional[int] = None,
        cold_ttl: Optional[int] = None,
        archive_ttl: Optional[int] = None,
) -> dict:
    """Create a new VolcEngine TLS topic.

    This tool allows you to create a new log topic within a specified project.
    A topic is a logical partition for organizing and managing log data.

    Args:
        topic_name: Name of the log topic (required)
        project_id: ID of the project where the topic will be created. If not provided, uses the globally configured project ID (optional)
        ttl: Log retention time in days (default: 30 days)
        shard_count: Number of log partitions (default: 2, range: 1-10)
        description: Description of the log topic (optional)
        auto_split: Whether to enable automatic partition splitting (default: True)
        max_split_shard: Maximum number of partitions after splitting (default: 50)
        enable_tracking: Whether to enable WebTracking functionality (default: False)
        time_key: Field name for log time field (optional)
        time_format: Time field parsing format (optional)
        tags: Log topic tag information, List[TagInfo] format where TagInfo contains key and value fields (optional)
        log_public_ip: Whether to enable public IP recording (default: True)
        enable_hot_ttl: Whether to enable hot/cold archiving (default: False)
        hot_ttl: Hot data retention time (optional)
        cold_ttl: Cold data retention time (optional)
        archive_ttl: Archive data retention time (optional)

    Returns:
        Dictionary containing the created topic information including topic_id and other configuration details.

    Examples:
        # Create basic topic
        create_topic_tool("my-log-topic")

        # Create topic with custom TTL and shards
        create_topic_tool("production-logs", ttl=90, shard_count=3)

        # Create topic with description and tags
        create_topic_tool("api-logs", description="API gateway logs", tags=[{"key": "type", "value": "api"}])
    """
    try:

        from mcp_server_tls.server import mcp

        auth_info = get_sdk_auth_info(mcp.get_context())

        project_id = project_id or TLS_CONFIG.project_id
        if not project_id:
            raise ValueError("project id is required")

        return await create_topic_resource(
            auth_info=auth_info,
            topic_name=topic_name,
            project_id=project_id,
            ttl=ttl,
            shard_count=shard_count,
            description=description,
            auto_split=auto_split,
            max_split_shard=max_split_shard,
            enable_tracking=enable_tracking,
            time_key=time_key,
            time_format=time_format,
            tags=tags,
            log_public_ip=log_public_ip,
            enable_hot_ttl=enable_hot_ttl,
            hot_ttl=hot_ttl,
            cold_ttl=cold_ttl,
            archive_ttl=archive_ttl,
        )

    except Exception as e:
        logger.error("call tool error: create_topic_tool, err is {}".format(str(e)))
        return {"error": str(e)}

async def delete_topic_tool(
        topic_id: str
) -> dict:
    """Delete a VolcEngine TLS topic.

    This tool allows you to delete a log topic by specifying the topic ID.
    Note that deleting a topic will also delete all logs and configurations within it.

    Args:
        topic_id: ID of the topic to delete (required).

    Returns:
        Dictionary containing the request ID for tracking the deletion operation.

    Examples:
        # Delete specific topic
        delete_topic_tool("topic-123456")
    """
    try:

        from mcp_server_tls.server import mcp

        auth_info = get_sdk_auth_info(mcp.get_context())

        if not topic_id:
            raise ValueError("topic id is required")

        return await delete_topic_resource(
            auth_info=auth_info,
            topic_id=topic_id,
        )

    except Exception as e:
        logger.error("call tool error: delete_topic_tool, err is {}".format(str(e)))
        return {"error": str(e)}
