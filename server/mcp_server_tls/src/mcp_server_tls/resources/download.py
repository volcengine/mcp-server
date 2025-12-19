import logging
from typing import Optional, Dict, Any, List
from volcengine.tls.TLSService import TLSService
from volcengine.tls.tls_exception import TLSException
from volcengine.tls.tls_requests import CreateDownloadTaskRequest, DescribeDownloadTasksRequest, DescribeDownloadUrlRequest
from volcengine.tls.tls_responses import CreateDownloadTaskResponse, DescribeDownloadTasksResponse, DescribeDownloadUrlResponse

from mcp_server_tls.request import call_sdk_method

logger = logging.getLogger(__name__)


async def create_download_task_resource(
    auth_info: Dict,
    query: str,
    task_name: str,
    start_time: int,
    end_time: int,
    topic_id: str,
    format_type: str,
    sort: str,
    limit: int,
    compression: Optional[str] = None,
) -> Dict:
    """
    Create a download task for log data export

    """
    try:
        if compression is None:
            compression = "gzip"
            
        request = CreateDownloadTaskRequest(
            task_name=task_name,
            topic_id=topic_id,
            query=query,
            start_time=start_time,
            end_time=end_time,
            data_format=format_type,
            sort=sort,
            limit=limit,
            compression=compression
        )
            
        response: CreateDownloadTaskResponse = await call_sdk_method(
            auth_info=auth_info,
            method_name="create_download_task",
            create_download_task_request=request,
        )

        return {
            "task_id": response.get_task_id(),
        }
            
    except TLSException as e:
        logger.error("create_download_task_resource error: {}".format(str(e)))
        raise e


async def describe_download_tasks_resource(
    auth_info: Dict,
    topic_id: str,
    page_number: Optional[int] = 1,
    page_size: Optional[int] = 20,
    task_name: Optional[str] = None,
) -> Dict:
    """
    Query download task list
    """
    try:
        request = DescribeDownloadTasksRequest(
            topic_id=topic_id,
            page_number=page_number,
            page_size=page_size,
            task_name=task_name
        )

        response: DescribeDownloadTasksResponse = await call_sdk_method(
            auth_info=auth_info,
            method_name="describe_download_tasks",
            describe_download_tasks_request=request,
        )

        return {
            "total": response.get_total(),
            "tasks": [vars(task_info) for task_info in response.get_tasks()]
        }
            
    except TLSException as e:
        logger.error("describe_download_tasks_resource error: {}".format(str(e)))
        raise e


async def describe_download_url_resource(
    auth_info: Dict,
    task_id: str,
) -> Dict:
    """
    Get download URL for a task
    
    This function gets the download URL for a specified download task.
    The URL is typically valid for a limited time period.
    """
    try:
        request = DescribeDownloadUrlRequest(
            task_id=task_id
        )
            
        response: DescribeDownloadUrlResponse = await call_sdk_method(
            auth_info=auth_info,
            method_name="describe_download_url",
            describe_download_url_request=request,
        )
        
        return {
                "download_url": response.get_download_url(),
        }
            
    except TLSException as e:
        logger.error("describe_download_url_resource error: {}".format(str(e)))
        raise e