# coding:utf-8

from src.vod.mcp_server import create_mcp_server
from mcp.server.fastmcp import FastMCP
from src.base.base_mcp import BaseMCP
from dotenv import load_dotenv
import os
import asyncio
import sys
import argparse

load_dotenv()

mcp = BaseMCP(
        name="VOD MCP",
        host=os.getenv("MCP_SERVER_HOST", "0.0.0.0"),
        port=int(os.getenv("MCP_SERVER_PORT", "8000")),
        stateless_http=os.getenv("STATLESS_HTTP", "true").lower() == "true",
        streamable_http_path=os.getenv("STREAMABLE_HTTP_PATH", "/mcp"),
        instructions="""
        ## VOD MCP is the Volcengine VOD MCP Server.
        ### Before using the VOD service, please note:
        - `SpaceName` is the name of the VOD space.
        - `Vid` is the video ID, 示例：v02399g100***2qpj9aljht4nmunv9ng.
        - `DirectUrl` 指定资源的 FileName。示例：test.mp3
        """,
    )

    
def init_mcp () -> FastMCP:
    return mcp

def main():
    try:
        parser = argparse.ArgumentParser(description="Run the VOD MCP Server")
        parser.add_argument(
            "--transport",
            "-t",
            choices=["streamable-http", "stdio"],
            default="stdio",
            help="Transport protocol to use (streamable-http or stdio)",
        )
        args = parser.parse_args()
       
        mcp_instance = create_mcp_server(mcp)

        asyncio.run(mcp_instance.run(transport=args.transport))
    except Exception as e:
        print(f"Error occurred while starting the server: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
