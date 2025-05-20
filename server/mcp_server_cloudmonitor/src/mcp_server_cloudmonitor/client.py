import os
import base64
import json
import volcenginesdkcore
import volcenginesdkvolcobserve
from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession
from starlette.requests import Request

def init_client(region: str = None, ctx: Context = None):
    if "VOLCENGINE_ACCESS_KEY" not in os.environ or "VOLCENGINE_SECRET_KEY" not in os.environ:
        _ctx: Context[ServerSession, object] = ctx
        raw_request: Request = _ctx.request_context.request
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

            ak = data.get('AccessKeyId')
            sk = data.get('SecretAccessKey')
            session_token = data.get('SessionToken')

        except Exception as e:
            raise ValueError("Decode authorization info error", e)
    else:
        ak = os.environ["VOLCENGINE_ACCESS_KEY"]
        sk = os.environ["VOLCENGINE_SECRET_KEY"]
        session_token = ""

    configuration = volcenginesdkcore.Configuration()
    configuration.ak = ak
    configuration.sk = sk
    if session_token:
        configuration.session_token = session_token
    # Set region with default if needed
    region = region if region is not None else "cn-beijing"
    print(f"Using region: {region}")
    configuration.region = region

    # set default configuration
    volcenginesdkcore.Configuration.set_default(configuration)
    return volcenginesdkvolcobserve.VOLCOBSERVEApi()