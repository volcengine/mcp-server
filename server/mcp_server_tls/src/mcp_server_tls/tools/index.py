import logging
from typing import Optional, List

from mcp_server_tls.config import TLS_CONFIG
from mcp_server_tls.resources.index import create_index_resource, delete_index_resource, describe_index_resource
from mcp_server_tls.utils import get_sdk_auth_info

logger = logging.getLogger(__name__)

async def create_index_tool(
        topic_id: Optional[str] = None,
        full_text: Optional[dict] = None,
        key_value: Optional[List[dict]] = None,
        user_inner_key_value: Optional[List[dict]] = None,
) -> dict:
    """Create index configuration for a VolcEngine TLS topic.

    This tool allows you to create index configuration for a log topic to enable efficient log searching.
    You can configure full-text search, key-value indexing, and user inner key-value indexing.

    Args:
        topic_id: ID of the log topic to create index for (optional)
        full_text: Full-text search configuration (optional)
            - delimiter: Word delimiter for tokenization
            - case_sensitive: Whether search is case sensitive (default: False)
            - include_chinese: Whether to support Chinese character indexing (default: False)
        key_value: Key-value index configuration list (optional)
            - key: Field name to index
            - value_type: Data type (text/long/double, default: text)
            - delimiter: Word delimiter for tokenization
            - case_sensitive: Whether search is case sensitive (default: False)
            - include_chinese: Whether to support Chinese indexing (default: False)
            - sql_flag: Whether to enable SQL query support (default: False)
            - index_all: Whether to index all values (default: False)
        user_inner_key_value: User inner key-value index configuration list (optional)
            Same format as key_value

    Returns:
        Dictionary containing the request ID for tracking the index creation operation.

    Examples:
        # Create full-text index only
        create_index_tool("topic-123", full_text={"delimiter": " ", "case_sensitive": false})

        # Create key-value index for specific fields
        create_index_tool("topic-123", key_value=[{"key": "status", "value_type": "text"}])

        # Create combined index configuration
        create_index_tool("topic-123", 
                         full_text={"include_chinese": true},
                         key_value=[{"key": "user_id", "value_type": "long", "sql_flag": true}])
    """
    try:

        from mcp_server_tls.server import mcp
        topic_id = topic_id or TLS_CONFIG.topic_id
        if not topic_id or not topic_id.strip():
            raise ValueError("topic_id is required")

        auth_info = get_sdk_auth_info(mcp.get_context())

        return await create_index_resource(
            auth_info=auth_info,
            topic_id=topic_id,
            full_text=full_text,
            key_value=key_value,
            user_inner_key_value=user_inner_key_value,
        )

    except Exception as e:
        logger.error("call tool error: create_index_tool, err is {}".format(str(e)))
        return {"error": str(e)}

async def delete_index_tool(
        topic_id: str,
) -> dict:
    """Delete index configuration for a VolcEngine TLS topic.

    This tool allows you to delete the index configuration of a log topic.
    After deletion, the topic will no longer support indexed searches.

    Args:
        topic_id: ID of the log topic to delete index for (required)

    Returns:
        Dictionary containing the request ID for tracking the index deletion operation.

    Examples:
        # Delete index for specific topic
        delete_index_tool("topic-123")
    """
    try:

        from mcp_server_tls.server import mcp

        auth_info = get_sdk_auth_info(mcp.get_context())

        return await delete_index_resource(
            auth_info=auth_info,
            topic_id=topic_id,
        )

    except Exception as e:
        logger.error("call tool error: delete_index_tool, err is {}".format(str(e)))
        return {"error": str(e)}

async def describe_index_tool(
        topic_id: Optional[str] = None,
) -> dict:
    """Describe index configuration for a VolcEngine TLS topic.

    This tool allows you to query the index configuration of a log topic,
    including full-text search settings and key-value index configurations.

    Args:
        topic_id: ID of the log topic to query index for (optional, defaults to environment variable)

    Returns:
        Dictionary containing the index configuration details including
        topic_id, full_text config, key_value configs, and timestamps.

    Examples:
        # Query index configuration for specific topic
        describe_index_tool("topic-123")
        
        # Query index configuration for default topic
        describe_index_tool()
    """
    try:

        from mcp_server_tls.server import mcp

        auth_info = get_sdk_auth_info(mcp.get_context())

        topic_id = topic_id or TLS_CONFIG.topic_id
        if not topic_id:
            raise ValueError("topic id is required")

        return await describe_index_resource(
            auth_info=auth_info,
            topic_id=topic_id,
        )

    except Exception as e:
        logger.error("call tool error: describe_index_tool, err is {}".format(str(e)))
        return {"error": str(e)}