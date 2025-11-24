import json
import logging

from mcp_server_flink.resources.services import Version20210601, Host, ComponentEnum, LogLevelEnum
from mcp_server_flink.utils.open_api_client import openapi_client_invoke, Credential, RequestParams, OpenAPIContext

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def list_gas_logs_api(
        openapi_context: OpenAPIContext,
        app_id: str,
        project_id: str,
        start_time: int,
        end_time: int,
        level: LogLevelEnum = LogLevelEnum.ALL,
        component: ComponentEnum = ComponentEnum.JOBMANAGER,
        pod_name: str = "",
        cursor: str = "",
        page_size: int = 500,
):
    """
    列出 GWS Application 的 GAS 日志（支持分页和时间范围）。

    :param openapi_context: openapi 上下文
    :param app_id: 作业 Application ID，例如 "s-1983737678904938497"
    :param project_id: 项目 ID，例如 "hjgo1xmh557u"
    :param start_time: 日志查询起始时间戳（毫秒）
    :param end_time: 日志查询结束时间戳（毫秒）
    :param level: 日志级别过滤条件，默认 LogLevelEnum.INFO
    :param component: 组件类型过滤条件，默认 ComponentEnum.JOBMANAGER
    :param pod_name: Pod 名称过滤条件，默认为空字符串表示全部
    :param cursor: 游标用于查询日志，默认为空字符串表示从头开发查询, 游标滚动查询需要 response有带该值。
    :param page_size: 每页返回的日志数量，默认 500
    """

    # === 构造请求体 ===
    body = {
        "Application": app_id,
        "Project": project_id,
        "IndexType": "JOB",
        "PageSize": page_size,
        "Cursor": cursor,
        "StartTime": start_time,
        "EndTime": end_time,
        "Properties": {
            "component": str(component),
            "podName": pod_name,
            "fileName": ""
        }
    }

    if level == LogLevelEnum.ALL:
        body["Level"] = ""
    else:
        body["Level"] = str(level)

    logger.info(f"Invoke ListGasLogs with body: {json.dumps(body, ensure_ascii=False)}")

    # === 构造凭证 ===
    credential = Credential(
        ak=openapi_context.credential.ak,
        sk=openapi_context.credential.sk,
        service=openapi_context.credential.service,
        region=openapi_context.credential.region,
    )

    # === 构造请求参数 ===
    params = RequestParams(
        host=Host,
        body=body,
        query_params=[],
        method="POST",
        headers={
            "Content-Type": "application/json"
        },
        action="ListGASLogs",
        version=Version20210601,
        content_type="application/json"
    )

    # === 发送请求 ===
    try:
        resp = openapi_client_invoke(credential, params)
        logger.info(f"ListGasLogs response: {resp}")
        return resp
    except Exception as e:
        logger.error(f"ListGasLogs failed: {str(e)}", exc_info=True)
        raise
