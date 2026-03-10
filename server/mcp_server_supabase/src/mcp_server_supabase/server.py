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

DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 8000
DEFAULT_MOUNT_PATH = "/"
DEFAULT_SSE_PATH = "/sse"
DEFAULT_MESSAGE_PATH = "/messages/"
DEFAULT_STREAMABLE_HTTP_PATH = "/mcp"


def _resolve_port(port: int | None = None) -> int:
    if port is not None:
        return port
    return int(os.getenv("MCP_SERVER_PORT", os.getenv("PORT", str(DEFAULT_PORT))))


def _resolve_host(host: str | None = None) -> str:
    if host is not None:
        return host
    return os.getenv("MCP_SERVER_HOST", DEFAULT_HOST)


def _resolve_default_workspace_id(default_target_id: str | None = None) -> str | None:
    if default_target_id is not None:
        return default_target_id
    return os.getenv("DEFAULT_WORKSPACE_ID")


def _resolve_mount_path(mount_path: str | None = None) -> str:
    if mount_path is not None:
        return mount_path
    return os.getenv("MCP_MOUNT_PATH", DEFAULT_MOUNT_PATH)


def _resolve_sse_path(sse_path: str | None = None) -> str:
    if sse_path is not None:
        return sse_path
    return os.getenv("MCP_SSE_PATH", DEFAULT_SSE_PATH)


def _resolve_message_path(message_path: str | None = None) -> str:
    if message_path is not None:
        return message_path
    return os.getenv("MCP_MESSAGE_PATH", DEFAULT_MESSAGE_PATH)


def _resolve_streamable_http_path(streamable_http_path: str | None = None) -> str:
    if streamable_http_path is not None:
        return streamable_http_path
    return os.getenv("STREAMABLE_HTTP_PATH", DEFAULT_STREAMABLE_HTTP_PATH)


def create_mcp(
    port: int | None = None,
    host: str | None = None,
    default_target_id: str | None = None,
    mount_path: str | None = None,
    sse_path: str | None = None,
    message_path: str | None = None,
    streamable_http_path: str | None = None,
) -> FastMCP:
    resolved_port = _resolve_port(port)
    resolved_host = _resolve_host(host)
    resolved_default_target_id = _resolve_default_workspace_id(default_target_id)
    runtime = create_runtime(resolved_default_target_id)
    mcp = FastMCP(
        "Supabase MCP Server (AIDAP)",
        host=resolved_host,
        port=resolved_port,
        mount_path=_resolve_mount_path(mount_path),
        sse_path=_resolve_sse_path(sse_path),
        message_path=_resolve_message_path(message_path),
        streamable_http_path=_resolve_streamable_http_path(streamable_http_path),
    )
    register_tools(mcp, runtime)
    return mcp


mcp = create_mcp()


def run_server(
    transport: str = "stdio",
    port: int | None = None,
    host: str | None = None,
    default_target_id: str | None = None,
) -> None:
    create_mcp(
        port=port,
        host=host,
        default_target_id=default_target_id,
    ).run(transport=transport)


def main():
    parser = argparse.ArgumentParser(description="Supabase MCP Server")
    parser.add_argument(
        "--transport",
        "-t",
        choices=["sse", "stdio", "streamable-http"],
        default="stdio",
        help="Transport protocol to use",
    )
    parser.add_argument("--host", type=str, default=None, help="Host to bind for network transports")
    parser.add_argument("--port", type=int, default=None, help="Port to run the server on")
    args = parser.parse_args()

    resolved_host = _resolve_host(args.host)
    resolved_port = _resolve_port(args.port)
    resolved_default_workspace_id = _resolve_default_workspace_id()

    logger.info("Starting Supabase MCP Server with %s transport", args.transport)
    logger.info("Read-only mode: %s", READ_ONLY)
    if resolved_default_workspace_id:
        logger.info("Default workspace ID: %s", resolved_default_workspace_id)
    if args.transport != "stdio":
        logger.info(
            "Server binding: host=%s port=%s sse_path=%s message_path=%s streamable_http_path=%s",
            resolved_host,
            resolved_port,
            _resolve_sse_path(),
            _resolve_message_path(),
            _resolve_streamable_http_path(),
        )

    run_server(
        transport=args.transport,
        port=args.port,
        host=args.host,
    )


if __name__ == "__main__":
    main()
