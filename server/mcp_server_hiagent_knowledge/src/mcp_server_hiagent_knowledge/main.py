"""Command line entrypoint for the HiAgent MCP server."""

from __future__ import annotations

import argparse
import logging
import os

from mcp_server_hiagent_knowledge.versions import (
    DEFAULT_VERSION,
    SUPPORTED_VERSIONS,
    load_version_module,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def main() -> None:
    """Run the HiAgent MCP server."""

    parser = argparse.ArgumentParser(description="Run the HiAgent MCP Server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "streamable-http"],
        default="stdio",
        help="Transport protocol. 'stdio' (default) for local plugin hosts "
        "(e.g. HiAgent STDIO); 'streamable-http' for a long-running HTTP server.",
    )
    parser.add_argument(
        "--tools",
        "-t",
        help="Comma-separated allowlist of tool names to expose (e.g. "
        "'search_wiki,read_wiki_page'). Selects the base tool set; when omitted, "
        "all tools are exposed. Overrides the HIAGENT_TOOLS environment variable. "
        "'health_check' is always available.",
    )
    parser.add_argument(
        "--disabled-tools",
        help="Comma-separated denylist of tool names to hide. Subtracted from the "
        "--tools allowlist (or from all tools when --tools is omitted). Overrides "
        "the HIAGENT_DISABLED_TOOLS environment variable.",
    )
    parser.add_argument(
        "--hiagent-version",
        help="HiAgent OpenAPI compatibility version to use (e.g. "
        f"{DEFAULT_VERSION}). Overrides the HIAGENT_VERSION environment "
        "variable. Defaults to the latest registered version. "
        f"Supported: {', '.join(SUPPORTED_VERSIONS)}.",
    )
    parser.add_argument(
        "--host",
        help="Server host (streamable-http only). Overrides MCP_SERVER_HOST.",
    )
    parser.add_argument(
        "--port",
        type=int,
        help="Server port (streamable-http only). Overrides MCP_SERVER_PORT.",
    )
    args = parser.parse_args()

    # Select the HiAgent OpenAPI compatibility implementation by version.
    # Precedence: --hiagent-version CLI flag > HIAGENT_VERSION env > latest.
    version = (
        (args.hiagent_version or "").strip()
        or os.getenv("HIAGENT_VERSION", "").strip()
        or DEFAULT_VERSION
    )
    if version not in SUPPORTED_VERSIONS:
        parser.error(
            f"unsupported HIAGENT_VERSION {version!r}; "
            f"supported versions: {', '.join(SUPPORTED_VERSIONS)}"
        )
    impl = load_version_module(version)
    logger.info("Using HiAgent version %s", version)

    # Resolve the tool-scope filters. Precedence for each: CLI flag > environment
    # variable > unset (all tools). ``parse_tool_list`` returns ``None`` when
    # neither is provided, which the server treats as "no restriction".
    enabled_tools = impl.parse_tool_list(
        args.tools if args.tools is not None else os.getenv("HIAGENT_TOOLS")
    )
    disabled_tools = impl.parse_tool_list(
        args.disabled_tools
        if args.disabled_tools is not None
        else os.getenv("HIAGENT_DISABLED_TOOLS")
    )

    try:
        mcp = impl.create_mcp_server(
            enabled_tools=enabled_tools,
            disabled_tools=disabled_tools,
        )
    except ValueError as exc:
        # Unknown tool name in --tools / --disabled-tools: fail fast with a clear
        # CLI error instead of a traceback.
        parser.error(str(exc))

    if args.transport == "stdio":
        logger.info("Starting HiAgent MCP Server with stdio transport")
        mcp.run(transport="stdio")
        return

    if args.host:
        os.environ["MCP_SERVER_HOST"] = args.host
    if args.port is not None:
        os.environ["MCP_SERVER_PORT"] = str(args.port)

    server_config = impl.load_server_config()
    logger.info("Starting HiAgent MCP Server with streamable-http transport")
    mcp.run(
        transport="streamable-http",
        host=server_config.host,
        port=server_config.port,
        path=server_config.streamable_http_path,
        stateless_http=server_config.stateless_http,
    )


if __name__ == "__main__":
    main()
