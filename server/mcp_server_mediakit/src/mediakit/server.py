from __future__ import annotations

import argparse
import asyncio
import os
import sys

from dotenv import load_dotenv

from base.base_mcp import BaseMCP
from base.client import create_client

from .mcp_server import register_categories

load_dotenv()

INSTRUCTIONS_TEXT = (
    "## MediaKit MCP is the MediaKit MCP Server\n"
    "### Before using the MediaKit service, please note:\n"
    "- 同步任务直接返回结果\n"
    "- 异步任务返回 task_id, 使用 task_id, 调用 query_task 查询任务状态\n"
    "- 默认开启幂等：相同账户 + 核心请求参数在 2 天内重复提交时，服务会直接返回首次任务结果，不会重复创建任务\n"
    "- 如需主动控制幂等，可传 client_token；请求重试时复用同一值，强制重新执行时必须传新的唯一值\n"
    "- client_token 由客户端生成，长度不超过 64 个字符\n"
)

mcp = BaseMCP(
    name="MediaKit MCP",
    host=os.getenv("MCP_SERVER_HOST", "0.0.0.0"),
    port=int(os.getenv("MCP_SERVER_PORT", "8000")),
    stateless_http=os.getenv("STATLESS_HTTP", "true").lower() == "true",
    streamable_http_path=os.getenv("STREAMABLE_HTTP_PATH", "/mcp"),
    instructions=INSTRUCTIONS_TEXT,
)


def main() -> None:
    try:
        parser = argparse.ArgumentParser(description="Run the MediaKit MCP Server")
        parser.add_argument(
            "--transport",
            "-t",
            choices=["streamable-http", "stdio"],
            default="stdio",
            help="Transport protocol to use (streamable-http or stdio)",
        )
        args = parser.parse_args()

        # 初始化 MCP Server：创建 client、绑定 mcp、注册 tools
        client = create_client()
        client.set_mcp_instance(mcp)
        mcp.set_base_mcp_store({"apiRequestInstance": client})
        register_categories(mcp, client)

        asyncio.run(mcp.run(transport=args.transport))
    except Exception as e:
        print(f"Error occurred while starting the server: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
