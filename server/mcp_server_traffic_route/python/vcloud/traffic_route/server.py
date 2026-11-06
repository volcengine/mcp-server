# coding:utf-8
from vcloud.traffic_route.mcp_server import create_mcp_server
from dotenv import load_dotenv

load_dotenv()

mcp = create_mcp_server()
if __name__ == "__main__":
    mcp.run()
