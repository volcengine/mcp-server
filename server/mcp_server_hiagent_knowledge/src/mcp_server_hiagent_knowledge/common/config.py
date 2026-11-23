"""Runtime configuration for the HiAgent MCP server."""

from __future__ import annotations

import os
from dataclasses import dataclass


DEFAULT_REGION = "cn-north-1"
DEFAULT_SERVICE = "app"
DEFAULT_ACCOUNT_ID = "1000000000"
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8000
DEFAULT_STREAMABLE_HTTP_PATH = "/mcp"
DEFAULT_STATELESS_HTTP = True


@dataclass(frozen=True)
class HiAgentConfig:
    """Configuration needed to call HiAgent Platform API."""

    top_host: str
    account_id: str
    access_key_id: str
    secret_access_key: str
    region: str = DEFAULT_REGION
    service: str = DEFAULT_SERVICE

    @property
    def is_configured(self) -> bool:
        return bool(
            self.top_host
            and self.account_id
            and self.access_key_id
            and self.secret_access_key
        )


@dataclass(frozen=True)
class ServerConfig:
    """Configuration for the MCP HTTP server."""

    host: str = DEFAULT_HOST
    port: int = DEFAULT_PORT
    streamable_http_path: str = DEFAULT_STREAMABLE_HTTP_PATH
    stateless_http: bool = DEFAULT_STATELESS_HTTP


def _clean_top_host(value: str) -> str:
    return value.strip().rstrip("/")


def load_hiagent_config() -> HiAgentConfig:
    """Load HiAgent Platform API config from environment variables."""

    return HiAgentConfig(
        top_host=_clean_top_host(os.getenv("HIAGENT_TOP_HOST", "")),
        account_id=(
            os.getenv("HIAGENT_ACCOUNT_ID", DEFAULT_ACCOUNT_ID).strip()
            or DEFAULT_ACCOUNT_ID
        ),
        access_key_id=os.getenv("HIAGENT_ACCESS_KEY_ID", "").strip(),
        secret_access_key=os.getenv("HIAGENT_SECRET_ACCESS_KEY", "").strip(),
        region=os.getenv("HIAGENT_REGION", DEFAULT_REGION).strip() or DEFAULT_REGION,
        service=os.getenv("HIAGENT_SERVICE", DEFAULT_SERVICE).strip() or DEFAULT_SERVICE,
    )


def load_server_config() -> ServerConfig:
    """Load MCP server config from environment variables."""

    raw_port = os.getenv("MCP_SERVER_PORT", str(DEFAULT_PORT)).strip()
    try:
        port = int(raw_port)
    except ValueError as exc:
        raise ValueError("MCP_SERVER_PORT must be an integer") from exc

    return ServerConfig(
        host=os.getenv("MCP_SERVER_HOST", DEFAULT_HOST).strip() or DEFAULT_HOST,
        port=port,
        streamable_http_path=(
            os.getenv("STREAMABLE_HTTP_PATH", DEFAULT_STREAMABLE_HTTP_PATH).strip()
            or DEFAULT_STREAMABLE_HTTP_PATH
        ),
        stateless_http=(
            os.getenv("STATELESS_HTTP", str(DEFAULT_STATELESS_HTTP)).strip().lower()
            == "true"
        ),
    )
