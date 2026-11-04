from __future__ import annotations

import argparse
import logging
import os
import sys

from base.faas_bootstrap import prefer_installed_site_packages

prefer_installed_site_packages()

from fastmcp import FastMCP

from base.constant import LOG_LEVEL_ENV, MEDIAKIT_API_KEY_ENV
from mediakit.middleware import ClientBindMiddleware, ToolFilterMiddleware

from .mcp_server import register_categories

logger = logging.getLogger(__name__)

INSTRUCTIONS_TEXT = (
    "## MediaKit MCP is the MediaKit MCP Server\n"
    "### Before using the MediaKit service, please note:\n"
    "- 同步任务直接返回结果\n"
    "- 异步任务返回 task_id, 使用 task_id, 调用 query_task 查询任务状态\n"
    "- 正常调用默认省略 client_token；仅转发调用方实际提供的值\n"
    "- 明确重试同一逻辑请求时复用同一个 client_token；业务参数变化后不得复用\n"
    "- MCP runtime 不推断重试意图，也不自动生成 client_token\n"
)

client_bind_mw = ClientBindMiddleware()

mcp = FastMCP(
    name="MediaKit MCP",
    instructions=INSTRUCTIONS_TEXT,
)
mcp.add_middleware(ToolFilterMiddleware())
mcp.add_middleware(client_bind_mw)


def _configure_logging() -> None:
    level_name = os.environ.get(LOG_LEVEL_ENV, "INFO").strip().upper()
    level = getattr(logging, level_name, logging.INFO)
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        stream=sys.stderr,
        force=True,
    )
    logger.info("MCP logging enabled at level %s", logging.getLevelName(level))


def _warn_shared_env_key_on_http(transport: str) -> None:
    if transport != "streamable-http":
        return
    if not os.environ.get(MEDIAKIT_API_KEY_ENV, "").strip():
        return
    logger.warning(
        "HTTP 模式下检测到 %s：未传 x-amk-api-key 的请求将共用该 Key。"
        "多租户部署请勿在服务器设置共享 API Key。",
        MEDIAKIT_API_KEY_ENV,
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
        _configure_logging()
        register_categories(mcp)
        _warn_shared_env_key_on_http(args.transport)

        if args.transport == "stdio":
            mcp.run(transport="stdio")
            return

        mcp.run(
            transport="streamable-http",
            host=os.getenv("MCP_SERVER_HOST", "0.0.0.0"),
            port=int(os.getenv("MCP_SERVER_PORT", "8000")),
            path=os.getenv("STREAMABLE_HTTP_PATH", "/mcp"),
            stateless_http=os.getenv("STATLESS_HTTP", "true").lower() == "true",
        )
    except Exception as e:
        print(f"Error occurred while starting the server: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
