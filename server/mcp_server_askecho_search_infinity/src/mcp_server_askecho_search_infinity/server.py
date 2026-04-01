import logging
import argparse
from mcp.server import FastMCP
from typing import Dict, Any

from .model import *
from .config import *
from .api.api_key_auth import *
from .api.volcengine_auth import *

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

config = None
mcp = FastMCP("联网搜索API MCP Server")


@mcp.tool()
async def web_search(
    Query: str,
    Count: int = 10,
    SearchType: str = "web",
    TimeRange: str = "",
    AuthLevel: int = 0,
) -> Dict[str, Any]:
    """
    联网搜索 API 调用，支持网页和图片搜索
    Args:
        Query (str): 搜索 query，1~100 个字符
        Count (int): 返回条数，web 最多 50 条，image 最多 5 条
        SearchType (str): 搜索类型，仅支持 web 或 image
        TimeRange (str): web 搜索时间范围，可选 OneDay/OneWeek/OneMonth/OneYear 或日期区间
        AuthLevel (int): 权威等级过滤，0 为默认，1 为非常权威
    Returns:
        联网搜索结果返回结构
    """
    logger.info(f"Received web_search tool request")

    try:
        if config is None:
            raise ValueError("config not loaded")

        req = build_web_search_request(
            query=Query,
            count=Count,
            search_type=SearchType,
            time_range=TimeRange or None,
            auth_level=AuthLevel,
        )

        if config.api_key is not None and len(config.api_key) > 0:
            return await web_search_api_key_auth(config.api_key, req, "web_search")
        else:
            return await web_search_volcengine_auth(config.volcengine_ak, config.volcengine_sk, req, "web_search")
    except Exception as e:
        logger.error(f"Error in web_search tool: {e}")
        resp_error = ResponseError(
            error=Error(
                message=str(e),
                type="mcp_server_ask_echo_search_infinity_error",
                code="mcp_server_ask_echo_search_infinity_error",
            )
        )
        return resp_error.to_dict()


def main():
    """Main entry point for the MCP server."""
    parser = argparse.ArgumentParser(description="Run the Web Search API MCP Server")
    parser.add_argument(
        "--transport",
        "-t",
        choices=["sse", "stdio", "streamable-http"],
        default="stdio",
        help="Transport protocol to use (sse, stdio or streamable-http)",
    )

    args = parser.parse_args()

    try:
        # Load configuration from environment variables
        global config
        config = load_config()
        # Run the MCP server
        logger.info(f"Starting Web Search API MCP Server with {args.transport} transport")
        mcp.run(transport=args.transport)
    except Exception as e:
        logger.error(f"Error starting Web Search API MCP Server: {str(e)}")
        raise


if __name__ == "__main__":
    main()
