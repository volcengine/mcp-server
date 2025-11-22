import logging
from typing import Optional, List

from volcengine.tls.tls_exception import TLSException
from volcengine.tls.tls_requests import CreateIndexRequest, DeleteIndexRequest, DescribeIndexRequest
from volcengine.tls.tls_responses import CreateIndexResponse, DeleteIndexResponse, DescribeIndexResponse
from volcengine.tls.data import FullTextInfo, KeyValueInfo, ValueInfo

from mcp_server_tls.request import call_sdk_method

logger = logging.getLogger(__name__)

async def create_index_resource(
        auth_info: dict,
        topic_id: str,
        full_text: Optional[dict] = None,
        key_value: Optional[List[dict]] = None,
        user_inner_key_value: Optional[List[dict]] = None,
) -> dict:
    """create_index resource
    """
    try:
        # 转换full_text配置
        full_text_info = None
        if full_text is not None:
            full_text_info = FullTextInfo(
                delimiter=full_text.get("delimiter"),
                case_sensitive=full_text.get("case_sensitive", False),
                include_chinese=full_text.get("include_chinese", False)
            )
        
        # 转换key_value配置
        key_value_infos = None
        if key_value is not None:
            key_value_infos = []
            for kv_dict in key_value:
                value_info = ValueInfo(
                    value_type=kv_dict.get("value_type", "text"),
                    delimiter=kv_dict.get("delimiter"),
                    case_sensitive=kv_dict.get("case_sensitive", False),
                    include_chinese=kv_dict.get("include_chinese", False),
                    sql_flag=kv_dict.get("sql_flag", False),
                    index_all=kv_dict.get("index_all", False)
                )
                key_value_infos.append(KeyValueInfo(
                    key=kv_dict.get("key"),
                    value=value_info
                ))
        
        # 转换user_inner_key_value配置
        user_inner_key_value_infos = None
        if user_inner_key_value is not None:
            user_inner_key_value_infos = []
            for kv_dict in user_inner_key_value:
                value_info = ValueInfo(
                    value_type=kv_dict.get("value_type", "text"),
                    delimiter=kv_dict.get("delimiter"),
                    case_sensitive=kv_dict.get("case_sensitive", False),
                    include_chinese=kv_dict.get("include_chinese", False),
                    sql_flag=kv_dict.get("sql_flag", False),
                    index_all=kv_dict.get("index_all", False)
                )
                user_inner_key_value_infos.append(KeyValueInfo(
                    key=kv_dict.get("key"),
                    value=value_info
                ))
        
        request: CreateIndexRequest = CreateIndexRequest(
            topic_id=topic_id,
            full_text=full_text_info,
            key_value=key_value_infos,
            user_inner_key_value=user_inner_key_value_infos
        )

        response: CreateIndexResponse = await call_sdk_method(
            auth_info=auth_info,
            method_name="create_index",
            create_index_request=request,
        )

        return {"request_id": response.get_request_id()}

    except TLSException as e:
        logger.error("create_index_resource error")
        raise e

async def delete_index_resource(
        auth_info: dict,
        topic_id: str,
) -> dict:
    """delete_index resource
    """
    try:
        request: DeleteIndexRequest = DeleteIndexRequest(
            topic_id=topic_id,
        )

        response: DeleteIndexResponse = await call_sdk_method(
            auth_info=auth_info,
            method_name="delete_index",
            delete_index_request=request,
        )

        return {"request_id": response.get_request_id()}

    except TLSException as e:
        logger.error("delete_index_resource error")
        raise e

async def describe_index_resource(
        auth_info: dict,
        topic_id: str,
) -> dict:
    """describe_index resource
    """
    try:
        request: DescribeIndexRequest = DescribeIndexRequest(
            topic_id=topic_id,
        )

        response: DescribeIndexResponse = await call_sdk_method(
            auth_info=auth_info,
            method_name="describe_index",
            describe_index_request=request,
        )

        return {
            "topic_id": topic_id,
            "full_text": vars(response.get_full_text()) if response.get_full_text() else None,
            "key_value": [kv.json() for kv in response.get_key_value()] if response.get_key_value() else None,
            "user_inner_key_value": [kv.json for kv in response.get_user_inner_key_value()] if response.get_user_inner_key_value() else None,
            "create_time": response.get_create_time(),
            "modify_time": response.get_modify_time()
        }

    except TLSException as e:
        logger.error("describe_index_resource error")
        raise e