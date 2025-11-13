import logging
from typing import Optional, List

from volcengine.tls.tls_exception import TLSException
from volcengine.tls.tls_requests import DescribeTopicRequest, DescribeTopicsRequest, CreateTopicRequest, DeleteTopicRequest
from volcengine.tls.tls_responses import DescribeTopicResponse, DescribeTopicsResponse, CreateTopicResponse, DeleteTopicResponse
from volcengine.tls.data import TagInfo

from mcp_server_tls.request import call_sdk_method

logger = logging.getLogger(__name__)

async def describe_topic_resource(
        auth_info: dict,
        topic_id: str,
) -> dict:
    try:
        request: DescribeTopicRequest = DescribeTopicRequest(
            topic_id=topic_id,
        )

        response: DescribeTopicResponse = await call_sdk_method(
            auth_info=auth_info,
            method_name="describe_topic",
            describe_topic_request=request,
        )

        return vars(response.get_topic())

    except TLSException as e:
        logger.error(f"Describe topic error: {e}")
        raise e

async def describe_topics_resource(
        auth_info: dict,
        page_number: Optional[int] = 1,
        page_size: Optional[int] = 10,
        project_name: Optional[str] = None,
        project_id: Optional[str] = None,
        topic_name: Optional[str] = None,
        topic_id: Optional[str] = None,
) -> dict:
    try:
        request: DescribeTopicsRequest = DescribeTopicsRequest(
            page_number=page_number,
            page_size=page_size,
            project_name=project_name,
            project_id=project_id,
            topic_name=topic_name,
            topic_id=topic_id,
        )

        response: DescribeTopicsResponse = await call_sdk_method(
            auth_info=auth_info,
            method_name="describe_topics",
            describe_topics_request=request,
        )

        return {
            "total": response.get_total(),
            "topics": [vars(topic_info) for topic_info in response.get_topics()]
        }

    except TLSException as e:
        logger.error(f"Describe topics error: {e}")
        raise e

async def create_topic_resource(
        auth_info: dict,
        topic_name: str,
        project_id: str,
        ttl: int,
        shard_count: int,
        description: Optional[str] = None,
        auto_split: bool = True,
        max_split_shard: int = 50,
        enable_tracking: bool = False,
        time_key: Optional[str] = None,
        time_format: Optional[str] = None,
        tags: Optional[List] = None,
        log_public_ip: bool = True,
        enable_hot_ttl: bool = False,
        hot_ttl: Optional[int] = None,
        cold_ttl: Optional[int] = None,
        archive_ttl: Optional[int] = None,
) -> dict:
    """create_topic resource
    """
    try:
        # 转换tags格式：将字典列表转换为TagInfo对象列表
        tag_objects = None
        if tags is not None:
            tag_objects = []
            for tag_dict in tags:
                tag_objects.append(TagInfo(key=tag_dict.get("key"), value=tag_dict.get("value")))
        
        request: CreateTopicRequest = CreateTopicRequest(
            topic_name=topic_name,
            project_id=project_id,
            ttl=ttl,
            shard_count=shard_count,
            description=description,
            auto_split=auto_split,
            max_split_shard=max_split_shard,
            enable_tracking=enable_tracking,
            time_key=time_key,
            time_format=time_format,
            tags=tag_objects,
            log_public_ip=log_public_ip,
            enable_hot_ttl=enable_hot_ttl,
            hot_ttl=hot_ttl,
            cold_ttl=cold_ttl,
            archive_ttl=archive_ttl,
        )

        response: CreateTopicResponse = await call_sdk_method(
            auth_info=auth_info,
            method_name="create_topic",
            create_topic_request=request,
        )

        return {"topic_id": response.get_topic_id()}

    except TLSException as e:
        logger.error("create_topic_resource error")
        raise e

async def delete_topic_resource(
        auth_info: dict,
        topic_id: str,
) -> dict:
    """delete_topic resource
    """
    try:
        request: DeleteTopicRequest = DeleteTopicRequest(
            topic_id=topic_id,
        )

        response: DeleteTopicResponse = await call_sdk_method(
            auth_info=auth_info,
            method_name="delete_topic",
            delete_topic_request=request,
        )

        return {"request_id": response.get_request_id()}

    except TLSException as e:
        logger.error("delete_topic_resource error")
        raise e