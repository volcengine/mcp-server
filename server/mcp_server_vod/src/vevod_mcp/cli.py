 # Copyright 2025 Beijing Volcano Engine Technology Ltd.
 # SPDX-License-Identifier: MIT
import asyncio
import sys
from dotenv import load_dotenv

from vevod_mcp import create_mcp_server

def main():
    """命令行入口点，用于启动 VOD MCP 服务器"""

    # 加载环境变量
    load_dotenv()

    try:
        # 创建MCP服务器
        mcp = create_mcp_server()

        asyncio.run(mcp.run())
    except Exception as e:
        print(f"启动服务器时出错: {e}", file=sys.stderr)
        sys.exit(1)
