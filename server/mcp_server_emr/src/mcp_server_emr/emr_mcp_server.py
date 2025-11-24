# 导入工具模块，确保工具被注册
import logging
import os
from typing import List, Dict, Any

from mcp.server.fastmcp import FastMCP

from mcp_server_emr.api.on_ecs_api import list_clusters
from mcp_server_emr.api.on_serverless_api import list_serverless_jobs
from mcp_server_emr.api.on_vke_api import list_virtual_clusters

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create server
mcp = FastMCP("EMR MCP Server",
              host=os.getenv("MCP_SERVER_HOST", os.getenv("MCP_SERVER_HOST", "0.0.0.0")),
              port=int(os.getenv("MCP_SERVER_PORT", int(os.getenv("PORT", "8000")))),
              streamable_http_path=os.getenv("STREAMABLE_HTTP_PATH", os.getenv("STREAMABLE_HTTP_PATH", "/mcp")),
              stateless_http=os.getenv("STATLESS_HTTP", "true").lower() == "true")


@mcp.tool()
def list_emr_on_serverless_jobs(
        limit: int = 20,
        offset: int = 0,
) -> List[Dict[str, Any]]:
    """
    获取EMR on Serverless作业列表

    Args:
        limit: 每页数量，默认20
        offset: 页码，从0开始

    Returns:
        作业列表
    """
    try:
        # 过滤作业数据
        request_body = {
            "Limit": str(limit),
            "Offset": str(offset),
        }
        access_key = os.environ.get("VOLCENGINE_ACCESS_KEY")
        secret_key = os.environ.get("VOLCENGINE_SECRET_KEY")
        region = os.environ.get("VOLCENGINE_REGION")
        if not all([access_key, secret_key, region]):
            logger.error("缺少必要的环境变量: VOLCENGINE_ACCESS_KEY, VOLCENGINE_SECRET_KEY, VOLCENGINE_REGION")
            return []

        response = list_serverless_jobs(access_key=access_key, secret_key=secret_key,
                                    region=region, request_body=request_body)
        jobs = response.get("Result", {}).get("JobList", [])

        # 转换为字典格式返回
        return jobs

    except Exception as e:
        logger.error(f"查询作业列表时出错: {str(e)}")
        return []


@mcp.tool()
def list_emr_on_ecs_clusters(page_size: int = 20) -> List[Dict[str, Any]]:
    """
    获取 EMR on ECS 形态的集群列表信息
    Args:
        page_size: 每页数量, 默认 20
    """
    access_key = os.environ.get("VOLCENGINE_ACCESS_KEY")
    secret_key = os.environ.get("VOLCENGINE_SECRET_KEY")
    region = os.environ.get("VOLCENGINE_REGION")
    if not all([access_key, secret_key, region]):
        logger.error("缺少必要的环境变量: VOLCENGINE_ACCESS_KEY, VOLCENGINE_SECRET_KEY, VOLCENGINE_REGION")
        return []
    return list_clusters(access_key, secret_key, region, page_size)


@mcp.tool()
def list_emr_on_vke_clusters(
        page_size: int = 20) -> List[Dict[str, Any]]:
    """
    获取 EMR on VKE 形态的虚拟集群列表信息
    Args:
        page_size: 每页数量, 默认 20
    """
    access_key = os.environ.get("VOLCENGINE_ACCESS_KEY")
    secret_key = os.environ.get("VOLCENGINE_SECRET_KEY")
    region = os.environ.get("VOLCENGINE_REGION")
    if not all([access_key, secret_key, region]):
        logger.error("缺少必要的环境变量: VOLCENGINE_ACCESS_KEY, VOLCENGINE_SECRET_KEY, VOLCENGINE_REGION")
        return []
    return list_virtual_clusters(access_key, secret_key, region, page_size)
