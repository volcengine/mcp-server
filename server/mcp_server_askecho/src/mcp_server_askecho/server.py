import logging
import argparse
import dataclasses
import asyncio
import os
from mcp.server import FastMCP
from mcp.server.fastmcp import Context
from mcp import types
from typing import Dict, Any

from .model import *
from .config import *
from .api.api_key_auth import *
from .api.volcengine_auth import *

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

config = None
mcp = FastMCP("AskEcho MCP Server",
              host=os.getenv("MCP_SERVER_HOST", "0.0.0.0"),
              port=int(os.getenv("MCP_SERVER_PORT", "8000")),
              streamable_http_path=os.getenv("STREAMABLE_HTTP_PATH", "/mcp"))


@mcp.tool()
async def chat_completion(
        messages: list[Message]
) -> Dict[str, Any]:
    """
    联网问答智能体会话工具，根据用户输入问题，提供基于联网搜索的大模型总结后回复内容
    Args:
        messages (List[Dict[str, str]]): 对话消息列表，按顺序排列，包含历史消息与当前用户输入
            - role (str): 消息角色类型
            - content (str): 该轮消息的具体内容

    Returns:
        结构化的大模型基于联网搜索给出的总结回复
    """
    logger.info(f"Received chat_completion tool request")

    try:
        if config is None:
            raise ValueError("config not loaded")
        messages.insert(0, Message(
            role="system",
            content="回答使用简短清晰的语言（300字以内）",
        ))
        req = OriginChatCompletionRequest(
            bot_id=config.bot_id,
            stream=False,
            messages=messages,
            user_id="" if config.user_id is None else config.user_id
        )
        if config.api_key is not None and len(config.api_key) > 0:
            return await chat_completion_api_key_auth_api(config.api_key, req, "chat_completion")
        else:
            return await chat_completion_volcengine_auth(config.volcengine_ak, config.volcengine_sk, req,
                                                   "chat_completion")
    except Exception as e:
        logger.error(f"Error in chat_completion tool: {e}")
        resp_error = ResponseError(
            error=Error(
                message=str(e),
                type="mcp_server_askecho_error",
                code="mcp_server_askecho_error",
            )
        )
        return resp_error.to_dict()


def main():
    """Main entry point for the MCP server."""
    parser = argparse.ArgumentParser(description="Run the AskEcho MCP Server")
    parser.add_argument(
        "--transport",
        "-t",
        choices=["sse", "stdio", "streamable-http"],
        default="stdio",
        help="Transport protocol to use (sse, stdio or streamable-http)",
    )

    args = parser.parse_args()

    try:
        # Load configuration from environment variables
        global config
        config = load_config()
        # Run the MCP server
        logger.info(f"Starting AskEcho MCP Server with {args.transport} transport")
        mcp.run(transport=args.transport)
    except Exception as e:
        logger.error(f"Error starting AskEcho MCP Server: {str(e)}")
        raise


if __name__ == "__main__":
    main()
