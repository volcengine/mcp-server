"""
ECS MCP Server.

This server provides MCP tools to interact with ECS OpenAPI.
"""

import argparse

from mcp_server_ecs.common.logs import LOG
from mcp_server_ecs.server import serve
from mcp_server_ecs.tools import event, instance, region


def main():
    parser = argparse.ArgumentParser(description="Run the ECS MCP Server")
    parser.add_argument(
        "--transport",
        "-t",
        choices=["sse", "stdio"],
        default="stdio",
        help="Transport protocol to use (sse or stdio)",
    )

    args = parser.parse_args()
    LOG.info(f"Starting ECS MCP Server with {args.transport} transport")

    serve(args.transport)


if __name__ == "__main__":
    main()
