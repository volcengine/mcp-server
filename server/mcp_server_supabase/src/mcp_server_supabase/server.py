import argparse
import logging
import os

from mcp.server.fastmcp import FastMCP

from .config import READ_ONLY
from .runtime import create_runtime
from .tool_registry import register_tools

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

default_workspace_id = os.getenv("DEFAULT_WORKSPACE_ID")


def create_mcp(
    port: int | None = None,
    default_target_id: str | None = None,
) -> FastMCP:
    resolved_port = port if port is not None else int(os.getenv("PORT", "8000"))
    resolved_default_target_id = default_target_id if default_target_id is not None else default_workspace_id
    runtime = create_runtime(resolved_default_target_id)
    mcp = FastMCP("Supabase MCP Server (AIDAP)", port=resolved_port)
    register_tools(mcp, runtime)
    return mcp


mcp = create_mcp()


def main():
    parser = argparse.ArgumentParser(description="Supabase MCP Server")
    parser.add_argument("--port", type=int, default=8000, help="Port to run the server on")
    args = parser.parse_args()

    logger.info(f"Starting Supabase MCP Server on port {args.port}")
    logger.info(f"Read-only mode: {READ_ONLY}")
    if default_workspace_id:
        logger.info(f"Default workspace ID: {default_workspace_id}")

    create_mcp(port=args.port).run()


if __name__ == "__main__":
    main()
