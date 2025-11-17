import json
import logging

from mcp_server_flink.resources.services import Host, Version20220601
from mcp_server_flink.utils.open_api_client import openapi_client_invoke, Credential, RequestParams, OpenAPIContext

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def list_gmcs_resource_pool_api(
        openapi_context: OpenAPIContext,
        project_id: str,
        name: str = "",
        name_key: str = "",
        page_size: int = 1000,
        page_num: int = 1,
):
    """
    列出 GWS 资源池 列表（支持分页、排序和条件筛选）

    :param openapi_context: openapi 上下文
    :param project_id: Flink 项目 ID, 不传或者为"" 表示查询所有资源池列表
    :param name: Flink 资源池名称, 不传或者为"" 表示查询所有资源池列表
    :param name_key: Flink 资源池名称（模糊查询）, 不传或者为"" 表示查询所有资源池列表
    :param page_size: 每页数量，默认 10
    :param page_num: 页码，从 1 开始
    """

    query = [
        ("ProjectId", project_id),
        ("Name", name),
        ("NameKey", name_key),
        ("PageSize", page_size),
        ("PageNum", page_num),
    ]

    logger.info(f"Invoke ListGMCSResourcePool with body: {json.dumps(query, ensure_ascii=False)}")

    # === 构造凭证 ===
    credential = Credential(
        ak=openapi_context.credential.ak,
        sk=openapi_context.credential.sk,
        service=openapi_context.credential.service,
        region=openapi_context.credential.region,
    )

    params = RequestParams(
        host=Host,
        body={},
        query_params=query,
        method="GET",
        headers={
            "Content-Type": "application/json"
        },
        action="ListGMCSResourcePool",
        version=Version20220601,
        content_type="application/json"
    )

    # === 发送请求 ===
    try:
        resp = openapi_client_invoke(credential, params)
        logger.info(f"ListGMCSResourcePool response: {resp}")
        return resp
    except Exception as e:
        logger.error(f"ListGMCSResourcePool failed: {str(e)}", exc_info=True)
        raise
