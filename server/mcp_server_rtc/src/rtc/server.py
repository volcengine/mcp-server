# coding:utf-8

from src.rtc.mcp_server import create_mcp_server

from dotenv import load_dotenv
import asyncio
import sys
import argparse

load_dotenv()


def main():
    try:
        parser = argparse.ArgumentParser(description="Run the RTC MCP Server")
        parser.add_argument(
            "--transport",
            "-t",
            choices=["streamable-http", "stdio"],
            default="stdio",
            help="Transport protocol to use (streamable-http or stdio)",
        )
        args = parser.parse_args()
        print(args.transport)
        mcp = create_mcp_server()

        asyncio.run(mcp.run(transport=args.transport))
    except Exception as e:
        print(f"Error occurred while starting the server: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
