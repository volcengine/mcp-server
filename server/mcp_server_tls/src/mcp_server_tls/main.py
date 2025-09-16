import logging
import argparse

from mcp_server_tls.config import TLS_CONFIG
from mcp_server_tls.server import mcp
from mcp_server_tls.server import add_resources_to_mcp, add_tools_to_mcp

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Run the TLS MCP Server")
    parser.add_argument(
        "--transport", "-t",
        choices=["sse", "stdio", "streamable-http"],
        default="stdio",
        help="Transport protocol to use (sse or stdio)"
    )

    args = parser.parse_args()

    # Run the MCP server
    logger.info(f"Starting TLS MCP Server with {args.transport} transport, region is {TLS_CONFIG.region}")

    mcp.run(transport=args.transport)

if __name__ == "__main__":
    main()
