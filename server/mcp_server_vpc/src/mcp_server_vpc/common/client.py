import volcenginesdkcore
from volcenginesdkvpc import VPCApi

from mcp_server_vpc.common import config
from mcp_server_vpc.common import errors


def get_client(
        access_key: str | None = None,
        secret_key: str | None = None,
        endpoint: str | None = None,
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
    try:
        conf = config.VPCConfig()
        configuration = volcenginesdkcore.Configuration()
        configuration.ak = access_key or conf.access_key
        configuration.sk = secret_key or conf.secret_key
        configuration.region = region or conf.region
        configuration.host = endpoint or conf.endpoint
        return VPCApi(volcenginesdkcore.ApiClient(configuration))
    except Exception as e:
        raise errors.VPCError("创建VPC客户端失败", e)
