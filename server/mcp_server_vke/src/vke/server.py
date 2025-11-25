# coding:utf-8
from dotenv import load_dotenv
import sys
import argparse

from .mcp_server import create_mcp_server

load_dotenv()


def main():
    try:
        parser = argparse.ArgumentParser(description="Run the VKE MCP Server")
        parser.add_argument(
            "--transport",
            "-t",
            choices=["streamable-http", "stdio", "sse"],
            default="stdio",
            help="Transport protocol to use (streamable-http, stdio or sse)",
        )
        args = parser.parse_args()
        print(f"Using transport protocol: {args.transport}")
        mcp = create_mcp_server()
        mcp.run(transport=args.transport)
    except Exception as e:
        print(f"Error occurred while starting the server: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
