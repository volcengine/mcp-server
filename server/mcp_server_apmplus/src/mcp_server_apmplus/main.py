import argparse
import logging
import os
from typing import Optional

from mcp_server_apmplus.config import load_config, ApmplusConfig, ENV_MCP_SERVER_MODE
from mcp_server_apmplus.server import mcp

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Global variables
config: Optional[ApmplusConfig] = None


def main():
    parser = argparse.ArgumentParser(description="Run the APMPlus MCP Server")
    parser.add_argument(
        "--transport",
        "-t",
        choices=["sse", "stdio", "streamable-http"],
        default=os.getenv(ENV_MCP_SERVER_MODE, "stdio"),
        help="Transport protocol to use (sse, stdio or streamable-http)",
    )

    args = parser.parse_args()

    try:
        # Load configuration from environment variables
        global config

        config = load_config()

        # Run the MCP server
        logger.info(f"Starting APMPlus MCP Server with {args.transport} transport")

        mcp.run(transport=args.transport)
    except Exception as e:
        logger.error(f"Error starting APMPlus MCP Server: {str(e)}")
        raise


if __name__ == "__main__":
    main()
