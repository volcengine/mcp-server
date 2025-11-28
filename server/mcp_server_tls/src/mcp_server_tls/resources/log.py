import logging

from typing import Optional
from volcengine.tls.const import LZ4
from volcengine.tls.tls_exception import TLSException
from volcengine.tls.tls_requests import SearchLogsRequest, PutLogsV2Request, PutLogsV2Logs, ConsumeLogsRequest, DescribeCursorRequest, DescribeLogContextRequest
from volcengine.tls.tls_responses import SearchLogsResponse, PutLogsResponse, ConsumeLogsResponse, DescribeCursorResponse, DescribeLogContextResponse
from mcp_server_tls.request import call_sdk_method

logger = logging.getLogger(__name__)

async def search_logs_v2_resource(
        auth_info: dict,
        topic_id: str,
        query: str,
        start_time: int,
        end_time: int,
        limit: int,
        context: Optional[str] = None,
        sort: Optional[str] = "DESC",
) -> dict:
    try:
        request: SearchLogsRequest = SearchLogsRequest(
            topic_id=topic_id,
            query=query,
            start_time=start_time,
            end_time=end_time,
            limit=limit,
            context=context,
            sort=sort,
        )

        response: SearchLogsResponse = await call_sdk_method(
            auth_info=auth_info,
            method_name="search_logs_v2",
            search_logs_request=request,
        )

        search_result = response.get_search_result()
        search_result.analysis_result = vars(search_result.analysis_result)
        result =  vars(search_result)
        # Remove useless fields
        result.pop("HitCount", None)
        return result

    except TLSException as e:
        logger.error("search_logs_v2_resource error")
        raise e

async def put_logs_v2_resource(
        auth_info: dict,
        topic_id: str,
        logs: list[dict],
        log_time: int = 0,
        source: Optional[str] = None,
        filename: Optional[str] = None,
        hash_key: Optional[str] = None,
        compression: str = LZ4,
) -> dict:
    try:
        logs_ins = PutLogsV2Logs(source=source, filename=filename)
        for log_dict in logs:
            logs_ins.add_log(contents=log_dict, log_time=log_time)

        request: PutLogsV2Request = PutLogsV2Request(
            topic_id=topic_id,
            logs=logs_ins,
            hash_key=hash_key,
            compression=compression,
        )

        response: PutLogsResponse = await call_sdk_method(
            auth_info=auth_info,
            method_name="put_logs_v2",
            request=request,
        )

        return {
            "request_id": response.get_request_id()
        }

    except TLSException as e:
        logger.error("put_logs_v2_resource error")
        raise e

async def consume_logs_resource(
        auth_info: dict,
        topic_id: str,
        shard_id: int,
        cursor: str,
        end_cursor: Optional[str] = None,
        log_group_count: Optional[int] = None,
        compression: Optional[str] = None,
        consumer_group_name: Optional[str] = None,
        consumer_name: Optional[str] = None,
) -> dict:
    """consume_logs resource
    """
    try:
        request: ConsumeLogsRequest = ConsumeLogsRequest(
            topic_id=topic_id,
            shard_id=shard_id,
            cursor=cursor,
            end_cursor=end_cursor,
            log_group_count=log_group_count,
            compression=compression,
            consumer_group_name=consumer_group_name,
            consumer_name=consumer_name,
        )

        response: ConsumeLogsResponse = await call_sdk_method(
            auth_info=auth_info,
            method_name="consume_logs",
            consume_logs_request=request,
        )

        return {
            "x_tls_count": response.get_x_tls_count(),
            "x_tls_cursor": response.get_x_tls_cursor(),
            "pb_message": response.get_pb_message()
        }

    except TLSException as e:
        logger.error("consume_logs_resource error")
        raise e

async def describe_cursor_resource(
        auth_info: dict,
        topic_id: str,
        shard_id: int,
        from_time: str,
) -> dict:
    """describe_cursor resource
    """
    try:
        request: DescribeCursorRequest = DescribeCursorRequest(
            topic_id=topic_id,
            shard_id=shard_id,
            from_time=from_time,
        )

        response: DescribeCursorResponse = await call_sdk_method(
            auth_info=auth_info,
            method_name="describe_cursor",
            describe_cursor_request=request,
        )

        return {
            "cursor": response.get_cursor()
        }

    except TLSException as e:
        logger.error("describe_cursor_resource error")
        raise e

async def describe_log_context_resource(
        auth_info: dict,
        topic_id: str,
        context_flow: str,
        package_offset: int,
        source: str,
        prev_logs: int = 10,
        next_logs: int = 10,
) -> dict:
    """describe_log_context resource
    """
    try:
        request: DescribeLogContextRequest = DescribeLogContextRequest(
            topic_id=topic_id,
            context_flow=context_flow,
            package_offset=package_offset,
            source=source,
            prev_logs=prev_logs,
            next_logs=next_logs,
        )

        response: DescribeLogContextResponse = await call_sdk_method(
            auth_info=auth_info,
            method_name="describe_log_context",
            describe_log_context_request=request,
        )

        return {
            "prev_over": response.get_prev_over(),
            "next_over": response.get_next_over(),
            "log_context_infos": response.get_log_context_infos(),
        }

    except TLSException as e:
        logger.error("describe_log_context_resource error")
        raise e
