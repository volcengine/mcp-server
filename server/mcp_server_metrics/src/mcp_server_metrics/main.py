#!/usr/bin/env python3

import argparse
import logging
import sys

from mcp_server_metrics.server import mcp


def main():
    """Main entry point for the Metrics MCP Server."""
    parser = argparse.ArgumentParser(
        description="Run the Metrics MCP Server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--transport",
        "-t",
        choices=["sse", "stdio", "streamable-http"],
        default="stdio",
        help="Transport protocol to use (sse, stdio or streamable-http)",
    )
    parser.add_argument(
        "--port",
        "-p",
        type=int,
        default=8000,
        help="Port to use for streamable-http transport",
    )
    parser.add_argument(
        "--host",
        "-H",
        default="127.0.0.1",
        help="Host to use for streamable-http transport",
    )
    parser.add_argument(
        "--log-level",
        "-l",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Logging level",
    )

    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        stream=sys.stdout,
    )

    logger = logging.getLogger(__name__)
    logger.info(f"Starting Metrics MCP Server with {args.transport} transport")

    try:
        mcp.run(transport=args.transport)
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()