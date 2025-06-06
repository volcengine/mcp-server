import argparse
import logging
import os
import requests

from typing import Dict, Optional, Final, Any
from mcp.server import FastMCP
from mcp_server_vikingdb.config import config
from mcp_server_vikingdb.common.auth import prepare_request

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# knowledge base domain
g_vikingdb_domain = "api-vikingdb.volces.com"

# paths
search_path = "/api/index/search"

# Create MCP server
mcp = FastMCP("Vikingdb MCP Server", port=int(os.getenv("PORT", "8000")))

@mcp.tool()
def search_vikingdb(
        query: str,
        limit: int = 3,
) -> Dict:
    """Use the MCP Server to search within the Vikingdb service and retrieve the top `limit` relevant data records based on your query.
    This tool enables you to search text data within the provided collection using the specified query.

    Args:
        query: The text string used for the search.
        limit: The maximum number of search results to be returned. The default value is 3.
    """

    try:
        request_params = {
            "collection_name": config.vikingdb_collection_name,
            "index_name": config.vikingdb_index_name,
            "search": {
                "order_by_raw":{
                    "text": query,
                },
                "dense_weight": 0.5,
                "limit": limit,
            }
        }

        search_req = prepare_request(method="POST", path=search_path, ak=config.ak, sk=config.sk, data=request_params)
        rsp = requests.request(
            method=search_req.method,
            url="https://{}{}".format(g_vikingdb_domain, search_req.path),
            headers=search_req.headers,
            data=search_req.body)

        result = rsp.json()
        if result['code'] != 0:
            logger.error(f"Error in search: {result['message']}")
            return {"error": result['message']}

        return result['data']
    except Exception as e:
        logger.error(f"Error in search: {str(e)}")
        return {"error": str(e)}


def main():
    """Main entry point for the Vikingdb MCP server."""
    parser = argparse.ArgumentParser(description='Run the Vikingdb MCP Server')
    parser.add_argument(
        "--transport",
        "-t",
        choices=["sse", "stdio"],
        default="stdio",
        help="Transport protocol to use (sse or stdio)",
    )
    args = parser.parse_args()
    logger.info(f"Starting Vikingdb MCP Server with {args.transport} transport")

    try:
        # Run the MCP server
        logger.info( f"Starting Vikingdb MCP Server with {args.transport} transport")

        mcp.run(transport=args.transport)
    except Exception as e:
        logger.error(f"Error starting Vikingdb MCP Server: {str(e)}")
        raise

if __name__ == "__main__":
    main()