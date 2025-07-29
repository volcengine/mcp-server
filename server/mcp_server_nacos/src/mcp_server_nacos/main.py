import argparse
import logging

from .nacos_server import mcp

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ch = logging.StreamHandler()
ch.setFormatter(formatter)
log.addHandler(ch)


def main():
    parser = argparse.ArgumentParser(description="Run the NACOS MCP Server")
    parser.add_argument(
        "--transport",
        "-t",
        choices=["sse", "stdio", "streamable-http"],
        default="stdio",
        help="Transport protocol to use (sse, stdio or streamable-http)",
    )

    args = parser.parse_args()
    log.info(f"Starting NACOS MCP Server with {args.transport} transport")

    mcp.run(transport=args.transport)


if __name__ == "__main__":
    main()