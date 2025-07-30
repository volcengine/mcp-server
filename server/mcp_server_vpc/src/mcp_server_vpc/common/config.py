import os


class VPCConfig:
    """VPC配置"""

    # MCP
    ENV_MCP_SERVER_HOST = "MCP_SERVER_HOST"
    ENV_MCP_SERVER_PORT = "MCP_SERVER_PORT"

    # SDK
    ENV_ACCESS_KEY = "VOLCENGINE_ACCESS_KEY"
    ENV_SECRET_KEY = "VOLCENGINE_SECRET_KEY"
    ENV_ENDPOINT = "VOLCENGINE_ENDPOINT"
    ENV_REGION = "VOLCENGINE_REGION"

    def __init__(self):
        self._config: dict[str] = {}

        self._config["mcp_server_host"] = os.environ.get(self.ENV_MCP_SERVER_HOST, "127.0.0.1")
        self._config["mcp_server_port"] = os.environ.get(self.ENV_MCP_SERVER_PORT, 8000)

        self._config["access_key"] = os.environ.get(self.ENV_ACCESS_KEY)
        self._config["secret_key"] = os.environ.get(self.ENV_SECRET_KEY)
        self._config["endpoint"] = os.environ.get(self.ENV_ENDPOINT)
        self._config["region"] = os.environ.get(self.ENV_REGION)

    @property
    def mcp_server_host(self) -> str | None:
        """获取MCP server监听地址"""
        return self._config.get("mcp_server_host")

    @property
    def mcp_server_port(self) -> str | None:
        """获取MCP server监听端口"""
        return self._config.get("mcp_server_port")

    @property
    def access_key(self) -> str | None:
        """获取access key"""
        return self._config.get("access_key")

    @property
    def secret_key(self) -> str | None:
        """获取secret key"""
        return self._config.get("secret_key")

    @property
    def endpoint(self) -> str | None:
        """获取服务接入地址"""
        return self._config.get("endpoint")

    @property
    def region(self) -> str | None:
        """获取请求的region"""
        return self._config.get("region")
