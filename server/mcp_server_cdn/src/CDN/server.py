# coding:utf-8

from src.CDN.mcp_server import create_mcp_server
from dotenv import load_dotenv
import asyncio
import sys

load_dotenv()


def main():
    try:
        mcp = create_mcp_server()
        asyncio.run(mcp.run())
    except Exception as e:
        print(f"启动服务器时出错: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
