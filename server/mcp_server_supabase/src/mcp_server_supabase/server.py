import argparse
import logging
import os
from dataclasses import dataclass

from .runtime import create_runtime
from .tool_registry import register_tools
from .access_policy import AccessPolicy, build_access_policy
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


@dataclass(frozen=True, slots=True)
class ServerConfig:
    host: str
    port: int
    access_policy: AccessPolicy
    mount_path: str
    sse_path: str
    message_path: str
    streamable_http_path: str


def _resolve_string(value: str | None, env_name: str, default: str | None = None) -> str | None:
    if value is not None:
        return value
    if default is None:
        return os.getenv(env_name)
    return os.getenv(env_name, default)


def _resolve_read_only(read_only: str | bool | None) -> str | bool | None:
    if read_only is not None:
        return read_only
    return os.getenv("READ_ONLY")


def build_server_config(
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
) -> ServerConfig:
    resolved_port = port if port is not None else int(os.getenv("MCP_SERVER_PORT", os.getenv("PORT", str(DEFAULT_PORT))))
    resolved_host = _resolve_string(host, "MCP_SERVER_HOST", DEFAULT_HOST) or DEFAULT_HOST
    return ServerConfig(
        host=resolved_host,
        port=resolved_port,
        access_policy=build_access_policy(
            workspace_ref=_resolve_string(workspace_ref, "WORKSPACE_REF"),
            features=_resolve_string(features, "FEATURES"),
            read_only=_resolve_read_only(read_only),
            disabled_tools=_resolve_string(disabled_tools, "DISABLED_TOOLS"),
        ),
        mount_path=_resolve_string(mount_path, "MCP_MOUNT_PATH", DEFAULT_MOUNT_PATH) or DEFAULT_MOUNT_PATH,
        sse_path=_resolve_string(sse_path, "MCP_SSE_PATH", DEFAULT_SSE_PATH) or DEFAULT_SSE_PATH,
        message_path=_resolve_string(message_path, "MCP_MESSAGE_PATH", DEFAULT_MESSAGE_PATH) or DEFAULT_MESSAGE_PATH,
        streamable_http_path=_resolve_string(streamable_http_path, "STREAMABLE_HTTP_PATH", DEFAULT_STREAMABLE_HTTP_PATH) or DEFAULT_STREAMABLE_HTTP_PATH,
    )


def create_mcp(config: ServerConfig) -> ScopedFastMCP:
    mcp = ScopedFastMCP(
        "Supabase MCP Server (Volcengine)",
        access_policy=config.access_policy,
        host=config.host,
        port=config.port,
        mount_path=config.mount_path,
        sse_path=config.sse_path,
        message_path=config.message_path,
        streamable_http_path=config.streamable_http_path,
    )
    runtime = create_runtime(context_getter=mcp.get_context)
    register_tools(mcp, runtime)
    return mcp


def run_server(
    transport: str = "stdio",
    port: int | None = None,
    host: str | None = None,
    workspace_ref: str | None = None,
    features: str | None = None,
    read_only: str | bool | None = None,
    disabled_tools: str | None = None,
) -> None:
    config = build_server_config(
        port=port,
        host=host,
        workspace_ref=workspace_ref,
        features=features,
        read_only=read_only,
        disabled_tools=disabled_tools,
    )
    create_mcp(config).run(transport=transport)


def main() -> None:
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
    parser.add_argument("--workspace-ref", type=str, default=None, help="Hard-scope the server to a single workspace")
    parser.add_argument("--features", type=str, default=None, help="Comma-separated official feature groups")
    parser.add_argument("--read-only", nargs="?", const="true", default=None, help="Hide all mutating tools for the server")
    parser.add_argument("--disabled-tools", type=str, default=None, help="Comma-separated blacklist of tool names")
    args = parser.parse_args()

    config = build_server_config(
        port=args.port,
        host=args.host,
        workspace_ref=args.workspace_ref,
        features=args.features,
        read_only=args.read_only,
        disabled_tools=args.disabled_tools,
    )

    logger.info("Starting Supabase MCP Server with %s transport", args.transport)
    logger.info("Read-only mode: %s", config.access_policy.read_only)
    if config.access_policy.workspace_ref:
        logger.info("Workspace scope: %s", config.access_policy.workspace_ref)
    logger.info("Feature groups: %s", ",".join(sorted(config.access_policy.features)))
    if config.access_policy.disabled_tools:
        logger.info("Disabled tools: %s", ",".join(sorted(config.access_policy.disabled_tools)))
    if args.transport != "stdio":
        logger.info(
            "Server binding: host=%s port=%s sse_path=%s message_path=%s streamable_http_path=%s",
            config.host,
            config.port,
            config.sse_path,
            config.message_path,
            config.streamable_http_path,
        )

    create_mcp(config).run(transport=args.transport)


if __name__ == "__main__":
    main()
