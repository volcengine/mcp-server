import os
import volcenginesdkcore
import logging
import base64
import json

from volcenginesdkapig.api import APIGApi
from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession
from starlette.requests import Request


logger = logging.getLogger(__name__)


# 获取授权凭证
def get_authorization_credentials(ctx: Context = None) -> tuple[str, str, str]:
    """
    Gets authorization credentials from either environment variables or request headers.

    Args:
        ctx: The server context object

    Returns:
        tuple: (access_key, secret_key, session_token)

    Raises:
        ValueError: If authorization information is missing or invalid
    """
    # First try environment variables
    if "VOLCENGINE_ACCESS_KEY" in os.environ and "VOLCENGINE_SECRET_KEY" in os.environ:
        return (
            os.environ["VOLCENGINE_ACCESS_KEY"],
            os.environ["VOLCENGINE_SECRET_KEY"],
            "",  # No session token for static credentials
        )

    # Try getting auth from request or environment
    _ctx: Context[ServerSession, object] = ctx
    print(_ctx)
    raw_request: Request = _ctx.request_context.request
    auth = None

    if raw_request:
        # Try to get authorization from request headers
        auth = raw_request.headers.get("authorization", None)

    if auth is None:
        # Try to get from environment if not in headers
        auth = os.getenv("authorization", None)

    if auth is None:
        raise ValueError("Missing authorization info.")

    # Parse the authorization string
    if " " in auth:
        _, base64_data = auth.split(" ", 1)
    else:
        base64_data = auth

    try:
        # Decode Base64 and parse JSON
        decoded_str = base64.b64decode(base64_data).decode("utf-8")
        data = json.loads(decoded_str)

        return (
            data.get("AccessKeyId"),
            data.get("SecretAccessKey"),
            data.get("SessionToken"),
        )
    except Exception as e:
        raise ValueError(f"Failed to decode authorization info: {str(e)}")


# 获取APIG客户端
_apig_local_client = None


def get_volc_apig_client(mcp, region: str = None) -> APIGApi:
    global _apig_local_client
    try:
        # 获取凭证
        ak, sk, session_token = get_authorization_credentials(mcp.get_context())
        # 如果 session_token 为空，则表明使用 local 环境变量方式加载凭证
        if session_token == "":
            if _apig_local_client is None:
                apig_config = volcenginesdkcore.Configuration()
                apig_config.ak = ak
                apig_config.sk = sk
                apig_config.region = region or os.environ.get("VOLCENGINE_REGION")
                apig_config.host = os.environ.get("VOLCENGINE_ENDPOINT")
                apig_config.client_side_validation = True
                volcenginesdkcore.Configuration.set_default(apig_config)
                _apig_local_client = APIGApi()
            # 返回客户端
            return _apig_local_client
        # 请求头方式加载凭证
        else:
            # 不使用环境变量，解析请求头中的凭证信息获取 ak 和 sk
            apig_config = volcenginesdkcore.Configuration()
            apig_config.ak = ak
            apig_config.sk = sk
            apig_config.session_token = session_token
            apig_config.client_side_validation = True
            apig_config.region = region
            volcenginesdkcore.Configuration.set_default(apig_config)
            # 返回客户端
            return APIGApi()

    except Exception as e:
        logger.error(f"Failed to get volc apig client: {e}")
        raise e
