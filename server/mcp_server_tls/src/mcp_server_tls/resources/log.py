import logging

from typing import Optional
from volcengine.tls.const import LZ4
from volcengine.tls.tls_exception import TLSException
from volcengine.tls.tls_requests import SearchLogsRequest, PutLogsV2Request, PutLogsV2Logs
from volcengine.tls.tls_responses import SearchLogsResponse, PutLogsResponse
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
