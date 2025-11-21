import logging
from typing import List, Dict, Any

from server.mcp_server_emr.src.mcp_server_emr.api.on_ecs_api import list_clusters
from server.mcp_server_emr.src.mcp_server_emr.api.on_serverless_api import list_serverless_jobs
from server.mcp_server_emr.src.mcp_server_emr.api.on_vke_api import list_virtual_clusters
from server.mcp_server_emr.src.mcp_server_emr.emr_mcp_server import mcp

logger = logging.getLogger(__name__)


@mcp.tool()
def list_serverless_jobs(
        ak: str,
        sk: str,
        region: str,
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
        ak: 火山引擎AccessKey
        sk: 火山引擎SecretKey
        region: 火山引擎Region
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
        jobs = list_serverless_jobs(access_key=ak, secret_key=sk,
                                    region=region, request_body=request_body)

        # 转换为字典格式返回
        result = [job.to_dict() for job in jobs]
        return result

    except Exception as e:
        logger.error(f"查询作业列表时出错: {str(e)}")
        return []


@mcp.tool()
def list_emr_on_ecs_clusters(
        ak: str,
        sk: str,
        region: str,
        page_size: int = 20) -> List[Dict[str, Any]]:
    """
    获取 EMR on ECS 形态的集群列表信息
    Args:
        ak: 火山引擎AccessKey
        sk: 火山引擎SecretKey
        region: 火山引擎Region
        page_size: 每页数量, 默认 20
    """
    return list_clusters(ak, sk, region, page_size)


@mcp.tool()
def list_emr_on_vke_clusters(
        ak: str,
        sk: str,
        region: str,
        page_size: int = 20) -> List[Dict[str, Any]]:
    """
    获取 EMR on VKE 形态的虚拟集群列表信息
    Args:
        ak: 火山引擎AccessKey
        sk: 火山引擎SecretKey
        region: 火山引擎Region
        page_size: 每页数量, 默认 20
    """
    return list_virtual_clusters(ak, sk, region, page_size)
