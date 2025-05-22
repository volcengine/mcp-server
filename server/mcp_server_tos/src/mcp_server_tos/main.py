import logging
import argparse

from mcp_server_tos.server import mcp

from mcp_server_tos.config import TOS_CONFIG

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Run the TOS MCP Server")
    parser.add_argument(
        "--transport", "-t",
        choices=["sse", "stdio"],
        default="stdio",
        help="Transport protocol to use (sse or stdio)"
    )

    args = parser.parse_args()

    try:
        # Run the MCP server
        logger.info(f"Starting TOS MCP Server with {args.transport} transport, region is {TOS_CONFIG.region}")

        mcp.run(transport=args.transport)
    except Exception as e:
        logger.error(f"Error starting TOS MCP Server: {str(e)}")
        raise


if __name__ == "__main__":
    main()
