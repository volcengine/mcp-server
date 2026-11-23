"""Re-export shared OpenAPI request signer for v3.1.0 compatibility."""

from mcp_server_hiagent_knowledge.common.signer import (
    SignedRequest,
    sign_openapi_request,
)

__all__ = ["SignedRequest", "sign_openapi_request"]
