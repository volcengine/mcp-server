"""
ECS MCP Server.

This server provides MCP tools to interact with ECS OpenAPI.
"""

import argparse

from mcp_server_ecs.common.logs import LOG
from mcp_server_ecs.tools import event, instance, mcp, region


def main():
    parser = argparse.ArgumentParser(description="Run the ECS MCP Server")
    parser.add_argument(
        "--transport",
        "-t",
        choices=["sse", "stdio", "streamable-http"],
        default="stdio",
        help="Transport protocol to use (sse or stdio)",
    )

    args = parser.parse_args()
    LOG.info(
        f"Including tool types: {event.__name__}, {instance.__name__}, {region.__name__}"
    )
    LOG.info(f"Starting ECS MCP Server with {args.transport} transport")

    mcp.run(transport=args.transport)


if __name__ == "__main__":
    main()
