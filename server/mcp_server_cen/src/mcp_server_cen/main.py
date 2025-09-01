import argparse
import logging

from mcp_server_cen.server import mcp

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Run the CEN MCP Server")
    parser.add_argument(
        "--transport", "-t",
        choices=["stdio", "streamable-http"],
        default="stdio",
        help="Transport protocol to use stdio"
    )
    args = parser.parse_args()

    try:
        # Run the MCP server
        logger.info(f"Starting CEN MCP Server with {args.transport} transport")
        mcp.run(transport=args.transport)
    except Exception as e:
        logger.error(f"Error starting CEN MCP Server: {str(e)}")
        raise


if __name__ == "__main__":
    main()
