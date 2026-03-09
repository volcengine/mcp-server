"""Configuration for HQD MCP Server (remote proxy mode)."""

import os
import logging
from dataclasses import dataclass

from dotenv import load_dotenv

logger = logging.getLogger(__name__)

load_dotenv()


@dataclass
class HqdConfig:
    """Configuration for HQD MCP proxy server.

    Environment variables:
        HQD_MCP_ENDPOINT: Remote HQD MCP server endpoint (streamable-http)
        PORT: Local server port (default: 8000)
    """

    endpoint: str
    port: int


def load_config() -> HqdConfig:
    """Load configuration from environment variables."""
    endpoint = os.getenv(
        "HQD_MCP_ENDPOINT",
        "https://sd6k08f59gqcea6qe13vg.apigateway-cn-beijing.volceapi.com/mcp",
    )
    if not endpoint:
        raise ValueError("Missing required environment variable: HQD_MCP_ENDPOINT")

    return HqdConfig(
        endpoint=endpoint,
        port=int(os.getenv("PORT", "8000")),
    )


config = load_config()
