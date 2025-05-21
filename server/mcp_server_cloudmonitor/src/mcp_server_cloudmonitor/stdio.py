import logging

from mcp_server_cloudmonitor.server import mcp

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def main():
    logger.info("CloudMonitor MCP Server started")
    
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
