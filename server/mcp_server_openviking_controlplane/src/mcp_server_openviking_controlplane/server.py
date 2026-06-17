import argparse
import logging
import os
from typing import Any, Dict, Optional

from mcp.server import FastMCP

from mcp_server_openviking_controlplane.client import ControlPlaneError, get_client

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Create MCP server
mcp = FastMCP(
    "OpenViking Control Plane MCP Server",
    port=int(os.getenv("PORT", "8000")),
    streamable_http_path=os.getenv("STREAMABLE_HTTP_PATH", "/mcp"),
)


def _err(e: Exception) -> Dict[str, Any]:
    if isinstance(e, ControlPlaneError):
        return {"error": {"code": e.code, "message": e.message, "request_id": e.request_id}}
    return {"error": {"message": str(e)}}


@mcp.tool()
def list_collections(project: Optional[str] = None) -> Dict[str, Any]:
    """List OpenViking collections (OV libraries) under the configured account.

    Args:
        project: optional project filter; defaults to the configured project
                 (OPENVIKING_PROJECT, else "default").

    Returns:
        {"Collections": [ ...CollectionInfoData... ]}
    """
    try:
        return get_client().list_collections(project=project)
    except Exception as e:
        logger.error(f"list_collections failed: {e}")
        return _err(e)


@mcp.tool()
def get_collection(resource_id: str) -> Dict[str, Any]:
    """Get basic info of one OpenViking collection by ResourceID.

    Args:
        resource_id: target library ResourceID (the unique primary key).

    Returns:
        CollectionInfoData: Name, Creator, Project, ResourceID, Version, Source,
        Description, Status, OpenvikingVersion, VLM/Embedding (no secrets), CreateTime,
        UpdateTime (Unix seconds), etc.
    """
    try:
        return get_client().get_collection(resource_id)
    except Exception as e:
        logger.error(f"get_collection failed: {e}")
        return _err(e)


@mcp.tool()
def get_usage(resource_id: str) -> Dict[str, Any]:
    """Get overall usage / file counts for one OpenViking collection by ResourceID.

    Args:
        resource_id: target library ResourceID.

    Returns:
        {"CurContextFileNum", "ResourcesFileNum", "UserFileNum", "AgentFileNum",
         "FreshTime" (Unix seconds), "EstimatedCosts"}. Counts are whole-library +
         the three top-level dirs only; per-uri breakdown is not supported.
    """
    try:
        return get_client().get_usage(resource_id)
    except Exception as e:
        logger.error(f"get_usage failed: {e}")
        return _err(e)


@mcp.tool()
def get_collection_api_key(resource_id: str) -> Dict[str, Any]:
    """Get the plaintext data-plane API Key of one collection by ResourceID.

    Backed by the action GetOpenVikingCollectionUserAccess. Returns the library's
    default-user credential. You can only query libraries under your own account;
    there is no cross-account / sudo lookup. NOTE: the ApiKey is plaintext — handle
    and surface it with care.

    Args:
        resource_id: target library ResourceID.

    Returns:
        {"UserID", "Role", "ApiKey"}
    """
    try:
        return get_client().get_user_access(resource_id)
    except Exception as e:
        logger.error(f"get_collection_api_key failed: {e}")
        return _err(e)


@mcp.tool()
def create_collection(
    name: str,
    vlm: Optional[Dict[str, Any]] = None,
    embedding: Optional[Dict[str, Any]] = None,
    source: str = "agentplan",
    version: str = "developer",
    project: Optional[str] = None,
    description: Optional[str] = None,
    openviking_version: Optional[str] = None,
) -> Dict[str, Any]:
    """⚠️ Creates a NEW, BILLABLE OpenViking collection (provisions a Helm release).

    CONFIRM WITH THE USER before calling — this consumes paid quota (max 20 libraries
    per account, returns QuotaExceeded beyond that). Requires the account to have
    AgentPlan deduction activated (otherwise ProductUnordered). Do NOT call
    speculatively.

    Args:
        name: library name, regex ^[a-zA-Z][a-zA-Z0-9_]*$, length <= 64.
        vlm: optional VLM model config, e.g. {"ModelName": "...", "ApiKeyID": "..."}.
             For source="agentplan" this can be omitted — the model name defaults
             to the AgentPlan VLM and the ApiKey falls back to the configured
             AgentPlan key. ApiKeyID and ApiKey are mutually exclusive.
        embedding: optional embedding model config, same shape/defaults as vlm.
        source: model source — "agentplan" (default), "volcengine", or "codeplan".
        version: library version, currently only "developer".
        project: project name; defaults to the configured project.
        description: optional, length <= 65535.
        openviking_version: optional image version.

    Returns:
        {"ResourceID": "...", "Success": true}
    """
    try:
        return get_client().create_collection(
            name=name,
            source=source,
            vlm=vlm,
            embedding=embedding,
            version=version,
            project=project,
            description=description,
            openviking_version=openviking_version,
        )
    except Exception as e:
        logger.error(f"create_collection failed: {e}")
        return _err(e)


@mcp.tool()
def delete_collection(resource_id: str) -> Dict[str, Any]:
    """⚠️ IRREVERSIBLY deletes an OpenViking collection (uninstalls its Helm release).

    CONFIRM WITH THE USER before calling. This cannot be undone; all data in the
    library is lost.

    Args:
        resource_id: target library ResourceID.

    Returns:
        {"Success": true}
    """
    try:
        return get_client().delete_collection(resource_id)
    except Exception as e:
        logger.error(f"delete_collection failed: {e}")
        return _err(e)


def main():
    """Main entry point for the OpenViking Control Plane MCP server."""
    parser = argparse.ArgumentParser(description="Run the OpenViking Control Plane MCP Server")
    parser.add_argument(
        "--transport",
        "-t",
        choices=["sse", "stdio"],
        default="stdio",
        help="Transport protocol to use (sse or stdio)",
    )
    args = parser.parse_args()
    logger.info(f"Starting OpenViking Control Plane MCP Server with {args.transport} transport")

    try:
        mcp.run(transport=args.transport)
    except Exception as e:
        logger.error(f"Error starting OpenViking Control Plane MCP Server: {str(e)}")
        raise


if __name__ == "__main__":
    main()
