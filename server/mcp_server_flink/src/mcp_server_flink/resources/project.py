import json
import logging

from mcp_server_flink.resources.services import Version20210601, Host
from mcp_server_flink.utils.open_api_client import openapi_client_invoke, Credential, RequestParams, OpenAPIContext

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def list_gms_project_api(
        openapi_context: OpenAPIContext,
        search_key: str = "",
        page_size: int = 1000,
        page_num: int = 1
):
    """
    列出 GWS 项目 列表（支持分页、排序和条件筛选）

    :param openapi_context: openapi 上下文
    :param search_key: Flink 项目名称搜索关键字, 不传或者为"" 表示查询所有项目列表
    :param page_size: 每页数量，默认 10
    :param page_num: 页码，从 1 开始
    """

    query = [
        ("SearchKey", search_key),
        ("PageSize", page_size),
        ("PageNum", page_num),
    ]

    logger.info(f"Invoke ListGMSProject with body: {json.dumps(query, ensure_ascii=False)}")

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
        action="ListGMSProject",
        version=Version20210601,
        content_type="application/json"
    )

    # === 发送请求 ===
    try:
        resp = openapi_client_invoke(credential, params)
        logger.info(f"ListGMSProject response: {resp}")
        return resp
    except Exception as e:
        logger.error(f"ListGMSProject failed: {str(e)}", exc_info=True)
        raise


def get_gms_project_detail_api(
        openapi_context: OpenAPIContext,
        project_name: str = "",
):
    query = [
        ("ProjectName", project_name),
    ]

    logger.info(f"Invoke GetGMSProjectDetail with body: {json.dumps(query, ensure_ascii=False)}")

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
        action="GetGMSProjectDetail",
        version=Version20210601,
        content_type="application/json"
    )

    # === 发送请求 ===
    try:
        resp = openapi_client_invoke(credential, params)
        logger.info(f"GetGMSProjectDetail response: {resp}")
        return resp
    except Exception as e:
        logger.error(f"GetGMSProjectDetail failed: {str(e)}", exc_info=True)
        raise
