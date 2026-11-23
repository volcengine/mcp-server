"""Re-export shared OpenAPI client for v3.1.0 compatibility."""

from mcp_server_hiagent_knowledge.common.client import (
    HiAgentOpenAPIClient,
    OpenAPIError,
)

__all__ = ["HiAgentOpenAPIClient", "OpenAPIError"]
