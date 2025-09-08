import argparse
import os
from typing import Any

from mcp_server_sec_agent.config import SecIntelligentConfig, logger, load_config

config = SecIntelligentConfig(access_key="", secret_key="", region="", endpoint="", security_token="", debug=False)


def set_mcp_config_env(mode: str, **kwargs: Any) -> None:
    """Write environment variables according to the running mode.

    Args:
        mode: Running mode. One of ``streamable``, ``sse``, or ``stdio``.
        **kwargs: Extra key‐value pairs that will be written into environment
            variables named ``FASTMCP_<KEY>`` (upper-case).
    """
    if mode == "stdio":
        return

    # Mode-specific default settings
    if mode == "streamable":
        # Enable JSON response & stateless HTTP by default
        os.environ["FASTMCP_JSON_RESPONSE"] = "true"
        os.environ["FASTMCP_STATELESS_HTTP"] = "true"

    # Write remaining key-value pairs
    for key, value in kwargs.items():
        env_key = f"FASTMCP_{key.upper()}"
        os.environ[env_key] = str(value)


def main():
    """Main entry point for the MCP server."""
    parser = argparse.ArgumentParser(description="Run the SecIntelligent MCP Server")
    parser.add_argument(
        "--transport",
        "-t",
        choices=["sse", "stdio", "streamable-http"],
        default="stdio",
        help="Transport protocol to use (streamable-http, sse, or stdio)",
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host to bind to (only relevant for network transports)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to bind to (only relevant for network transports)",
    )

    args = parser.parse_args()

    try:
        # # Load configuration from environment variables
        global config

        config = load_config(None)
        set_mcp_config_env(args.transport, host=args.host, port=args.port)

        from mcp_server_sec_agent.server import mcp

        # Run the MCP server
        logger.info(
            f"Starting SecIntelligent MCP Server with {args.transport} transport, running on http://{args.host}:{args.port}")

        mcp.run(transport=args.transport)
    except Exception as e:
        logger.error(f"Error starting SecIntelligent MCP Server: {str(e)}")
        raise


if __name__ == "__main__":
    main()
