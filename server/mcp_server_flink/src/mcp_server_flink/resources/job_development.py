import json
import logging
from datetime import datetime
from typing import Dict, Optional

from mcp_server_flink.resources.services import Version20210601, Host, JobTypeEnum, EngineVersionEnum, PriorityEnum, \
    SchedulePolicyEnum
from mcp_server_flink.utils.open_api_client import openapi_client_invoke, Credential, RequestParams, OpenAPIContext

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

DEFAULT_DYNAMIC_OPTIONS = {
    "execution.checkpointing.interval": "300s",
    "execution.checkpointing.timeout": "600s",
    "jobmanager.memory.process.size": "4096mb",
    "kubernetes.jobmanager.cpu": "1",
    "kubernetes.taskmanager.cpu": "1",
    "parallelism.default": "2",
    "restart.attempt.enable": "true",
    "restart.attempt.interval.min": "1",
    "restart.attempt.max.count": "3",
    "state.backend.cache.enable": "false",
    "state.backend.cache.maxHeapSize": "1024mb",
    "state.checkpoints.region.enabled": "false",
    "taskmanager.memory.process.size": "4096mb",
    "taskmanager.numberOfTaskSlots": "2"
}


def list_gws_directory_api(
        openapi_context: OpenAPIContext,
        project_id: str,
        type: str = "JOB",
):
    """
    列出 GWS 文件夹 列表

    :param openapi_context: openapi 上下文
    :param project_id: Flink 项目 ID, 不传或者为"" 表示查询所有Application列表
    :param type: JOB:作业相关目录, QUERY：SQL查询相关目录
    """

    query = [
        ("ProjectId", project_id),
        ("Type", type)
    ]

    logger.info(f"Invoke ListGWSDirectory with body: {json.dumps(query, ensure_ascii=False)}")

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
        method="POST",
        headers={
            "Content-Type": "application/json"
        },
        action="ListGWSDirectory",
        version=Version20210601,
        content_type="application/json"
    )

    # === 发送请求 ===
    try:
        resp = openapi_client_invoke(credential, params)
        logger.info(f"ListGWSDirectory response: {resp}")
        return resp
    except Exception as e:
        logger.error(f"ListGWSDirectory failed: {str(e)}", exc_info=True)
        raise


def get_gws_application_draft_api(
        openapi_context: OpenAPIContext,
        project_id: str,
        id: str,
):
    """
    获取 GWS 作业草稿

    :param project_id: Flink 项目 ID, 不传或者为"" 表示查询所有Application列表
    :param id: 作业草稿 ID，例如 "1855862619368951810"
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
        f"Invoke GetGWSApplicationDraft with query={json.dumps(query, ensure_ascii=False)}, body={json.dumps(body, ensure_ascii=False)}")

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
        action="GetGWSApplicationDraft",
        version=Version20210601,
        content_type="application/json"
    )

    # === 发送请求 ===
    try:
        resp = openapi_client_invoke(credential, params)
        logger.info(f"GetGWSApplicationDraft response: {resp}")
        return resp
    except Exception as e:
        logger.error(f"GetGWSApplicationDraft failed: {str(e)}", exc_info=True)
        raise


def create_gws_application_draft_api(
        openapi_context: OpenAPIContext,
        job_name: str,
        project_id: str,
        directory_id: str,
        job_type: JobTypeEnum = JobTypeEnum.FLINK_STREAMING_SQL,
        engine_version: EngineVersionEnum = EngineVersionEnum.FLINK_VERSION_1_17,
):
    """
    创建 GWS Application 草稿

    :param openapi_context: openapi 上下文
    :param job_name: 作业名称
    :param job_type: 作业类型，可选：
                     - FLINK_STREAMING_SQL
                     - FLINK_BATCH_SQL
    :param engine_version: 运行引擎版本，可选：
                           - FLINK_VERSION_1_11
                           - FLINK_VERSION_1_16
                           - FLINK_VERSION_1_17
    :param project_id: Flink 项目 ID
    :param directory_id: 文件夹 ID
    """

    # === 组装请求体 ===
    body = {
        "JobName": job_name,
        "EngineVersion": str(engine_version),
        "ProjectId": project_id,
        "DirectoryId": directory_id,
    }

    if job_type == JobTypeEnum.FLINK_JOB_TYPE_ALL:
        body["JobType"] = ""
    else:
        body["JobType"] = str(job_type)

    logger.info(f"Invoke CreateGWSApplicationDraft with body: {json.dumps(body, ensure_ascii=False)}")

    query = [
        ("ProjectId", project_id),
    ]

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
        action="CreateGWSApplicationDraft",
        version=Version20210601,
        content_type="application/json"
    )

    # === 发送请求 ===
    try:
        resp = openapi_client_invoke(credential, params)
        logger.info(f"CreateGWSApplicationDraft response: {resp}")
        return resp
    except Exception as e:
        logger.error(f"CreateGWSApplicationDraft failed: {str(e)}", exc_info=True)
        raise


def update_gws_application_draft_api(
        openapi_context: OpenAPIContext,
        id: str,
        project_id: str,
        account_id: str,
        user_id: str,
        job_name: str,
        job_id: str,
        directory_id: str,
        directory_name: str,
        sql_text: str,
        dynamic_options: Dict[str, str] = None,
        job_type: JobTypeEnum = JobTypeEnum.FLINK_STREAMING_SQL,
        engine_version: EngineVersionEnum = EngineVersionEnum.FLINK_VERSION_1_17,
):
    """
    更新 GWS 作业草稿 (UpdateGWSApplicationDraft)

    :param openapi_context: openapi 上下文
    :param id: draft id
    :param job_type: 作业类型
    :param project_id: 项目 ID
    :param account_id: 租户 ID
    :param user_id: Flink 用户 ID
    :param job_name: 作业名
    :param job_id: 内部 ID，废弃字段，不推荐使用
    :param dynamic_options: 作业动态参数
    :param engine_version: Flink 引擎版本
    :param directory_id: 草稿作业所属文件夹 ID
    :param directory_name: 文件夹名
    :param sql_text: SQL 文本
    """

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    query = [
        ("ProjectId", project_id),
    ]

    body = {
        "Id": id,
        "ProjectId": project_id,
        "AccountId": account_id,
        "UserId": user_id,
        "Platform": "StreamX",
        "JobName": job_name,
        "JobId": job_id,
        "State": "CREATED",
        "Options": "{}",
        "CreateTime": current_time,
        "ModifiedTime": current_time,
        "K8sNamespace": "",
        "EngineVersion": engine_version,
        "DirectoryId": directory_id,
        "DirectoryName": directory_name,
        "SqlText": sql_text,
        "Dependency": "{}",
        "Sources": [],
        "Sinks": [],
        "DataConnectionGroups": [],
        "EnableDeepValidate": False,
    }

    if job_type == JobTypeEnum.FLINK_JOB_TYPE_ALL:
        body["JobType"] = ""
    else:
        body["JobType"] = str(job_type)

    if dynamic_options is None:
        body["DynamicOptions"] = json.dumps(DEFAULT_DYNAMIC_OPTIONS)
    else:
        body["DynamicOptions"] = json.dumps(dynamic_options)

    logger.info(f"Invoke UpdateGWSApplicationDraft with body: {json.dumps(body, ensure_ascii=False)}")

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
        action="UpdateGWSApplicationDraft",
        version=Version20210601,
        content_type="application/json"
    )

    # === 发送请求 ===
    try:
        resp = openapi_client_invoke(credential, params)
        logger.info(f"UpdateGWSApplicationDraft response: {resp}")
        return resp
    except Exception as e:
        logger.error(f"UpdateGWSApplicationDraft failed: {str(e)}", exc_info=True)
        raise


def deploy_gws_application_draft_api(
        openapi_context: OpenAPIContext,
        project_id: str,
        id: str,
        resource_pool: str,
        queue: str,
        priority: PriorityEnum = PriorityEnum.LEVEL_3,
        schedule_policy: SchedulePolicyEnum = SchedulePolicyEnum.GANG,
        schedule_timeout: Optional[int] = 60,
):
    """
    部署 GWS 作业草稿

    :param openapi_context: openapi 上下文
    :param project_id: Flink 项目 ID，例如 "mqp9r338gmbv"
    :param id: 作业草稿 ID，例如 "1855862619368951810"
    :param resource_pool: 资源池名称
    :param queue: 资源池 full name
    :param priority: 优先级，从 "1" 到 "5"，字符串类型，"1" 最高优先级
    :param schedule_policy: 调度策略，"DRF" 或 "GANG"
    :param schedule_timeout: 调度超时时长（秒），仅当 schedule_policy=GANG 时必填
    """

    # === 构造 query 参数 ===
    query = [
        ("ProjectId", project_id),
        ("Id", id),
    ]

    # === 构造请求体 ===
    body = {
        "ResourcePool": resource_pool,
        "Priority": str(priority),
        "SchedulePolicy": str(schedule_policy),
        "Queue": queue,
        "ScheduleTimeout": schedule_timeout,
    }

    logger.info(
        f"Invoke DeployGWSApplicationDraft with query={json.dumps(query, ensure_ascii=False)}, body={json.dumps(body, ensure_ascii=False)}")

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
        action="DeployGWSApplicationDraft",
        version=Version20210601,
        content_type="application/json"
    )

    # === 发送请求 ===
    try:
        resp = openapi_client_invoke(credential, params)
        logger.info(f"DeployGWSApplicationDraft response: {resp}")
        return resp
    except Exception as e:
        logger.error(f"DeployGWSApplicationDraft failed: {str(e)}", exc_info=True)
        raise


def offline_gws_application_api(
        openapi_context: OpenAPIContext,
        project_id: str,
        id: str,
):
    """
    下线 GWS 作业

    :param openapi_context: openapi 上下文
    :param project_id: Flink 项目 ID，例如 "mqp9r338gmbv"
    :param Id: 作业唯一ID
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
        f"Invoke DeleteGWSApplication with query={json.dumps(query, ensure_ascii=False)}, body={json.dumps(body, ensure_ascii=False)}")

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
        action="DeleteGWSApplication",
        version=Version20210601,
        content_type="application/json"
    )

    # === 发送请求 ===
    try:
        resp = openapi_client_invoke(credential, params)
        logger.info(f"DeleteGWSApplication response: {resp}")
        return resp
    except Exception as e:
        logger.error(f"DeleteGWSApplication failed: {str(e)}", exc_info=True)
        raise
