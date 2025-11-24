# 导入工具模块，确保工具被注册
import logging
import os
from typing import List, Dict, Any

from mcp.server.fastmcp import FastMCP

from server.mcp_server_emr.src.mcp_server_emr.api.on_ecs_api import list_clusters
from server.mcp_server_emr.src.mcp_server_emr.api.on_serverless_api import list_serverless_jobs
from server.mcp_server_emr.src.mcp_server_emr.api.on_vke_api import list_virtual_clusters

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
def list_serverless_jobs(
        job_id: str = "",
        job_name: str = "",
        start_time: str = "",
        finish_time: str = "",
        queue: str = "",
        limit: int = 20,
        offset: int = 1,
) -> List[Dict[str, Any]]:
    """
    获取EMR Serverless作业列表

    Args:
        job_id: 作业ID筛选
        job_name: 作业名称筛选
        start_time: 开始时间 "yyyy-MM-dd"
        finish_time: 结束时间 "yyyy-MM-dd"
        queue: 队列名称筛选
        limit: 每页数量，默认20
        offset: 页码，从1开始

    Returns:
        作业列表
    """
    try:
        # 过滤作业数据
        request_body = {
            "JobId": job_id,
            "JobName": job_name,
            "StartTime": start_time,
            "FinishTime": finish_time,
            "QueueName": queue,
            "Limit": limit,
            "Offset": offset,
        }
        access_key = os.environ.get("VOLCENGINE_ACCESS_KEY")
        secret_key = os.environ.get("VOLCENGINE_SECRET_KEY")
        region = os.environ.get("VOLCENGINE_REGION")
        if not all([access_key, secret_key, region]):
            logger.error("缺少必要的环境变量: VOLCENGINE_ACCESS_KEY, VOLCENGINE_SECRET_KEY, VOLCENGINE_REGION")
            return []

        jobs = list_serverless_jobs(access_key=access_key, secret_key=secret_key,
                                    region=region, request_body=request_body)

        # 转换为字典格式返回
        result = [job.to_dict() for job in jobs]
        return result

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
