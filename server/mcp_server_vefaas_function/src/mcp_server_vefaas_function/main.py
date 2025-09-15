import argparse
import logging
from .vefaas_server import mcp

# Basic logging similar to other entry points
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
_handler = logging.StreamHandler()
_handler.setFormatter(_formatter)
log.addHandler(_handler)

def main():
    """Main entry point for the MCP server."""
    parser = argparse.ArgumentParser(description="Run veFaaS MCP Server")
    parser.add_argument(
        "--transport",
        "-t",
        choices=["sse", "stdio", "streamable-http"],
        default="stdio",
        help="Transport protocol to use (sse, stdio or streamable-http)",
    )

    args = parser.parse_args()

    try:
        # Run the MCP server
        log.info(f"Starting veFaaS MCP Server with {args.transport} transport")
        mcp.run(transport=args.transport)
    except Exception as e:
        log.error(f"Error starting veFaaS MCP Server: {str(e)}")
        raise

if __name__ == "__main__":
    main()
