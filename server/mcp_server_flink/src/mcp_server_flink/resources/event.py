import json
import logging

from mcp_server_flink.resources.services import Host, Version20210601
from mcp_server_flink.utils.open_api_client import OpenAPIContext, RequestParams, openapi_client_invoke, Credential

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def get_gws_event_list_api(
        openapi_context: OpenAPIContext,
        project_id: str,
        id: str = "",
        limit: int = 50,
):
    """
    查询 Flink Application 的 Event 运行事件信息。

    :param openapi_context: openapi 上下文
    :param project_id: Flink 项目 ID，例如 "mqp9r338gmbv"
    :param id: 作业唯一ID
    """

    # === 构造 query 参数 ===
    query = [
        ("ProjectId", project_id),
    ]

    # === 构造请求体 ===
    body = {
        "Id": id,
        "Limit": limit,
    }

    logger.info(f"Invoke GWSGetEventList with body: {json.dumps(body, ensure_ascii=False)}")

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
        query_params=query,
        method="POST",
        headers={
            "Content-Type": "application/json"
        },
        action="GWSGetEventList",
        version=Version20210601,
        content_type="application/json"
    )

    # === 发送请求 ===
    try:
        resp = openapi_client_invoke(credential, params)
        logger.info(f"GWSGetEventList response: {resp}")
        return resp
    except Exception as e:
        logger.error(f"GWSGetEventList failed: {str(e)}", exc_info=True)
        raise
