import json
import logging

from mcp_server_flink.resources.services import Version20210601, Host, JobTypeEnum, StartTypeEnum, JobStateEnum
from mcp_server_flink.utils.open_api_client import openapi_client_invoke, Credential, RequestParams, OpenAPIContext

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def list_gws_application_api(
        openapi_context: OpenAPIContext,
        project_id: str = "",
        job_name: str = "",
        resource_pool="",
        job_state: JobStateEnum = JobStateEnum.ALL,
        job_type: JobTypeEnum = JobTypeEnum.FLINK_JOB_TYPE_ALL,
        page_size: int = 1000,
        page_num: int = 1,
        sort_field: str = "DeployTime",
        sort_order: str = "desc",
):
    """
    列出 GWS Application 列表（支持分页、排序和条件筛选）

    :param openapi_context: openapi 上下文
    :param project_id: Flink 项目 ID, 不传或者为"" 表示查询所有Application列表
    :param job_name: 作业名称，可选
    :param resource_pool: 资源池名称，可选
    :param job_type: 作业类型，可选
    :param page_size: 每页数量，默认 10
    :param page_num: 页码，从 1 开始
    :param sort_field: 排序字段，默认 DeployTime
    :param sort_order: 排序方式，asc / desc，默认 desc
    """

    query = [
        ("PageSize", page_size),
        ("PageNum", page_num),
        ("SortField", sort_field),
        ("SortOrder", sort_order),
    ]

    body = {
        "ProjectId": project_id,
        "JobName": job_name,
        "ResourcePool": resource_pool,
        "JobType": str(job_type),
    }

    if job_type == JobTypeEnum.FLINK_JOB_TYPE_ALL:
        body["JobType"] = ""
    else:
        body["JobType"] = str(job_type)

    if job_state != JobStateEnum.ALL:
        body["State"] = str(job_state)

    logger.info(f"Invoke ListGWSApplication with body: {json.dumps(query, ensure_ascii=False)}")

    # === 构造凭证 ===
    credential = Credential(
        ak=openapi_context.credential.ak,
        sk=openapi_context.credential.sk,
        service=openapi_context.credential.service,
        region=openapi_context.credential.region,
    )

    params = RequestParams(
        host=Host,
        body=body,
        query_params=query,
        method="POST",
        headers={
            "Content-Type": "application/json"
        },
        action="ListGWSApplication",
        version=Version20210601,
        content_type="application/json"
    )

    # === 发送请求 ===
    try:
        resp = openapi_client_invoke(credential, params)
        logger.info(f"ListGWSApplication response: {resp}")
        return resp
    except Exception as e:
        logger.error(f"ListGWSApplication failed: {str(e)}", exc_info=True)
        raise


def get_gws_application_api(
        openapi_context: OpenAPIContext,
        id: str,
        account_id: str = "",
):
    """
    列出 GWS Application 列表（支持分页、排序和条件筛选）

    :param openapi_context: openapi 上下文
    :param id: Flink 作业 ID
    :param account_id: Flink 用户ID，可选，不传或者为"" 表示查询指定ID的作业
    """

    body = {
        "Id": id,
        "AccountId": account_id,
    }

    logger.info(f"Invoke ListGWSApplication with body: {json.dumps(body, ensure_ascii=False)}")

    # === 构造凭证 ===
    credential = Credential(
        ak=openapi_context.credential.ak,
        sk=openapi_context.credential.sk,
        service=openapi_context.credential.service,
        region=openapi_context.credential.region,
    )

    params = RequestParams(
        host=Host,
        body=body,
        query_params=[],
        method="POST",
        headers={
            "Content-Type": "application/json"
        },
        action="GetGWSApplication",
        version=Version20210601,
        content_type="application/json"
    )

    # === 发送请求 ===
    try:
        resp = openapi_client_invoke(credential, params)
        logger.info(f"GetGWSApplication response: {resp}")
        return resp
    except Exception as e:
        logger.error(f"GetGWSApplication failed: {str(e)}", exc_info=True)
        raise


def get_grs_app_by_id_api(
        openapi_context: OpenAPIContext,
        app_id: str,
):
    """
    根据作业ID获取对应的作业运行时信息。

    :param openapi_context: openapi 上下文
    :param app_id: GRS应用的唯一标识ID。
    :return: 指定GRS应用的详细信息。
    """
    query = [
        ("AppIdKey", app_id),
    ]

    logger.info(f"Invoke GetGRSAppById with body: {json.dumps(query, ensure_ascii=False)}")

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
        action="GetGRSAppById",
        version=Version20210601,
        content_type="application/json"
    )

    # === 发送请求 ===
    try:
        resp = openapi_client_invoke(credential, params)
        logger.info(f"GetGRSAppById response: {resp}")
        return resp
    except Exception as e:
        logger.error(f"GetGRSAppById failed: {str(e)}", exc_info=True)
        raise


def start_gws_application_api(
        openapi_context: OpenAPIContext,
        project_id: str,
        id: str,
        start_type: StartTypeEnum = StartTypeEnum.FROM_NEW,
):
    """
    启动 GWS 作业

    :param openapi_context: openapi 上下文
    :param project_id: Flink 项目 ID，例如 "mqp9r338gmbv"
    :param id: 作业唯一ID
    :param conf: 作业动态参数（字典形式），例如 {"key1": "v1", "key2": "v2"}
    :param start_type: 启动类型，可选：
        - FROM_NEW（默认，全新启动）
        - FROM_LATEST（从最新状态启动）
    """

    # === 构造 query 参数 ===
    query = [
        ("ProjectId", project_id),
    ]

    # === 构造请求体 ===
    body = {
        "Id": id,
        "Type": str(start_type),
    }

    logger.info(
        f"Invoke StartGWSApplication with query={json.dumps(query, ensure_ascii=False)}, body={json.dumps(body, ensure_ascii=False)}")

    # === 构造凭证 ===
    credential = Credential(
        ak=openapi_context.credential.ak,
        sk=openapi_context.credential.sk,
        service=openapi_context.credential.service,
        region=openapi_context.credential.region,
    )

    # === 组织请求参数 ===
    params = RequestParams(
        host=Host,
        body=body,
        query_params=query,
        method="POST",
        headers={
            "Content-Type": "application/json"
        },
        action="StartGWSApplication",
        version=Version20210601,
        content_type="application/json"
    )

    # === 发送请求 ===
    try:
        resp = openapi_client_invoke(credential, params)
        logger.info(f"StartGWSApplication response: {resp}")
        return resp
    except Exception as e:
        logger.error(f"StartGWSApplication failed: {str(e)}", exc_info=True)
        raise


def stop_gws_application_api(
        openapi_context: OpenAPIContext,
        project_id: str,
        id: str,
):
    """
    停止 GWS 作业

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
    }

    logger.info(
        f"Invoke CancelGWSApplication with query={json.dumps(query, ensure_ascii=False)}, body={json.dumps(body, ensure_ascii=False)}")

    # === 构造凭证 ===
    credential = Credential(
        ak=openapi_context.credential.ak,
        sk=openapi_context.credential.sk,
        service=openapi_context.credential.service,
        region=openapi_context.credential.region,
    )

    # === 组织请求参数 ===
    params = RequestParams(
        host=Host,
        body=body,
        query_params=query,
        method="POST",
        headers={
            "Content-Type": "application/json"
        },
        action="CancelGWSApplication",
        version=Version20210601,
        content_type="application/json"
    )

    # === 发送请求 ===
    try:
        resp = openapi_client_invoke(credential, params)
        logger.info(f"CancelGWSApplication response: {resp}")
        return resp
    except Exception as e:
        logger.error(f"CancelGWSApplication failed: {str(e)}", exc_info=True)
        raise


def restart_gws_application_api(
        openapi_context: OpenAPIContext,
        project_id: str,
        id: str,
        start_type: StartTypeEnum = StartTypeEnum.FROM_NEW,
):
    """
    重启 GWS 作业

    :param openapi_context: openapi 上下文
    :param project_id: Flink 项目 ID，例如 "mqp9r338gmbv"
    :param id: 作业唯一ID
    :param conf: 作业动态参数（字典形式），例如 {"key1": "v1", "key2": "v2"}
    :param start_type: 启动类型，可选：
        - FROM_NEW（默认，全新启动）
        - FROM_LATEST（从最新状态启动）
    """

    # === 构造 query 参数 ===
    query = [
        ("ProjectId", project_id),
    ]

    # === 构造请求体 ===
    body = {
        "Id": id,
        "Type": str(start_type),
    }

    logger.info(
        f"Invoke RestartGWSApplication with query={json.dumps(query, ensure_ascii=False)}, body={json.dumps(body, ensure_ascii=False)}")

    # === 构造凭证 ===
    credential = Credential(
        ak=openapi_context.credential.ak,
        sk=openapi_context.credential.sk,
        service=openapi_context.credential.service,
        region=openapi_context.credential.region,
    )

    # === 组织请求参数 ===
    params = RequestParams(
        host=Host,
        body=body,
        query_params=query,
        method="POST",
        headers={
            "Content-Type": "application/json"
        },
        action="RestartGWSApplication",
        version=Version20210601,
        content_type="application/json"
    )

    # === 发送请求 ===
    try:
        resp = openapi_client_invoke(credential, params)
        logger.info(f"RestartGWSApplication response: {resp}")
        return resp
    except Exception as e:
        logger.error(f"RestartGWSApplication failed: {str(e)}", exc_info=True)
        raise
