"""
EMR MCP Server
"""
import argparse
import logging

from server.mcp_server_emr.src.mcp_server_emr.emr_mcp_server import mcp

logger = logging.getLogger(__name__)


def main():
    """Main entry point for the MCP server."""
    parser = argparse.ArgumentParser(description="Run the EMR MCP Server")
    parser.add_argument(
        "--transport",
        "-t",
        choices=["streamable-http", "stdio"],
        default="streamable-http",
        help="Transport protocol to use (streamable-http or stdio)",
    )

    args = parser.parse_args()

    try:
        # Run the MCP server
        logger.info(f"Starting EMR MCP Server with {args.transport} transport")
        mcp.run(transport=args.transport)
    except Exception as e:
        logger.error(f"Error starting EMR MCP Server: {str(e)}")
        raise


if __name__ == "__main__":
    main()
