import os
import logging
import argparse
from termios import IXOFF
import base64
import json
import time
from typing import Dict, List, Optional, Any
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp_server_las.config import load_config, LASConfig, load_config_by_sts
from mcp_server_las.las_service import las_search_keyword_api,las_search_dataset_info_api,las_search_dataset_by_name

from mcp.server.session import ServerSession
from mcp.server.fastmcp import Context, FastMCP
from starlette.requests import Request

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create MCP server
mcp = FastMCP("LAS Dataset Search Server", port=int(os.getenv("PORT", "8888")),host=os.getenv("ENV_MCP_SERVER_HOST", "127.0.0.1"))

@mcp.tool()
def las_get_dataset_info(
    dataset_id: str,
) -> str:
    """Get dataset info from the LAS service.

    This tool allows you to get dataset base info using various dataset_id.

    Args:
        dataset_id: Dataset ID to get info from. If not provided, set to the default dataset_id.

    Returns:
        Dataset info as a string.

    Examples:
        # get dataset info by dataset_id
        las_get_dataset_info("dataset_id")

        # get dataset info  default
        las_get_dataset_info("")

    """
    logger.info(f"Received get_dataset_info request with dataset_id: {dataset_id}")

    try:
        
        # 刷新凭证  sse接口特有
        config, global_dataset_id = refreshCredentials()

        # Use current time if end_time is not provided
        if dataset_id is not None:
            dataset_id = dataset_id.strip('"').strip("'")
        if dataset_id is None or dataset_id == '' or dataset_id == 'default':
            if global_dataset_id is None:
                raise ValueError("Dataset ID is required")
            dataset_id = global_dataset_id
          
        logger.info(
            f"Getting dataset info with dataset_id: {dataset_id}"
        )

        data = {
            "DatasetId": dataset_id,
        }
        #判断config不为空
        if config is None:
            raise ValueError("config is None")
        response = las_search_dataset_info_api(config.access_key_id, config.access_key_secret, config.session_token, data)
        return str(response)
    except Exception as e:
        logger.error(f"Error in get_dataset_info: {str(e)}")
        return str(e)


@mcp.tool()
def las_search_dataset(
    query: str,
) -> List[str]:
    """Search dataset by name from the LAS service.

    This tool allows you to search dataset by name.Use keyword to search dataset list.

    Args:
        query: Dataset name to search. keyword is part of name.

    Returns:
        list of dataset info as a string.

    Examples:
        # search dataset by assc
        las_search_dataset("assc")

        # search dataset by image
        las_search_dataset("image")

    """
    logger.info(f"Received search_dataset request with query: {query}")

    try:
        # 刷新凭证  sse接口特有
        config, global_dataset_id = refreshCredentials()
        # Use current time if end_time is not provided
        if query is None or query == '' or query == 'default':
            query = ''
        logger.info(
            f"Getting dataset info with query: {query}"
        )

        data = {
            "Name": query,
            "Status":["AVAILABLE"],
            "NextToken":"0",
            "MaxResults":10
        }
        #判断config不为空
        if config is None:
            raise ValueError("config is None")
        response = las_search_dataset_by_name(config.access_key_id, config.access_key_secret, config.session_token, data)
        res = response['Result']['Items']
        #将每一条数据转成字符串用逗号隔开
        res = [str(item) for item in res]
        return res
    except Exception as e:
        logger.error(f"Error in get_dataset_info: {str(e)}")
        return [str(e)]



@mcp.tool()
def las_search_keyword(
    query: str,
    dataset_id: Optional[str] = None,
    limit: int = 100,
    start_time: Optional[int] = None,
    end_time: Optional[int] = None,
) -> List[str]:
    """Search by keyword using the provided query from the LAS service.

    This tool allows you to search keywords using various query types including full text search,
    key-value search, and SQL analysis. It provides flexible time range filtering and
    limit options to customize your search results.

    Args:
        query: Search query string. Supports three formats:
            - Full text search: e.g., "error"
            - Key-value search: e.g., "key1:error"
            - SQL analysis: e.g., "* | select count(*) as count"
        dataset_id: Optional dataset ID to search logs from. If not provided, uses the globally configured dataset.
        limit: Maximum number of logs to return (default: 100)

    Returns:
        List of log entries matching the search criteria. Each log entry is a dictionary
        containing the log data, timestamp, and other metadata.

    Examples:
        # Search for error logs
        las_search_keyword("error")

        # Search for logs with a specific key-value
        las_search_keyword("status_code:500")

        # Perform SQL analysis
        las_search_keyword("* | select count(*) as count group by status_code")
    """
    logger.info(f"Received las_search_keyword request with query: {query}")

    try:
        # 刷新凭证  sse接口特有
        config, global_dataset_id = refreshCredentials()
        # Use current time if end_time is not provided
        if end_time is None:
            end_time = int(time.time() * 1000)

        # Use 15 minutes ago if start_time is not provided
        if start_time is None:
            start_time = end_time - (15 * 60 * 1000)  # 15 minutes in milliseconds
        dataset_id = dataset_id or global_dataset_id
        if not dataset_id:
            raise ValueError("Dataset ID is required")
        logger.info(
            f"Searching with query: {query} for dataset: {dataset_id}, limit: {limit}, time range: {start_time} to {end_time}"
        )

        #构建搜索参数
        # TODO 优化参数
        data = {
            "DatasetId": dataset_id,
            "NextToken": "0",
            "MaxResults": "5",
            "keyword": query,
        }
        #判断config不为空
        if config is None:
            raise ValueError("config is None")
        response = las_search_keyword_api(config.access_key_id, config.access_key_secret, config.session_token, data)
        res = response['Result']['Items']
        #将每一条数据转成字符串用逗号隔开
        res = [str(item) for item in res]
        return res
    except Exception as e:
        logger.error(f"Error in las_search_keyword: {str(e)}")
        return [str(e)]

def refreshCredentials():
    # 从 context 中获取 header
    ctx: Context[ServerSession, object] = mcp.get_context()
    raw_request: Request | None = ctx.request_context.request

    auth = None
    if raw_request:
        # 从 header 的 authorization 字段读取 base64 编码后的 sts json
        auth = raw_request.headers.get("authorization", None)
    if auth is None:
        # 如果 header 中没有认证信息，可能是 stdio 模式，尝试从环境变量获取
        auth = os.getenv("authorization", None)
    if auth is None:
        # 获取认证信息失败
        raise ValueError("Missing authorization info.")

    if ' ' in auth:
        _, base64_data = auth.split(' ', 1)
    else:
        base64_data = auth

    try:
        # 解码 Base64
        decoded_str = base64.b64decode(base64_data).decode('utf-8')
        data = json.loads(decoded_str)
        # 获取字段
        current_time = data.get('CurrentTime')
        expired_time = data.get('ExpiredTime')
        ak = data.get('AccessKeyId')
        sk = data.get('SecretAccessKey')
        session_token = data.get('SessionToken')
        if not ak or not sk or not session_token:
            raise ValueError("Invalid credentials ak, sk, session_token is null")
        logger.info(f"Loaded credentials: {current_time}, {expired_time}")

        config = load_config_by_sts(ak, sk, session_token)
        global_dataset_id = config.dataset_id

        logger.info(f"Loaded configuration for dataset ID: {global_dataset_id}")
        return config, global_dataset_id
    except Exception as e:
        logger.error(f"Error refreshing credentials: {str(e)}")
        raise

def main():
    """Main entry point for the MCP server."""

    try:
        logger.info("Starting LAS MCP Server...")

        mcp.run(transport='sse')
    except Exception as e:
        logger.error(f"Error starting LAS MCP Server: {str(e)}")
        raise


if __name__ == "__main__":
    main()
