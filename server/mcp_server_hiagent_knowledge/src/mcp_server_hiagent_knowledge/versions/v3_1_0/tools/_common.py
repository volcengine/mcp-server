"""Re-export shared OpenAPI protocol and constants for v3.1.0 compatibility."""

from mcp_server_hiagent_knowledge.common.tools._common import (
    OPENAPI_SERVICE,
    OPENAPI_VERSION,
    OpenAPIClient,
)

__all__ = ["OPENAPI_SERVICE", "OPENAPI_VERSION", "OpenAPIClient"]
