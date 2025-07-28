import base64
import json

import volcenginesdkcore
from volcenginesdkvpc import VPCApi

from mcp_server_vpc.common import config
from mcp_server_vpc.common import errors
from mcp_server_vpc.server import mcp


def get_client(
        region: str | None = None,
) -> VPCApi:
    """
    获取火山引擎VPC客户端

    Args:
        access_key: 访问密钥ID
        secret_key: 访问密钥密码
        endpoint: 服务接入地址
        region: 请求的region

    Returns:
        VPCApi: VPC客户端实例

    Raises:
        VPCError: 创建客户端失败时抛出
    """
    auth_data = {}
    ctx = mcp.get_context()
    if ctx.request_context and ctx.request_context.request and (
            ctx.request_context.request.headers and
            ctx.request_context.request.headers.get("Authorization")):
        auth_header = ctx.request_context.request.headers.get("Authorization")
        if " " in auth_header:
            _, auth_header = auth_header.split(" ", 1)
        try:
            auth_data = json.loads(base64.b64decode(auth_header).decode())
        except Exception as e:
            raise errors.VPCError("获取认证信息失败", e)

    vpc_conf = config.VPCConfig()
    volc_conf = volcenginesdkcore.Configuration()
    volc_conf.ak = auth_data.get("AccessKeyId") or vpc_conf.access_key
    volc_conf.sk = auth_data.get("SecretAccessKey") or vpc_conf.secret_key
    volc_conf.session_token = auth_data.get("SessionToken")
    volc_conf.region = region or vpc_conf.region
    volc_conf.host = vpc_conf.endpoint
    if not ((volc_conf.ak and volc_conf.sk) or volc_conf.session_token):
        raise errors.VPCError("无有效认证信息")
    if not volc_conf.region:
        raise errors.VPCError("未指定请求的region")
    try:
        return VPCApi(volcenginesdkcore.ApiClient(volc_conf))
    except Exception as e:
        raise errors.VPCError("创建VPC客户端失败", e)
