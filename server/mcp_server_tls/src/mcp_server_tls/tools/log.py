import time
import logging

from typing import Optional
from mcp_server_tls.config import TLS_CONFIG
from mcp_server_tls.resources.log import search_logs_v2_resource, put_logs_v2_resource, consume_logs_resource, describe_cursor_resource, describe_log_context_resource
from mcp_server_tls.utils import get_sdk_auth_info

logger = logging.getLogger(__name__)

async def search_logs_v2_tool(
        query: str,
        topic_id: Optional[str] = None,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        limit: Optional[int] = 10
) -> dict:
    """Search logs using the provided query from the TLS service.

    This tool allows you to search logs using various query types including full text search,
    key-value search, and SQL analysis. It provides flexible time range filtering and
    limit options to customize your search results.

    Args:
        query: Search query string. Supports three formats:
            - Full text search: e.g., "error"
            - Key-value search: e.g., "key1:error"
            - SQL analysis: e.g., "* | select count(*) as count"
        topic_id: Optional topic ID to search logs from. If not provided, uses the globally configured topic.
        limit: Maximum number of logs to return (default: 100)
        start_time: Start time in milliseconds since epoch (default: 15 minutes ago)
        end_time: End time in milliseconds since epoch (default: current time)

    Returns:
        List of log entries matching the search criteria. Each log entry is a dictionary
        containing the log data, timestamp, and other metadata.

    Examples:
        # Search for error logs
        search_logs("error")

        # Search for logs with a specific key-value
        search_logs("status_code:500")

        # Perform SQL analysis
        search_logs("* | select count(*) as count group by status_code")
    """
    try:

        from mcp_server_tls.server import mcp

        auth_info = get_sdk_auth_info(mcp.get_context())

        if not query:
            raise ValueError("query is required")

        if end_time is None:
            end_time = int(time.time() * 1000)

        if start_time is None:
            start_time = end_time - ( 15 * 60 * 1000 )

        topic_id = topic_id or TLS_CONFIG.topic_id
        if not topic_id:
            raise ValueError("topic id is required")

        return await search_logs_v2_resource(
            auth_info=auth_info,
            topic_id=topic_id,
            query=query,
            start_time=start_time,
            end_time=end_time,
            limit=limit,
        )

    except Exception as e:
        logger.error("call tool error: search_logs_v2_tool, err is {}".format(str(e)))
        return {"error": str(e)}


async def put_logs_v2_tool(
        logs: list[dict],
        log_time: int = 0,
        topic_id: Optional[str] = None,
        source: Optional[str] = None,
        filename: Optional[str] = None,
        hash_key: Optional[str] = None,
        compression: str = "lz4",
) -> dict:
    """Put logs tool to upload logs to the specified log topic of tls.

    Currently, it only supports writing logs in key-value format, and then the tool converts them
    to PB format (Protocol Buffer) log data and sends them to the tls server.

    refer to Data Encoding Method. When uploading logs, it supports writing in load balanced mode
    and HashKey routing shard mode.

    1. HashKey Routing Shard Mode:
        When writing logs, the data is written to the specified shard in an orderly manner.
        It is suitable for scenarios where data writing and consumption require high order.
        For example, a producer can be fixed to the Shard according to the name Hash,
        so that the data written and consumed on the Shard is strictly ordered,
        and in the process of merging and splitting, it can be strictly guaranteed that
        the Key will only appear on a Shard at a point in time. At this time, you need to
        set the HashKey, the logging service will write the data to the Shard that contains the value of the Key.
    2. Load Balancing Mode:
        Automatically writes packets to any of the currently available Shards according to the load balancing principle.
        This mode is suitable for scenarios where the write and consumption behavior is independent of the Shard, such as out-of-order.
        The interfaces related to log uploads (PutLogs, WebTracks) share a common invocation frequency and traffic limit quota, which is limited as follows:

    The total request frequency of the interface is limited to 500 requests/Shard/sec,
    xceeding the request frequency limit will report an error ExceedQPSLimit.

    The total traffic limit of the interface is 5MiB/Shard/s, and the traffic limit of each Shard after log decompression is 30MiB/s.
    Exceeding the traffic limit will report ExceedRateLimit.
    It is recommended to turn on Shard auto-splitting in case of heavy traffic so as not to affect the data writing efficiency.

    Args:
        logs: A list of logs consisting of key-value pairs in key-value format.
        log_time: Optional log time of these logs, default is 0, it will be converted to the current time, Supports seconds or milliseconds timestamps
        topic_id: Optional topic ID for searching logs. by default, the globally configured topic is used, but if it is not configured, this topic parameter is required.
        source: Optional source of the log, usually identified by the machine IP.
        filename: Optional filename of log file name.
        hash_key: Optional hash_key of the log group that specifies the partition (Shard) to which the current log group is to be written.
        compression: Optional The compression format of the request body. Default compression format is lz4. supports setting to lz4, zlib

    Returns:
        reqeust_id: Unique identifier for each API request

    Examples:
        # write logs with default setting
        logs: [
            {"key1": "value1", "key2": value2},
        ]
        put_logs_v2_tool(logs)

        # write logs with log_time
        put_logs_v2_tool(logs, 1747713515000)

    """
    try:

        from mcp_server_tls.server import mcp

        auth_info = get_sdk_auth_info(mcp.get_context())

        topic_id = topic_id or TLS_CONFIG.topic_id
        if not topic_id:
            raise ValueError("topic id is required")

        return await put_logs_v2_resource(
            auth_info=auth_info,
            topic_id=topic_id,
            logs=logs,
            log_time=log_time,
            source=source,
            filename=filename,
            hash_key=hash_key,
            compression=compression,
        )

    except Exception as e:
        logger.error("call tool error: put_logs_v2_tool, err is {}".format(str(e)))
        return {"error": str(e)}

async def consume_logs_tool(
        shard_id: int,
        cursor: str,
        topic_id: Optional[str] = None,
        end_cursor: Optional[str] = None,
        log_group_count: Optional[int] = None,
        compression: Optional[str] = None,
        consumer_group_name: Optional[str] = None,
        consumer_name: Optional[str] = None,
) -> dict:
    """Consume logs from a specific shard in a VolcEngine TLS topic.

    This tool allows you to consume logs from a specific shard using a cursor.
    You can specify the start cursor and optionally an end cursor to limit the consumption range.

    Args:
        shard_id: ID of the shard to consume from (required)
        cursor: Starting cursor position for consumption (required)
        topic_id: ID of the log topic to consume from (optional, defaults to environment variable)
        end_cursor: Ending cursor position to limit consumption range (optional)
        log_group_count: Maximum number of log groups to return (optional)
        compression: Compression format for returned data, supports lz4/zlib (optional)
        consumer_group_name: Consumer group name for coordinated consumption (optional)
        consumer_name: Consumer name within the group (optional)

    Returns:
        Dictionary containing consumed log groups, count, and cursor information.

    Examples:
        # Basic consumption from cursor
        consume_logs_tool(0, "ACEleZiZAQAAmZpvqAEAAAAxNzU5MTU2Mjc5OTA5X3Yy")

        # Consume with limit and compression
        consume_logs_tool(0, "ACEleZiZAQAAmZpvqAEAAAAxNzU5MTU2Mjc5OTA5X3Yy", topic_id="topic-123", end_cursor="cACEleZiZAQAAmZpvqAEAAAAxNzU5MTU2Mjc5OTA5X3fd",
                         log_group_count=100, compression="lz4")

        # Consume with consumer group
        consume_logs_tool(0, "ACEleZiZAQAAmZpvqAEAAAAxNzU5MTU2Mjc5OTA5X3Yy", topic_id="topic-123",
                         consumer_group_name="my-group", consumer_name="consumer-1")
    """
    try:

        from mcp_server_tls.server import mcp

        auth_info = get_sdk_auth_info(mcp.get_context())

        topic_id = topic_id or TLS_CONFIG.topic_id
        if not topic_id:
            raise ValueError("topic id is required")

        return await consume_logs_resource(
            auth_info=auth_info,
            topic_id=topic_id,
            shard_id=shard_id,
            cursor=cursor,
            end_cursor=end_cursor,
            log_group_count=log_group_count,
            compression=compression,
            consumer_group_name=consumer_group_name,
            consumer_name=consumer_name,
        )

    except Exception as e:
        logger.error("call tool error: consume_logs_tool, err is {}".format(str(e)))
        return {"error": str(e)}

async def describe_cursor_tool(
        shard_id: int,
        from_time: str,
        topic_id: Optional[str] = None,
) -> dict:
    """Get cursor position for a specific time point in a VolcEngine TLS shard.

    This tool allows you to get the cursor position corresponding to a specific time point.
    You can use Unix timestamp (seconds) or special values "begin"/"end".

    Args:
        shard_id: ID of the shard to query (required)
        from_time: Time point to get cursor for, can be Unix timestamp (seconds) or "begin"/"end" (required)
        topic_id: ID of the log topic (optional, defaults to environment variable)

    Returns:
        Dictionary containing the cursor position and log count information.

    Examples:
        # Get cursor for beginning of shard
        describe_cursor_tool(0, "begin")

        # Get cursor for specific timestamp
        describe_cursor_tool(0, "1640995200", topic_id="topic-123")

        # Get cursor for end of shard
        describe_cursor_tool(0, "end", topic_id="topic-123")
    """
    try:

        from mcp_server_tls.server import mcp

        auth_info = get_sdk_auth_info(mcp.get_context())

        topic_id = topic_id or TLS_CONFIG.topic_id
        if not topic_id:
            raise ValueError("topic id is required")

        return await describe_cursor_resource(
            auth_info=auth_info,
            topic_id=topic_id,
            shard_id=shard_id,
            from_time=from_time,
        )

    except Exception as e:
        logger.error("call tool error: describe_cursor_tool, err is {}".format(str(e)))
        return {"error": str(e)}

async def describe_log_context_tool(
        context_flow: str,
        package_offset: int,
        source: str,
        topic_id: Optional[str] = None,
        prev_logs: int = 10,
        next_logs: int = 10,
) -> dict:
    """Get log context (surrounding logs) for a specific log entry in VolcEngine TLS.

    This tool allows you to get the context around a specific log entry,
    including previous and next logs from the same log group.

    Args:
        context_flow: ID of the LogGroup containing the target log (required)
        package_offset: Sequence number of the target log within the LogGroup (required)
        source: Source host IP address of the log (required)
        topic_id: ID of the log topic (optional, defaults to environment variable)
        prev_logs: Number of previous logs to include in context (default: 10)
        next_logs: Number of next logs to include in context (default: 10)

    Returns:
        Dictionary containing previous logs, next logs, and context flow information.

    Examples:
        # Get basic log context
        describe_log_context_tool("flow-123", 5, "192.168.1.1")

        # Get extended context
        describe_log_context_tool("flow-123", 5, "192.168.1.1", topic_id="topic-123",
                               prev_logs=20, next_logs=20)
    """
    try:

        from mcp_server_tls.server import mcp

        auth_info = get_sdk_auth_info(mcp.get_context())

        topic_id = topic_id or TLS_CONFIG.topic_id
        if not topic_id:
            raise ValueError("topic id is required")

        return await describe_log_context_resource(
            auth_info=auth_info,
            topic_id=topic_id,
            context_flow=context_flow,
            package_offset=package_offset,
            source=source,
            prev_logs=prev_logs,
            next_logs=next_logs,
        )

    except Exception as e:
        logger.error("call tool error: describe_log_context_tool, err is {}".format(str(e)))
        return {"error": str(e)}
