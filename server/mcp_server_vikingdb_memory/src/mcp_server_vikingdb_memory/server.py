import argparse
import logging
import os
import string
import random
from typing import Dict, Optional, Final, Any
from mcp.server import FastMCP
from mcp_server_vikingdb_memory.config import config
from mcp_server_vikingdb_memory.common.auth import prepare_request
from mcp_server_vikingdb_memory.common.memory_client import VikingDBMemoryService, VikingDBMemoryException
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
import time
from datetime import datetime




# Create MCP server
mcp = FastMCP("Memory MCP Server", port=int(os.getenv("PORT", "8000")))



vm = VikingDBMemoryService(ak=config.ak, sk=config.sk) # 替换成你的ak sk


# 创建 collection
collection_name=config.collection_name

def generate_random_letters(length):
    # 生成包含所有大小写字母的字符集
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))


def format_milliseconds(timestamp_ms):
    """
    将毫秒级时间戳转换为 'YYYYMMDD HH:MM:SS' 格式的字符串

    参数:
    - timestamp_ms: 毫秒级时间戳（整数或浮点数）

    返回:
    - 格式化后的时间字符串
    """
    # 将毫秒转换为秒
    timestamp_seconds = timestamp_ms / 1000

    # 转换为 datetime 对象
    dt = datetime.fromtimestamp(timestamp_seconds)

    # 按照指定格式输出
    return dt.strftime('%Y%m%d %H:%M:%S')

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
        session_id = generate_random_letters(10)
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
            return str(rsp)
        except Exception as e:
            print(f"add_messages occurs error: {e}")
            return str(e)
        # rsp {'code': 0, 'data': {}, 'message': 'success', 'request_id': 'xxxx'}


    except Exception as e:
        logger.error(f"Error in add_memories: {str(e)}")
        return {"error": str(e)}


@mcp.tool()
def search_memory(
        query: str
) -> str:
    """
    搜索已存储的记忆。每当用户提出任何问题时，都会调用此方法。
    如果一次搜索没有结果后，在同一句对话中就不要重复搜索了
    搜索到记忆，用来补充你对用户的了解，用来回复用户的问题
    Args:
         query: 用户提出的任何问题.
    Returns:
        用户与query相关的记忆
    """

    try:

        result = ""

        try:
            limit = 1
            filter = {
                "user_id": config.user_id,
                "memory_type": ['sys_profile_v1'],
            }
            rsp = vm.search_memory(collection_name=collection_name, query='sys_profile_v1', filter=filter, limit=limit)
            profiles = [item.get('memory_info').get('user_profile') for item in rsp.get('data').get('result_list')]
            if len(profiles)>0:
                result += f'''
用户画像 (trace_id = {rsp.get('request_id')})：
{profiles[0]}


    '''
            print(rsp)
        except Exception as e:
            result+=str(e)
            print(f"search_memory occurs error: {e}")

        try:
            # 搜索记忆
            limit = 5
            filter = {
                "user_id": config.user_id,
                "memory_type": ['sys_event_v1'],
            }
            rsp = vm.search_memory(collection_name=collection_name, query=query, filter=filter, limit=limit)
            content = "\n".join([f'{format_milliseconds(item.get("time"))} - {item.get("memory_info").get("summary")}' for item in
                       rsp.get('data').get('result_list')])
            result += f'''
事件记忆 (trace_id = {rsp.get('request_id')})：
{content}
'''
            print(rsp)
        except Exception as e:
            result += str(e)
            print(f"search_memory occurs error: {e}")

        return result

    except Exception as e:
        logger.error(f"Error in get_doc: {str(e)}")
        return str(e)


def main():
    """Main entry point for the Memory MCP server."""
    parser = argparse.ArgumentParser(description='Run the Viking Memory MCP Server')
    parser.add_argument(
        "--transport",
        "-t",
        choices=["stdio", "streamable-http"],
        default="stdio",
        help="Transport protocol to use (stdio or streamable-http)",
    )
    args = parser.parse_args()
    logger.info(f"Starting Memory MCP Server with {args.transport} transport")

    try:
        # Run the MCP server
        logger.info( f"Starting Viking Memory MCP Server with {args.transport} transport")

        mcp.run(transport=args.transport)
    except Exception as e:
        logger.error(f"Error starting Memory MCP Server: {str(e)}")
        raise

if __name__ == "__main__":
    main()