import base64
import hashlib
import hmac
import json
import logging
import os
from mcp.server.session import ServerSession
from mcp.server.fastmcp import Context
from starlette.requests import Request

from urllib.parse import quote

from mcp_server_tls.config import TLS_CONFIG
from mcp_server_tls.consts import *

logger = logging.getLogger(__name__)

def norm_query(params):
    query = ""
    for key in sorted(params.keys()):
        if type(params[key]) == list:
            for k in params[key]:
                query = (
                        query + quote(key, safe="-_.~") + "=" + quote(k, safe="-_.~") + "&"
                )
        else:
            query = (query + quote(key, safe="-_.~") + "=" + quote(params[key], safe="-_.~") + "&")
    query = query[:-1]
    return query.replace("+", "%20")

def hmac_sha256(key: bytes, content: str):
    """sha256 非对称加密
    """
    return hmac.new(key, content.encode("utf-8"), hashlib.sha256).digest()

def hash_sha256(content: str):
    """sha256 hash算法
    """
    return hashlib.sha256(content.encode("utf-8")).hexdigest()

def get_context_from_tools(ctx: Context[ServerSession, object, any]) -> dict:
    """get context in tool, this function should be called in tool
    """
    auth = None
    raw_request: Request = ctx.request_context.request
    if raw_request:
        # 从 header 的 authorization 字段读取 base64 编码后的 sts json
        auth = raw_request.headers.get("authorization", None)

    if auth is None:
        # 如果 header 中没有认证信息，可能是 stdio 模式，尝试从环境变量获取
        auth = os.getenv("authorization", None)

    if auth is None:
        # 获取认证信息失败
        raise ValueError("Missing authorization info.")

    if ' ' in auth:
        _, base64_data = auth.split(' ', 1)
    else:
        base64_data = auth

    auth_info = {}

    try:
        # 解码 Base64
        decoded_str = base64.b64decode(base64_data).decode('utf-8')
        data: dict = json.loads(decoded_str)

        if not data.get('AccessKeyId'):
            raise ValueError("get remote ak failed, it's empty")

        if not data.get('SecretAccessKey'):
            raise ValueError("get remote sk failed, it's empty")

        if bool(data.get("Region")) ^ bool(data.get("Endpoint")):
            raise ValueError("environment variables VOLCENGINE_REGION and VOLCENGINE_ENDPOINT should be set togather")

        # if not data.get("SessionToken"):
        #     raise ValueError("get remote token failed, request just support sts, token should not be")

        # get auth info
        auth_info["current_time"] = data.get('CurrentTime')
        auth_info["expired_time"] = data.get('ExpiredTime')
        auth_info["ak"] = data.get('AccessKeyId')
        auth_info["sk"] = data.get('SecretAccessKey')
        auth_info["token"] = data.get('SessionToken')
        auth_info["region"] = data.get("Region")
        auth_info["endpoint"] = data.get("Endpoint")

    except Exception as e:
        raise ValueError("Decode authorization info error", e)

    return auth_info

def get_sdk_auth_info(ctx: Context[ServerSession, object, any]):
    if TLS_CONFIG.deploy_mode == DEPLOY_MODE_LOCAL:
        return get_local_sdk_auth_info()

    return get_remote_sdk_auth_info(get_context_from_tools(ctx))

def get_local_sdk_auth_info() -> dict:
    return {
        "region": TLS_CONFIG.region,
        "endpoint": TLS_CONFIG.endpoint,
        "ak": TLS_CONFIG.ak,
        "sk": TLS_CONFIG.sk,
        "token": TLS_CONFIG.token,
    }

def get_remote_sdk_auth_info(remote_context_info: dict) -> dict:
    # env has a higher priority
    region = TLS_CONFIG.region or remote_context_info.get("region") or "cn-beijing"
    endpoint = TLS_CONFIG.endpoint or remote_context_info.get("endpoint") or "https://tls-cn-beijing.volces.com"

    # check region and endpoint
    # if not region or not endpoint:
    #     raise ValueError("should set Region or Endpoint in your request header or remote config")

    return {
        "region": region,
        "endpoint": endpoint,
        "ak": remote_context_info.get("ak"),
        "sk": remote_context_info.get("sk"),
        "token": remote_context_info.get("token"),
    }
