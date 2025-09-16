import os
from dataclasses import dataclass

import volcenginesdkcore
from volcenginesdkcore.interceptor import RuntimeOption

ENV_VOLCENGINE_ENDPOINT = "VOLCENGINE_ENDPOINT"
ENV_VOLCENGINE_REGION = "VOLCENGINE_REGION"
ENV_VOLCENGINE_ACCESS_KEY = "VOLCENGINE_ACCESS_KEY"
ENV_VOLCENGINE_SECRET_KEY = "VOLCENGINE_SECRET_KEY"
ENV_VOLCENGINE_SESSION_TOKEN = "VOLCENGINE_SESSION_TOKEN"

ENV_MCP_SERVER_NAME = "MCP_SERVER_NAME"
ENV_MCP_SERVER_MODE = "MCP_SERVER_MODE"
ENV_MCP_SERVER_HOST = "MCP_SERVER_HOST"
ENV_MCP_SERVER_PORT = "MCP_SERVER_PORT"

ENV_POOL_CONCURRENCY = "POOL_CONCURRENCY"

@dataclass
class VMPConfig:
    """Configuration for VMP MCP Server."""
    volcengine_endpoint: str
    volcengine_region: str
    volcengine_ak: str
    volcengine_sk: str
    session_token: str

    pool_concurrency: int

    def is_valid(self) -> bool:
        """Check if the configuration is valid."""
        if self.volcengine_ak == "" and self.volcengine_sk == "" and self.session_token == "":
            return False
        return True
    
    def to_volc_configuration(self) -> volcenginesdkcore.Configuration:
        """Convert to volcengine configuration."""
        volcConf = volcenginesdkcore.Configuration()
        volcConf.host = self.volcengine_endpoint
        volcConf.region = self.volcengine_region
        volcConf.ak = self.volcengine_ak
        volcConf.sk = self.volcengine_sk
        volcConf.session_token = self.session_token
        volcConf.connection_pool_maxsize = self.pool_concurrency
        return volcConf

    def to_runtime_option(self) -> RuntimeOption:
        """Convert to RuntimeOption."""
        option = RuntimeOption(
            True,
            ak=self.volcengine_ak,
            sk=self.volcengine_sk,
            session_token=self.session_token,
            region=self.volcengine_region,
        )
        return option

def load_env_config() -> VMPConfig:
    """Load configuration from environment variables."""
    return VMPConfig(
        volcengine_endpoint=os.getenv(ENV_VOLCENGINE_ENDPOINT, ""),
        volcengine_region=os.getenv(ENV_VOLCENGINE_REGION, "cn-beijing"),
        volcengine_ak=os.getenv(ENV_VOLCENGINE_ACCESS_KEY, ""),
        volcengine_sk=os.getenv(ENV_VOLCENGINE_SECRET_KEY, ""),
        session_token=os.getenv(ENV_VOLCENGINE_SESSION_TOKEN, ""),
        pool_concurrency=int(os.getenv(ENV_POOL_CONCURRENCY, "0")) or os.cpu_count()*32+1,
    )