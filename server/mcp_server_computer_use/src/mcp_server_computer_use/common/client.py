import os
from typing import Optional

from tool_server_client.client import ComputerUseClient, new_computer_use_client

from mcp_server_computer_use.common.logs import LOG
from mcp_server_computer_use.common.config import (
    tool_server_config,
    plugins_config,
    ssl_config,
)

_local_client = None


def _resolve_auth_key() -> str:
    return os.environ.get("AUTH_API_KEY") or tool_server_config.get("auth_key", "")


def _resolve_client_ca() -> Optional[str]:
    enable_https_env = os.environ.get("TOOL_SERVER_ENABLE_HTTPS")
    if enable_https_env is not None:
        enable_https = enable_https_env.strip().lower() in ("1", "true", "yes", "on")
    else:
        enable_https = bool(plugins_config.get("enable_https", False))

    if not enable_https:
        return None

    return os.environ.get("TOOL_SERVER_CLIENT_CA") or ssl_config.get("client_ca") or None


def tool_server_client(endpoint: str = None) -> ComputerUseClient:
    global _local_client

    auth_key = _resolve_auth_key()
    client_ca = _resolve_client_ca()

    try:
        if tool_server_config["local"]:
            if _local_client is None:
                endpoint = endpoint or os.environ.get(
                    "TOOL_SERVER_ENDPOINT") or tool_server_config["endpoint"]
                _local_client = new_computer_use_client(
                    endpoint, auth_key=auth_key, client_ca=client_ca
                )

            return _local_client
        else:
            LOG.info(f"Get client, endpoint: {endpoint}")
            return new_computer_use_client(
                endpoint, auth_key=auth_key, client_ca=client_ca
            )

    except Exception as e:
        LOG.error(f"Get client failed: {str(e)}")
        raise e