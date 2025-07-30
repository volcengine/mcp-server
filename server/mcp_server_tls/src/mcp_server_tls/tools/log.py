import time
import logging

from typing import Optional
from mcp_server_tls.config import TLS_CONFIG
from mcp_server_tls.resources.log import search_logs_v2_resource, put_logs_v2_resource
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

        topic_id = TLS_CONFIG.topic_id or topic_id
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

        topic_id = TLS_CONFIG.topic_id or topic_id
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
