import argparse
import logging
import os
import requests
import json

from typing import Dict, Optional, Final, Any
from mcp.server import FastMCP
from mcp_server_aisearch.config import config
from mcp_server_aisearch.common.auth import prepare_request

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# # knowledge base domain
g_aisearch_engine_domain = "aisearch.cn-beijing.volces.com"

# paths
search_path = "/api/v1/application/${applicationId}/search"
chat_search_path = "/api/v1/application/${applicationId}/chat_search"
# Create MCP server
mcp = FastMCP("AISearch Engine MCP Server", port=int(os.getenv("PORT", "8000")))

@mcp.tool()
def search(application_id: str, dataset_id: str, text: str = None, image_url: str = None, filter: dict = None, page_number: int = 1, page_size: int = 10) -> Dict[str, Any]:
    """
    This is a basic search tool without conversational capabilities. It can query the corresponding dataset based on the user's text or image query and return the raw search results. 
    The search tool cannot be used without the datasetId input parameter. You can try using the chat_search tool based on the original query.

    Args:
        application_id (str): The application ID for the search.
        dataset_id (str): The ID of the dataset to search in.
        text (str, optional): The search query text. Either text or image_url must be provided.
        image_url (str, optional): The URL of the image to search with. Either text or image_url must be provided.
        filter (dict, optional): Filter conditions for search results. Supports must, must_not, range operators and and, or logical operators.
                                Format: {"op": "must", "field": "status", "conds": [1,2]}.
                                - op (required): Operator type, supports "must", "must_not", "range", "and", "or".
                                - field (required for must, must_not, range): The field to apply the filter condition.
                                - conds (required for must, must_not): List of values to filter by.
                                - conds (required for and, or): Nested filter conditions.
                                Leave empty or None to apply no filter. Defaults to None.
        page_number (int, optional): The page number of results to retrieve. Defaults to 1.
        page_size (int, optional): The number of results per page. Defaults to 10.

    Returns:
        dict[str, Any]: A dictionary containing the search results.
    """
    # Validate that either text or image_url is provided, but not both
    if (text is None or text == "") and (image_url is None or image_url == ""):
        raise ValueError("Either text or image_url must be provided")
    if(application_id is None or application_id == ""):
        raise ValueError("application_id must be provided")
    if(dataset_id is None or dataset_id == ""):
        raise ValueError("dataset_id must be provided")

    logger.info(f"Received search tool request: applicationId = {application_id},text={text}, image_url={image_url}, filter={filter}, page_number={page_number}, page_size={page_size}, dataset_id={dataset_id}")
    
    try:
        request_params = {
            "query": {
                "text": text,
                "image_url": image_url
            },
            "page_number": page_number,
            "page_size": page_size,
            "filter": filter,
            "dataset_id": dataset_id
        }
        temp_search_path = search_path.replace("${applicationId}", application_id)
        search_req = prepare_request(method="POST", path=temp_search_path, ak=config.ak, sk=config.sk, data=request_params)
        logger.info(f"Request: {search_req.headers}, body:{search_req.body}, url: https://{g_aisearch_engine_domain}{search_req.path}")
        rsp = requests.request(
            method=search_req.method,
            url="https://{}{}".format(g_aisearch_engine_domain, search_req.path),
            headers=search_req.headers,
            data=search_req.body)

        result = rsp.json()
        logger.info(f"Response: {result}")
        if "error" in result:
            logger.error(f"Error in search: {result['error']}")
            return {"error": result['error']}

        return result
    except Exception as e:
        logger.error(f"Error in search: {str(e)}")
        return {"error": str(e)}

@mcp.tool()
def chat_search(application_id: str, session_id: str, text: str = None, image_url: str = None, search_limit: int = 10, dataset_ids: list = None, filters: dict = None) -> Dict[str, Any]:
    """
    Perform a chat-based search using AI capabilities to answer user questions based on datasets.
    This Tool is only applicable to conversational search scenarios and cannot be used to query the dataset collections under an application. If a non-conversational search or retrieval is required, 
    the search tool should be used instead.

    Args:
        application_id (str): The application ID for the search.
        session_id (str): The unique identifier for the chat session.
        text (str, optional): The search query text. Either text or image_url must be provided.
        image_url (str, optional): The URL of the image to search with. Either text or image_url must be provided.
        search_limit (int, optional): The maximum number of search results to return. Defaults to 10.
        dataset_ids (list[str], optional): List of dataset IDs to search in. Defaults to None.
        filters (dict, optional): Filter conditions for search results, applied per dataset.
                                 Format: {"dataset_id": {"op": "must", "field": "status", "conds": [1,2]}}.
                                 - op (required): Operator type, supports "must", "must_not", "range", "and", "or".
                                 - field (required for must, must_not, range): The field to apply the filter condition.
                                 - conds (required for must, must_not): List of values to filter by.
                                 - conds (required for and, or): Nested filter conditions.
                                 Leave empty or None to apply no filter. Defaults to None.
    Returns:
        dict[str, Any]: A dictionary containing the chat search results, including related items data.
    """
    # Validate that either text or image_url is provided, but not both
    if (text is None or text == "") and (image_url is None or image_url == ""):
        raise ValueError("Either text or image_url must be provided")
    if(application_id is None or application_id == ""):
        raise ValueError("application_id must be provided")
    if(session_id is None or session_id == ""):
        raise ValueError("session_id must be provided")

    logger.info(f"Received chat_search tool request: applicationId = {application_id}, session_id={session_id}, text={text}, image_url={image_url}, search_limit={search_limit}, dataset_ids={dataset_ids}, filters={filters}")
    try:
        # 构造 input_message 的 content 数组
        content = []
        if text:
            content.append({"type": "text", "text": text})
        if image_url:
            content.append({
                "type": "image_url", 
                "image_url": {
                    "url": image_url
                }
            })

        request_params = {
            "session_id": session_id,
            "input_message": {
                "content": content
            },
            "search_param": {
                "limit": search_limit,
                "dataset_ids": dataset_ids,
                "filters": filters
            }
        }
        temp_chat_search_path = chat_search_path.replace("${applicationId}", application_id)
        search_req = prepare_request(method="POST", path=temp_chat_search_path, ak=config.ak, sk=config.sk, data=request_params)
        rsp = requests.request(
            method=search_req.method,
            url="https://{}{}".format(g_aisearch_engine_domain, search_req.path),
            headers=search_req.headers,
            data=search_req.body,
            stream=True)
        rsp.raise_for_status()
        start_marker_checked = False
        full_response = ""
        related_items = []
        for line in rsp.iter_lines(decode_unicode=True):
            if line:  # 跳过空行
                try:
                    data = json.loads(line)
                    result = data.get("result", {})
                    
                    # 检查step_info中的step类型
                    step_info = result.get("step_info")
                    step = None
                    if step_info and isinstance(step_info, dict):
                        step = step_info.get("step")
            
                    if step == "reply":
                        start_marker_checked = True
                    
                    # 只有在reply步骤后才收集content
                    if start_marker_checked and "content" in result:
                        # 获取当前片段
                        content_fragment = result["content"]
                        # 拼接片段到完整回复
                        full_response += content_fragment
                        logger.info(f"拼接后内容: {full_response}")

                    # 提取 related_items
                    if "payload" in result and "related_items" in result["payload"]:
                        related_items = result["payload"]["related_items"]

                    # 处理结束标识（如果有）
                    if "stop_reason" in result and result["stop_reason"] == "stop":
                        logger.info("流式传输结束，完整回复已生成")
                        break

                except json.JSONDecodeError as e:
                    logger.error(f"解析单行JSON失败: {e}，内容: {line}")
        
        # 返回包含content和related_items的字典
        return {
            "content": full_response,
            "related_items": related_items
        }
    except Exception as e:
        logger.error(f"Error in chat_search: {str(e)}")
        return {"error": str(e)}
    finally:
        if 'rsp' in locals():
            rsp.close()  # 确保连接关闭

def main():
    """Main entry point for the AISearch Engine MCP server."""
    parser = argparse.ArgumentParser(description='Run the AISearch Engine MCP Server')
    parser.add_argument(
        "--transport",
        "-t",
        choices=["stdio", "streamable-http"],
        default="stdio",
        help="Transport protocol to use (stdio or streamable-http)",
    )
    args = parser.parse_args()
    logger.info(f"Starting AISearch Engine MCP Server with {args.transport} transport")
    try:
        mcp.run(transport=args.transport)
    except Exception as e:
        logger.error(f"Error starting AISearch Engine MCP Server: {str(e)}")
        raise

if __name__ == "__main__":
    main()
