import argparse
import logging
import os
import requests

from typing import Dict, Optional, Final, Any
from mcp.server import FastMCP
from mcp_server_memory.config import config
from mcp_server_memory.common.auth import prepare_request
from mcp_server_memory.common.memory_client import VikingDBMemoryService, VikingDBMemoryException
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
import time
# knowledge base domain
g_knowledge_base_domain = "api-memory.mlp.cn-beijing.volces.com"

# paths
search_knowledge_path = "/api/knowledge/collection/search_knowledge"
list_collections_path = "/api/knowledge/collection/list"
get_collections_path = "/api/knowledge/collection/info"
doc_add_path = "/api/knowledge/doc/add"
doc_info_path = "/api/knowledge/doc/info"

# Create MCP server
mcp = FastMCP("Memory MCP Server", port=int(os.getenv("PORT", "8000")))



vm = VikingDBMemoryService(ak=config.ak, sk=config.sk) # 替换成你的ak sk



# 创建 collection
collection_name="test_case"
builtin_event_type="sys_common"
try:
    rsp = vm.create_collection(collection_name=collection_name, description="", builtin_event_types=[builtin_event_type])
    print(rsp)
except Exception as e:
    print(f"create_collection occurs error: {e}")
# rsp {'ResponseMetadata': {'Action': '', 'Region': 'cn-beijing', 'RequestId': 'xxx', 'Service': 'knowledge_base_server', 'Version': ''}, 'Result': {'resource_id': 'mem-xxx'}}


@mcp.tool()
def add_memories(
        text: str
) -> str:
    """
    添加新记忆。每当用户告知任何关于他们自己的信息、他们的偏好，或任何具有可在未来对话中派上用场的相关信息时，都会调用此方法。当用户要求你记住某事时，也可调用此方法。
    Args:
         text: 用户说的话
    Returns:


    """
    try:
        # 添加消息
        session_id = "test_id"
        messages = [
            {"role": "user", "content": text}
        ]
        metadata = {
            "default_user_id": config.user_id,
            "default_assistant_id": 'assistant',
            "time": int(time.time() * 1000)
        }
        try:
            rsp = vm.add_messages(collection_name=collection_name, session_id=session_id, messages=messages,
                                  metadata=metadata)
            print(rsp)
        except Exception as e:
            print(f"add_messages occurs error: {e}")
        # rsp {'code': 0, 'data': {}, 'message': 'success', 'request_id': 'xxxx'}
        return '记忆已更新'

    except Exception as e:
        logger.error(f"Error in add_doc: {str(e)}")
        return {"error": str(e)}


@mcp.tool()
def search_memory(
        query: str
) -> str:
    """
    搜索已存储的记忆。每当用户提出任何问题时，都会调用此方法。
    Args:
         query: 用户提出的任何问题.
    Returns:
        用户与query相关的记忆
    """

    try:

        # 搜索记忆
        limit = 5
        filter = {
            "user_id": config.user_id,
            "memory_type": [builtin_event_type],
        }
        try:
            rsp = vm.search_memory(collection_name=collection_name, query=query, filter=filter, limit=limit)
            print(rsp)
        except Exception as e:
            print(f"search_memory occurs error: {e}")

        return str(rsp)

    except Exception as e:
        logger.error(f"Error in get_doc: {str(e)}")
        return {"error": str(e)}


def main():
    """Main entry point for the Knowledgebase MCP server."""
    parser = argparse.ArgumentParser(description='Run the Viking Knowledgebase MCP Server')
    parser.add_argument(
        "--transport",
        "-t",
        choices=["sse", "stdio"],
        default="stdio",
        help="Transport protocol to use (sse or stdio)",
    )
    args = parser.parse_args()
    logger.info(f"Starting Knowledgebase MCP Server with {args.transport} transport")

    try:
        # Run the MCP server
        logger.info( f"Starting Viking Knowledge Base MCP Server with {args.transport} transport")

        mcp.run(transport=args.transport)
    except Exception as e:
        logger.error(f"Error starting Knowledgebase MCP Server: {str(e)}")
        raise

if __name__ == "__main__":
    main()