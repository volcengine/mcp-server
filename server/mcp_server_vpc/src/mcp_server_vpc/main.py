"""
VPC MCP Server.
"""

import argparse

from mcp_server_vpc.common import errors
from mcp_server_vpc.common.logs import logger
from mcp_server_vpc.server import mcp
from mcp_server_vpc.tools import havip # noqa: for side-effects
from mcp_server_vpc.tools import network_acl # noqa: for side-effects
from mcp_server_vpc.tools import network_interface # noqa: for side-effects
from mcp_server_vpc.tools import prefix_list # noqa: for side-effects
from mcp_server_vpc.tools import route_table # noqa: for side-effects
from mcp_server_vpc.tools import security_group # noqa: for side-effects
from mcp_server_vpc.tools import subnet # noqa: for side-effects
from mcp_server_vpc.tools import vpc # noqa: for side-effects


def main():
    parser = argparse.ArgumentParser(description="Run VPC MCP Server")
    parser.add_argument(
        "--transport",
        "-t",
        choices=["stdio", "streamable-http"],
        default="stdio",
        help="transport protocol",
    )
    args = parser.parse_args()

    try:
        logger.info("Starting %s in %s transport mode", __name__, args.transport)
        mcp.run(transport=args.transport)
    except Exception as e:
        raise errors.VPCError(f"failed to start {__name__}", e)


if __name__ == "__main__":
    main()
