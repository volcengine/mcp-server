"""Re-export shared configuration for v3.1.0 compatibility."""

from mcp_server_hiagent_knowledge.common.config import (
    DEFAULT_ACCOUNT_ID,
    DEFAULT_HOST,
    DEFAULT_PORT,
    DEFAULT_REGION,
    DEFAULT_SERVICE,
    DEFAULT_STREAMABLE_HTTP_PATH,
    HiAgentConfig,
    ServerConfig,
    load_hiagent_config,
    load_server_config,
)

__all__ = [
    "DEFAULT_ACCOUNT_ID",
    "DEFAULT_HOST",
    "DEFAULT_PORT",
    "DEFAULT_REGION",
    "DEFAULT_SERVICE",
    "DEFAULT_STREAMABLE_HTTP_PATH",
    "HiAgentConfig",
    "ServerConfig",
    "load_hiagent_config",
    "load_server_config",
]
