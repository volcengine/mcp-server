import base64
import json

from starlette.requests import Request

from mcp_server_ecs.common.logs import LOG
from mcp_server_ecs.tools import mcp


def get_auth_info():
    raw_request: Request = mcp.get_context().request_context.request
    auth = raw_request.headers.get("authorization", None)
    if auth is None:
        LOG.error("Missing authorization info")
        raise ValueError("Missing authorization info")

    if " " in auth:
        _, base64_data = auth.split(" ", 1)
    else:
        base64_data = auth

    try:
        decoded_str = base64.b64decode(base64_data).decode("utf-8")
        data = json.loads(decoded_str)

        ak = data.get("AccessKeyId")
        sk = data.get("SecretAccessKey")
        session_token = data.get("SessionToken")

        return ak, sk, session_token

    except Exception as e:
        LOG.error(f"Decode authorization info error: {e}")
        raise ValueError(f"Decode authorization info error: {e}")
