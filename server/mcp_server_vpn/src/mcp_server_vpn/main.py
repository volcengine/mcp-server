import argparse
import logging

from mcp_server_vpn.server import mcp

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the VPN MCP Server")
    parser.add_argument(
        "--transport",
        "-t",
        choices=["sse", "stdio", "streamable-http"],
        default="stdio",
        help="Transport protocol to use",
    )
    args = parser.parse_args()

    logger.info("Starting VPN MCP Server with %s transport", args.transport)
    mcp.run(transport=args.transport)


if __name__ == "__main__":
    main()
