import os
import logging
import argparse
from termios import IXOFF
import time
from typing import Dict, List, Optional, Any

from mcp.server.fastmcp import FastMCP
import mcp.types as types

from mcp_server_las.config import load_config, LASConfig
from mcp_server_las.las_service import las_search_keyword_api,las_search_dataset_info_api,las_search_dataset_by_name

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Global variables
config = None
global_dataset_id = None

# Create MCP server
mcp = FastMCP("LAS Dataset Search Server", port=int(os.getenv("PORT", "8000")))



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

    This tool allows you to search dataset by name.

    Args:
        This tool allows you to search dataset by name.Use keyword to search dataset list.

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

    This tool allows you to search keywords in dataset. You can use a simple str to search. Result with list items.

    Args:
        query: Search query string
        dataset_id: Optional dataset ID to search logs from. If not provided, uses the globally configured dataset.
        limit: Optional limit of logs to return (default: 10)

    Returns:
        List of log entries matching the search criteria. Each log entry is a dictionary
        containing the log data, timestamp, and other metadata.

    Examples:
        # Search for ray dataset items
        las_search_keyword("ray")
    """
    logger.info(f"Received las_search_keyword request with query: {query}")

    try:
        if end_time is None:
            end_time = int(time.time() * 1000)

        if start_time is None:
            start_time = end_time - (15 * 60 * 1000)  # 15 minutes in milliseconds
        dataset_id = dataset_id or global_dataset_id
        if not dataset_id:
            raise ValueError("Dataset ID is required")
        logger.info(
            f"Searching with query: {query} for dataset: {dataset_id}, limit: {limit}, time range: {start_time} to {end_time}"
        )

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


def main():
    """Main entry point for the MCP server."""
    parser = argparse.ArgumentParser(description="Run the LAS MCP Server")
    parser.add_argument(
        "--transport",
        "-t",
        choices=["sse", "stdio", "streamable-http"],
        default="stdio",
        help="Transport protocol to use (sse or stdio)",
    )

    args = parser.parse_args()

    try:
        # Load configuration from environment variables
        global config
        global las_service
        global global_dataset_id

        config = load_config()
        global_dataset_id = config.dataset_id
        logger.info(f"Loaded configuration for dataset ID: {global_dataset_id}")

        logger.info(f"Starting LAS MCP Server with {args.transport} transport")
        mcp.run(transport=args.transport)
    except Exception as e:
        logger.error(f"Error starting LAS MCP Server: {str(e)}")
        raise


if __name__ == "__main__":
    main()
