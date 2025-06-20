import argparse
import logging
from .config_utils import set_mcp_config_env

# Setup basic logging similar to other entry points
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
_handler = logging.StreamHandler()
_handler.setFormatter(_formatter)
log.addHandler(_handler)


def _set_env_for_transport(transport: str, host: str, port: int) -> None:
    """Set environment variables according to selected transport."""
    mode_map = {
        "stdio": "stdio",
        "sse": "sse",
        "streamable-http": "streamable",
    }
    mode = mode_map[transport]

    if transport == "stdio":
        # Do not need to set host/port for STDIO
        set_mcp_config_env(mode)
    else:
        set_mcp_config_env(mode, host=host, port=port)


def main() -> None:
    """Command-line entry point for running veFaaS MCP with configurable transport."""
    parser = argparse.ArgumentParser(description="Run the veFaaS MCP Server")
    parser.add_argument(
        "--transport",
        "-t",
        choices=["sse", "stdio", "streamable-http"],
        default="stdio",
        help="Transport protocol to use (sse, stdio or streamable-http)",
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

    # 1. Set environment variables BEFORE importing vefaas_server
    _set_env_for_transport(args.transport, args.host, args.port)

    # 2. Import MCP after env vars are set
    from .vefaas_server import mcp  # pylint: disable=import-error,import-outside-toplevel

    log.info("Starting veFaaS MCP Server with %s transport", args.transport)

    # 3. Run MCP
    mcp.run(transport=args.transport)


if __name__ == "__main__":
    main()
