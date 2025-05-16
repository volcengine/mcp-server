# coding:utf-8

from vcloud.veen.mcp_server import create_mcp_server
from dotenv import load_dotenv
import asyncio

load_dotenv()

mcp = create_mcp_server()
if __name__ == "__main__":
    asyncio.run(mcp.run())
