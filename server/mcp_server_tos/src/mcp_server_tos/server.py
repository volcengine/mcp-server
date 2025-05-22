import base64
import json
import logging
import os
from typing import Optional

from mcp.server.session import ServerSession
from mcp.server.fastmcp import Context, FastMCP
from starlette.requests import Request

from mcp_server_tos.config import load_config, TosConfig, TOS_CONFIG, LOCAL_DEPLOY_MODE
from mcp_server_tos.credential import Credential
from mcp_server_tos.resources.bucket import BucketResource
from mcp_server_tos.resources.object import ObjectResource

logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("TOS MCP Server", port=int(os.getenv("PORT", "8000")))


def get_credential_from_request():
    ctx: Context[ServerSession, object] = mcp.get_context()
    raw_request: Request | None = ctx.request_context.request

    auth = None
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

    try:
        # 解码 Base64
        decoded_str = base64.b64decode(base64_data).decode('utf-8')
        data = json.loads(decoded_str)
        # 获取字段
        current_time = data.get('CurrentTime')
        expired_time = data.get('ExpiredTime')
        ak = data.get('AccessKeyId')
        sk = data.get('SecretAccessKey')
        session_token = data.get('SessionToken')
        if not ak or not sk or not session_token:
            raise ValueError("Invalid credentials ak, sk, session_token is null")

        logger.info(f"Loaded credentials: {ak},{current_time}, {expired_time}")
        return Credential(ak, sk, session_token, expired_time)
    except Exception as e:
        logger.error(f"Error get credentials: {str(e)}")
        raise


def get_tos_config() -> TosConfig:
    if TOS_CONFIG.deploy_mode == LOCAL_DEPLOY_MODE:
        return TOS_CONFIG
    else:
        credential = get_credential_from_request()
        return TosConfig(
            access_key=credential.access_key,
            secret_key=credential.secret_key,
            security_token=credential.security_token,
            region=TOS_CONFIG.region,
            endpoint=TOS_CONFIG.endpoint,
            deploy_mode=TOS_CONFIG.deploy_mode,
            max_object_size=TOS_CONFIG.max_object_size,
            buckets=[]
        )


@mcp.tool()
async def list_buckets() -> list[dict]:
    """
    List all buckets in TOS.
    Returns:
        A list of buckets.
    """
    try:
        config = get_tos_config()
        tos_resource = BucketResource(config)
        buckets = await tos_resource.list_buckets()
        return buckets
    except Exception as e:
        logger.error(f"Error listing buckets: {e}")
        raise


@mcp.tool()
async def list_objects(bucket: str, prefix: Optional[str] = None, start_after: Optional[str] = None,
                       continuation_token: Optional[str] = None) -> str:
    """
    List all objects in a bucket.
    Args:
        bucket: The name of the bucket.
        prefix: The prefix to filter objects.
        start_after: The start after key to filter objects.
        continuation_token: The continuation token to filter objects.
    Returns:
        A list of objects.
    """
    try:
        config = get_tos_config()
        tos_resource = BucketResource(config)
        objects = await tos_resource.list_objects(bucket, prefix, start_after, continuation_token)
        return objects
    except Exception as e:
        logger.error(f"Error list objects: {e}")
        raise


@mcp.tool()
async def get_object(bucket: str, key: str) -> str:
    """
    Retrieves an object from VolcEngine TOS. In the GetObject request, specify the full key name for the object.
    Args:
        bucket: The name of the bucket.
        key: The key of the object.
    Returns:
        If the object content is text format, return the content as string.
        If the object content is binary format, return the content as base64 encoded string.
    """
    try:
        config = get_tos_config()
        tos_resource = ObjectResource(config)
        content = await tos_resource.get_object(bucket, key)
        return content
    except Exception as e:
        logger.error(f"Error getting object: {e}")
        raise
