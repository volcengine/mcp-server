import logging
from typing import Optional, Dict, Any

from mcp_server_tls.config import TLS_CONFIG
from mcp_server_tls.resources.download import describe_download_tasks_resource, describe_download_url_resource, \
    create_download_task_resource
from mcp_server_tls.utils import get_sdk_auth_info

logger = logging.getLogger(__name__)


async def create_download_task_tool(
    query: str,
    task_name: str,
    start_time: int,
    end_time: int,
    format_type: str,
    sort: str,
    limit: int,
    topic_id: Optional[str] = None,
    compression: Optional[str] = None,
) -> dict:
    """Create a download task for exporting log data.

    This tool creates a download task that exports log data based on specified
    query conditions and time range. The exported data can be downloaded once
    the task is completed.

    Args:
        query: Log query statement for filtering logs (required)
        task_name: Name of the download task (required)
        start_time: Query start time, Unix timestamp (seconds/milliseconds) (required)
        end_time: Query end time, Unix timestamp (seconds/milliseconds) (required)
        format_type: Export format type (csv, json) (required)
        sort: Sort order for the exported data (required)
        limit: Maximum number of logs to export (required)
        topic_id: Log topic ID (optional, defaults to configured topic_id)
        compression: Compression format for the download file (optional, defaults to gzip)

    Returns:
        Dictionary containing task_id, task_name

    Examples:
        # Create a download task with all required parameters (using default topic_id)
        create_download_task_tool(
            query="__content__: error",
            task_name="error_logs_export",
            start_time=1700000000,
            end_time=1700086400,
            format_type="csv",
            sort="desc",
            limit=10000
        )

        # Create a download task with specific topic_id and compression
        create_download_task_tool(
            query="status: 500",
            task_name="server_errors_export",
            start_time=1700000000,
            end_time=1700086400,
            format_type="json",
            sort="desc",
            limit=5000,
            topic_id="topic-123456",
            compression="gzip"
        )
    """
    try:

        from mcp_server_tls.server import mcp

        auth_info = get_sdk_auth_info(mcp.get_context())

        # Use configured topic_id if not provided
        topic_id = topic_id or TLS_CONFIG.topic_id
        if not topic_id or not topic_id.strip():
            raise ValueError("topic_id is required")

        return await create_download_task_resource(
            auth_info=auth_info,
            query=query,
            task_name=task_name,
            start_time=start_time,
            end_time=end_time,
            topic_id=topic_id,
            compression=compression,
            format_type=format_type,
            sort=sort,
            limit=limit,
        )

    except Exception as e:
        logger.error("call tool error: create_download_task_tool, err is {}".format(str(e)))
        return {"error": str(e)}

async def describe_download_tasks_tool(
    topic_id: Optional[str] = None,
    page_number: Optional[int] = 1,
    page_size: Optional[int] = 20,
    task_name: Optional[str] = None,
) -> dict:
    """Query download task list.

    This tool queries the list of download tasks for a specified log topic,
    supporting pagination and task name filtering.

    Args:
        topic_id: Log topic ID (optional, defaults to configured topic_id)
        page_number: Page number for pagination (optional, defaults to 1)
        page_size: Page size for pagination (optional, defaults to 20, max 100)
        task_name: Task name for filtering, supports fuzzy search (optional)

    Returns:
        Dictionary containing total count and task list information

    Examples:
        # Query all download tasks for default topic
        describe_download_tasks_tool()

        # Query tasks for specific topic with pagination
        describe_download_tasks_tool(
            topic_id="topic-123456",
            page_number=1,
            page_size=10
        )

        # Query tasks by name filter
        describe_download_tasks_tool(
            topic_id="topic-123456",
            task_name="error_export"
        )
    """
    try:

        from mcp_server_tls.server import mcp

        auth_info = get_sdk_auth_info(mcp.get_context())

        # Use configured topic_id if not provided
        topic_id = topic_id or TLS_CONFIG.topic_id
        if not topic_id or not topic_id.strip():
            raise ValueError("topic_id is required")

        return await describe_download_tasks_resource(
            auth_info=auth_info,
            topic_id=topic_id,
            page_number=page_number,
            page_size=page_size,
            task_name=task_name,
        )

    except Exception as e:
        logger.error("call tool error: describe_download_tasks_tool, err is {}".format(str(e)))
        return {"error": str(e)}


async def describe_download_url_tool(
    task_id: str,
) -> dict:
    """Get download URL for a task.

    This tool gets the download URL for a specified download task.
    The URL is typically valid for a limited time period.

    Args:
        task_id: Download task ID (required)

    Returns:
        Dictionary containing download URL information

    Examples:
        # Get download URL for a task
        describe_download_url_tool("task-123456789")
    """
    try:

        from mcp_server_tls.server import mcp

        auth_info = get_sdk_auth_info(mcp.get_context())

        if not task_id or not task_id.strip():
            raise ValueError("task_id is required")

        return await describe_download_url_resource(
            auth_info=auth_info,
            task_id=task_id,
        )

    except Exception as e:
        logger.error("call tool error: describe_download_url_tool, err is {}".format(str(e)))
        return {"error": str(e)}