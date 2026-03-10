import argparse
import logging
import os

from .runtime import create_runtime
from .tool_registry import register_tools
from .access_policy import build_partial_access_policy
from .scoped_mcp import ScopedFastMCP

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


def _resolve_workspace_ref(workspace_ref: str | None = None) -> str | None:
    if workspace_ref is not None:
        return workspace_ref
    return os.getenv("WORKSPACE_REF")


def _resolve_features(features: str | None = None) -> str | None:
    if features is not None:
        return features
    return os.getenv("FEATURES")


def _resolve_read_only(read_only: str | bool | None = None) -> str | bool | None:
    if read_only is not None:
        return read_only
    return os.getenv("READ_ONLY")


def _resolve_disabled_tools(disabled_tools: str | None = None) -> str | None:
    if disabled_tools is not None:
        return disabled_tools
    return os.getenv("DISABLED_TOOLS")


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
    workspace_ref: str | None = None,
    features: str | None = None,
    read_only: str | bool | None = None,
    disabled_tools: str | None = None,
    mount_path: str | None = None,
    sse_path: str | None = None,
    message_path: str | None = None,
    streamable_http_path: str | None = None,
) -> ScopedFastMCP:
    resolved_port = _resolve_port(port)
    resolved_host = _resolve_host(host)
    access_policy = build_partial_access_policy(
        workspace_ref=_resolve_workspace_ref(workspace_ref),
        features=_resolve_features(features),
        read_only=_resolve_read_only(read_only),
        disabled_tools=_resolve_disabled_tools(disabled_tools),
    )
    mcp = ScopedFastMCP(
        "Supabase MCP Server (Volcengine)",
        access_policy=access_policy,
        host=resolved_host,
        port=resolved_port,
        mount_path=_resolve_mount_path(mount_path),
        sse_path=_resolve_sse_path(sse_path),
        message_path=_resolve_message_path(message_path),
        streamable_http_path=_resolve_streamable_http_path(streamable_http_path),
    )
    runtime = create_runtime(context_getter=mcp.get_context)
    register_tools(mcp, runtime)
    return mcp


mcp = create_mcp()


def run_server(
    transport: str = "stdio",
    port: int | None = None,
    host: str | None = None,
    workspace_ref: str | None = None,
    features: str | None = None,
    read_only: str | bool | None = None,
    disabled_tools: str | None = None,
) -> None:
    create_mcp(
        port=port,
        host=host,
        workspace_ref=workspace_ref,
        features=features,
        read_only=read_only,
        disabled_tools=disabled_tools,
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
    parser.add_argument("--workspace-ref", type=str, default=None, help="Hard-scope the connection to a single workspace")
    parser.add_argument("--features", type=str, default=None, help="Comma-separated official feature groups")
    parser.add_argument("--read-only", nargs="?", const="true", default=None, help="Hide all mutating tools for this connection")
    parser.add_argument("--disabled-tools", type=str, default=None, help="Comma-separated blacklist of tool names")
    args = parser.parse_args()

    resolved_host = _resolve_host(args.host)
    resolved_port = _resolve_port(args.port)
    resolved_workspace_ref = _resolve_workspace_ref(args.workspace_ref)
    resolved_features = _resolve_features(args.features)
    resolved_read_only = _resolve_read_only(args.read_only)
    resolved_disabled_tools = _resolve_disabled_tools(args.disabled_tools)
    resolved_read_only_value = build_partial_access_policy(read_only=resolved_read_only).read_only

    logger.info("Starting Supabase MCP Server with %s transport", args.transport)
    logger.info("Read-only mode: %s", bool(resolved_read_only_value))
    if resolved_workspace_ref:
        logger.info("Workspace scope: %s", resolved_workspace_ref)
    if resolved_features:
        logger.info("Feature groups: %s", resolved_features)
    if resolved_read_only_value is not None:
        logger.info("Connection read_only: %s", resolved_read_only_value)
    if resolved_disabled_tools:
        logger.info("Disabled tools: %s", resolved_disabled_tools)
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
        workspace_ref=args.workspace_ref,
        features=args.features,
        read_only=args.read_only,
        disabled_tools=args.disabled_tools,
    )


if __name__ == "__main__":
    main()
