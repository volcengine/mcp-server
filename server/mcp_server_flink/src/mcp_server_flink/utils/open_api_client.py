import base64
import json
import logging
import os
import threading
from typing import Dict, Literal, Any, List, Tuple

import volcenginesdkcore
from mcp import ServerSession
from mcp.server.fastmcp import Context
from mcp.server.lowlevel.server import LifespanResultT
from mcp.types import Request
from pydantic import BaseModel

from mcp_server_flink.config import DEFAULT_FLINK_CONFIG

lock = threading.Lock()
mapping = {}

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class Credential(BaseModel):
    ak: str
    sk: str
    service: str
    region: str
    session_token: str = ""
    # Inner/AssumeRole
    mode: str = ""
    role: str = None
    account_id: int = 0


class OpenAPIContext(BaseModel):
    project_name: str = ""
    credential: Credential

    def is_valid(self) -> bool:
        """Check if the configuration is valid."""
        if self.credential.session_token == "" and self.credential.ak == "" and self.credential.sk == "":
            return False
        return True


class RequestParams(BaseModel):
    host: str = ""
    # query or post body
    body: Dict[str, Any] = {}
    query_params: List[Tuple[str, Any]] = []
    method: Literal["POST", "GET", "PUT", "PATCH", "DELETE"]  # 枚举值
    headers: Dict[str, str] = {}  # 字典类型
    action: str
    version: str
    # "text/plain" or "application/json"
    accept: str = "application/json"
    # "text/plain" or "application/json"
    content_type: str = "application/json"


def init_auth_openapi_context(region: str, project_name: str,
                              ctx: Context[ServerSession, LifespanResultT, Request] = None) -> OpenAPIContext:
    """Initialize auth config from env or request context."""
    openapi_context = OpenAPIContext(
        project_name=DEFAULT_FLINK_CONFIG.project_name,
        credential=Credential(
            ak=DEFAULT_FLINK_CONFIG.access_key,
            sk=DEFAULT_FLINK_CONFIG.secret_key,
            service=DEFAULT_FLINK_CONFIG.service,
            region=DEFAULT_FLINK_CONFIG.region,
        )
    )

    if region and len(region) > 0:
        openapi_context.credential.region = region

    if project_name and len(project_name) > 0:
        openapi_context.project_name = project_name

    # 从 context 中获取 header
    raw_request: Request = ctx.request_context.request

    auth = None
    if raw_request:
        # 从 header 的 authorization 字段读取 base64 编码后的 sts json
        auth = raw_request.headers.get("authorization", None)
    if auth is None:
        # 如果 header 中没有认证信息，可能是 stdio 模式，尝试从环境变量获取
        auth = os.getenv("authorization", None)
    if auth is not None:
        if ' ' in auth:
            _, base64_data = auth.split(' ', 1)
        else:
            base64_data = auth

        try:
            # 解码 Base64
            decoded_str = base64.b64decode(base64_data).decode('utf-8')
            data = json.loads(decoded_str)
            # 获取字段
            openapi_context.credential.sk = data.get('AccessKeyId')
            openapi_context.credential.sk = data.get('SecretAccessKey')
            openapi_context.credential.session_token = data.get('SessionToken')
            logger.info(f"OpenAPI credential: {openapi_context.credential}, decoded credential data: {data}")
        except Exception as e:
            raise ValueError("Decode authorization info error", e)
    if not openapi_context.is_valid():
        raise ValueError("No valid auth info found")
    return openapi_context


def openapi_client_invoke(credential: Credential, params: RequestParams):
    collection_formats = {}
    path_params = {}
    header_params = {}
    form_params = []
    local_var_files = {}

    configuration = volcenginesdkcore.Configuration()
    configuration.host = params.host
    configuration.ak = credential.ak
    configuration.sk = credential.sk
    configuration.region = credential.region
    configuration.client_side_validation = True

    client = volcenginesdkcore.ApiClient(configuration)
    query_params = params.query_params
    body_params = params.body
    # HTTP header `Accept`
    header_params['Accept'] = client.select_header_accept(
        [params.accept])  # noqa: E501
    # HTTP header `Content-Type`
    header_params['Content-Type'] = client.select_header_content_type(  # noqa: E501
        [params.content_type])  # noqa: E501
    if params.headers:
        header_params.update(params.headers)
    # Authentication setting
    auth_settings = ['volcengineSign']  # noqa: E501
    true_path = f'/{params.action}/{params.version}/{credential.service}/{params.method.lower()}/{params.content_type.lower().replace("/", "_")}'

    preload_content = False
    if params.host.find("volcengine") != -1:
        preload_content = True
    response = client.call_api(
        true_path, params.method,
        path_params,
        query_params,
        header_params,
        body=body_params,
        post_params=form_params,
        files=local_var_files,
        auth_settings=auth_settings,
        async_req=False,
        response_type=object,
        _return_http_data_only=True,
        _preload_content=preload_content,
        _request_timeout=None,
        collection_formats=collection_formats)

    if not preload_content:
        try:
            response = json.loads(response.data)
        except ValueError:
            response = response.data
    return response


DEFAULT_OPENAPI_CONTEXT = OpenAPIContext(
    project_name=DEFAULT_FLINK_CONFIG.project_name,
    credential=Credential(
        ak=DEFAULT_FLINK_CONFIG.access_key,
        sk=DEFAULT_FLINK_CONFIG.secret_key,
        service=DEFAULT_FLINK_CONFIG.service,
        region=DEFAULT_FLINK_CONFIG.region,
    )
)
