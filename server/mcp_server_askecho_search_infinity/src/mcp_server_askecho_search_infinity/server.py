import logging
import argparse
import dataclasses
from mcp.server import FastMCP
from mcp.server.fastmcp import Context
from mcp import types
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
mcp = FastMCP("AskEcho Search Infinity MCP Server")


@mcp.tool()
def web_search(
    Query: str,
    Count: int = 10
) -> Dict[str, Any]:
    """
    联网搜索能力调用，基于用户query搜索网络结果
    Args:
        Query (str): 用户搜索 query，1~100 个字符 (过长会截断)，不支持多词搜索
        Count (int): 返回条数，最多50条，不传默认10条
    Returns:
        联网搜索结果返回结构
    """
    logger.info(f"Received web_search tool request with query: {Query}")

    try:
        if config is None:
            raise ValueError("config not loaded")
        
        # Validate Count parameter
        if Count > 50:
            Count = 50
        elif Count < 1:
            Count = 10
            
        req = WebSearchRequest(
            Query=Query,
            Count=Count
        )
        
        if config.api_key is not None and len(config.api_key) > 0:
            resp = web_search_api_key_auth(config.api_key, req, "web_search")
            resp.raise_for_status()
            logger.info(f"Received web_search_api_key_auth response")
            return resp.json()
        else:
            resp = web_search_volcengine_auth(config.volcengine_ak, config.volcengine_sk, req, "web_search")
            resp.raise_for_status()
            logger.info(f"Received web_search_volcengine_auth response")
            return resp.json()
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
    parser = argparse.ArgumentParser(description="Run the AskEchoSearchInfinity MCP Server")
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
        logger.info(f"Starting AskEchoSearchInfinity MCP Server with {args.transport} transport")
        mcp.run(transport=args.transport)
    except Exception as e:
        logger.error(f"Error starting AskEchoSearchInfinity MCP Server: {str(e)}")
        raise


if __name__ == "__main__":
    main()