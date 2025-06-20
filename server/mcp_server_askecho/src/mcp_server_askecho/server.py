import logging
import argparse
import dataclasses
from mcp.server import FastMCP

from .model import *
from .config import *
from .api import *

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

config = None
mcp = FastMCP("AskEcho MCP Server")


@mcp.tool()
def chat_completion(
        query: str,
) -> str:
    """
    联网问答智能体会话工具，基于联网搜索结果，提供端到端的AI问答能力
    Args:
        query: 搜索问题
    Returns:
        结构化的大模型基于联网搜索给出的总结回复
    """
    logger.info(f"Received chat_completion tool request with query: {query}")

    try:
        if config is None:
            raise ValueError("config not loaded")
        req = OriginChatCompletionRequest(
            bot_id=config.bot_id,
            stream=False,
            messages=[
                Message(
                    role="system",
                    content="回答使用简短清晰的语言（300字以内）",
                ),
                Message(
                    role="user",
                    content=query,
                )
            ],
        )
        origin_api_resp = chat_completion_api(config.volcengine_ak, config.volcengine_sk, req)
        logger.info(f"Received chat_completion_api response")
        api_resp = OriginChatCompletionResponse.from_dict(origin_api_resp)
        if len(api_resp.id) > 0:
            response = Response(
                log_id=api_resp.id,
                content=api_resp.choices[0].message.content if api_resp.choices else "",
                references=api_resp.references
            )
            return json.dumps(dataclasses.asdict(response), ensure_ascii=False)
        else:
            logger.error(f"Error in chat_completion_api: {origin_api_resp}")
            return json.dumps(origin_api_resp, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Error in chat_completion tool: {e}")
        resp_error = ResponseError(
            error=Error(
                message=str(e),
                type="mcp_server_askecho_error",
                code="mcp_server_askecho_error",
            )
        )
        return json.dumps(dataclasses.asdict(resp_error), ensure_ascii=False)


def main():
    """Main entry point for the MCP server."""
    parser = argparse.ArgumentParser(description="Run the AskEcho MCP Server")
    parser.add_argument(
        "--transport",
        "-t",
        choices=["sse", "stdio"],
        default="stdio",
        help="Transport protocol to use (sse or stdio)",
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
