# coding:utf-8

from .mcp_server import create_mcp_server
from dotenv import load_dotenv
import asyncio
import sys
import argparse
import logging

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Run the veImageX MCP Server")
    parser.add_argument(
        "--transport", "-t",
        choices=["sse", "stdio"],
        default="stdio",
        help="Transport protocol to use (sse or stdio)"
    )
    args = parser.parse_args()

    try:
        mcp = create_mcp_server()
        logger.info("Starting MCP Server veImageX with %s transport", args.transport)
        asyncio.run(mcp.run(transport=args.transport))
    except Exception as e:
        logger.error(f"Error starting veImageX MCP Server: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
